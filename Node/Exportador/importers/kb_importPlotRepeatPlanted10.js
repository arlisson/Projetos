import Monitoramento from "../models/kobo/monitoramento.model.js";
import ParcelaMonitoramento from "../models/kobo/parcela-monitoramento.model.js";
import ArvorePlantadaDAP10 from "../models/kobo/arvore-dap-10cm.model.js";
import { getOrCreateEspecieId } from "../utils/especieHelper.js";
import { Op } from "sequelize"; // se ainda não estiver importado neste arquivo
import Especie from "#models/catalogo/especie.model.js";


export async function kb_importPlotRepeatPlanted10(rows = []) {
  

  let inserted = 0, updated = 0, skippedZero = 0, unresolved = 0, errors = 0;

  // helper local
  const toInt = (v) => {
    if (v === null || v === undefined || String(v).trim() === "") return NaN;
    const n = Number(String(v).replace(",", "."));
    return Number.isFinite(n) ? Math.trunc(n) : NaN;
  };

  for (const [i, row] of rows.entries()) {
    try {
      const submissionUuid = (row["_submission__uuid"] || "").toString().trim().toLowerCase();
      const especieRaw = row["Espécies de árvores (use nome científico)"];
      const qtdRaw = row["Número de Árvores desta Espécie"];
      const qtd = toInt(qtdRaw);

      if (!submissionUuid) {
        unresolved++;
        console.warn(`   ⚠️ [linha ${i + 1}] Sem _submission__uuid.`);
        continue;
      }

      // 1) achar monitoramento pelo UUID do envio principal
      const monitoramento = await Monitoramento.findOne({
        where: { uuid: submissionUuid },
        attributes: ["id"],
      });
      if (!monitoramento) {
        unresolved++;
        console.warn(`   ⚠️ [linha ${i + 1}] Monitoramento não encontrado para uuid=${submissionUuid}`);
        continue;
      }

      // 2) pegar a parcela (assumindo 1 parcela por envio; se houver várias, pega a primeira por criação)
      const parcela = await ParcelaMonitoramento.findOne({
        where: { monitoramentoId: monitoramento.id },
        order: [["criado_em", "ASC"]],
        attributes: ["id"],
      });
      if (!parcela) {
        unresolved++;
        console.warn(`   ⚠️ [linha ${i + 1}] Parcela não encontrada para monitoramento_id=${monitoramento.id}`);
        continue;
      }

      // 3) quantidade
      if (!Number.isFinite(qtd) || qtd <= 0) {
        skippedZero++;
        console.log(`   ↳ [linha ${i + 1}] Quantidade inválida/zero ("${qtdRaw}"). Pulando.`);
        continue;
      }

     
      // 4) espécie
        let especieId = await getOrCreateEspecieId(especieRaw);

        if (!especieId) {
        // findOrCreate da espécie "desconhecida"
        const existing = await Especie.findOne({
            where: { nome: { [Op.iLike]: "desconhecida" } },
            attributes: ["id"],
        });

        if (existing?.id) {
            especieId = existing.id;
        } else {
            const created = await Especie.create({
            nome: "desconhecida",
            nome_cientifico: null,
            });
            especieId = created.id;
        }
        }

      if (!especieId) {
        unresolved++;
        console.warn(`   ⚠️ [linha ${i + 1}] Espécie não reconhecida: "${especieRaw}"`);
        continue;
      }

      // 5) upsert por (parcelaId, especieId, tipoArvore='plantada')
      const [rec, created] = await ArvorePlantadaDAP10.findOrCreate({
        where: {
          parcelaId: parcela.id,
          especieId,
          tipoArvore: "plantada",
        },
        defaults: {
          parcelaId: parcela.id,
          especieId,
          tipoArvore: "plantada",
          numeroArvores: qtd,
        },
      });

      if (!created) {
        // atualiza contagem
        await rec.update({ numeroArvores: qtd });
        updated++;
      } else {
        inserted++;
      }
    } catch (err) {
      errors++;
      console.error(`❌ Planted_10cm erro na linha ${i + 1}:`, {
        name: err.name,
        message: err.message,
        details: err.errors ? err.errors.map((e) => e.message) : null,
      });
    }
  }
 
  return { inserted, updated, skippedZero, unresolved, errors };
}
