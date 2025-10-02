// kb_y0DatabaseImporter.js
// Importador para a aba Y0_Database (PPC/PACTO)
// Cobre: 30x30 (contagem por espécie), 3x3 (subparcela, contagem por espécie), DAP >10cm (árvore individual)

import { Op, Sequelize } from "sequelize";

// MODELS – ajuste caminhos/nomes conforme sua estrutura de carregamento
import ParcelaMonitoramento from "../models/kobo/parcela-monitoramento.model.js";
import SubparcelaMonitoramento from "../models/kobo/subparcela-monitoramento.model.js";
import ArvorePlantadaDAP10 from "../models/kobo/arvore-dap-10cm.model.js";
import SubparcelaArvore from "../models/kobo/subparcela-arvore.model.js";
import Arvore from "../models/kobo/arvore.model.js";
import Especie from "../models/catalogo/especie.model.js";

// =============== Helpers utilitários ===============

const clean = (v) => {
  if (v === undefined || v === null) return null;
  const s = String(v).trim();
  return s.length ? s : null;
};

const toFloat = (v) => {
  if (v === undefined || v === null || v === "") return null;
  // aceita vírgula decimal
  const s = String(v).replace(",", ".").replace(/[^\d.-]/g, "");
  const n = parseFloat(s);
  return Number.isFinite(n) ? n : null;
};

const toInt = (v) => {
  if (v === undefined || v === null || v === "") return null;
  const s = String(v).replace(/[^\d-]/g, "");
  const n = parseInt(s, 10);
  return Number.isFinite(n) ? n : null;
};

// Busca tolerante de chave no JSON
function getVal(row, candidates) {
  for (const c of candidates) {
    for (const key of Object.keys(row)) {
      if (key.toLowerCase() === c.toLowerCase()) return row[key];
    }
  }
  // fallback por regex “contém”
  for (const c of candidates) {
    const rx = new RegExp(c, "i");
    for (const key of Object.keys(row)) {
      if (rx.test(key)) return row[key];
    }
  }
  return null;
}

// Normaliza possíveis cabeçalhos usados na Y0_Database
function extractCommonFields(row) {
  const tamanhoParcela = clean(
    getVal(row, [
      "Tamanho_parcela",
      "Tamanho da parcela",
      "Tipo de Parcela (30x30/3x3)",
      "Tamanho da Parcela",
    ])
  );

  const idParcela = clean(
    getVal(row, [
      "Identificação (ID) da Parcela de Monitoramento de Árvores",
      "ID da Parcela",
      "ID Parcela",
      "Parcela_ID",
      "Identificação da Parcela",
    ])
  );

  // Subparcela: às vezes não vem explícita; se vier, ótimo
  const idSubparcela = clean(
    getVal(row, ["ID Subparcela", "Subparcela_ID", "Identificação da Subparcela"])
  );

  const especieCientifico = clean(
    getVal(row, [
      "Espécie (nome científico)",
      "Especie (nome científico)",
      "Especie (nome cientifico)",
      "Nome científico",
      "Nome cientifico",
      "Especie",
      "Espécie",
    ])
  );

  const especiePopular = clean(
    getVal(row, [
      "Nome comum",
      "Nome popular",
      "Popular",
      "Comum",
    ])
  );

  const quantidade = toInt(
    getVal(row, [
      "Número de indivíduos",
      "Numero de individuos",
      "Quantidade",
      "Qtde",
      "N",
      "n",
    ])
  );

  // DAP individual
  const dap_cm =
    toFloat(getVal(row, ["DAP (diam)", "DAP cm", "DAP", "Diametro à altura do peito (cm)"])) ??
    toFloat(getVal(row, ["DAP_cm", "DAP (cm)"]));

  const numeroArvore = toInt(getVal(row, ["Número da árvore", "Numero da arvore", "Arvore_N", "Árvore N", "Tree #"]));
  const numeroFuste = toInt(getVal(row, ["Número de fuste", "Numero de fuste", "Fuste_N"]));

  return {
    tamanhoParcela,
    idParcela,
    idSubparcela,
    especieCientifico,
    especiePopular,
    quantidade,
    dap_cm,
    numeroArvore,
    numeroFuste,
  };
}

function classifyRowType(fields) {
  const tp = (fields.tamanhoParcela || "").replace(/\s/g, "").toLowerCase();
  const hasDap = fields.dap_cm !== null && fields.dap_cm !== undefined;

  // Se tem DAP, tratamos como árvore individual (>10 cm)
  if (hasDap) return "DAP_INDIVIDUAL";

  // Sem DAP: usa tamanhoParcela para decidir o agregador
  if (tp.includes("30x30") || tp.includes("30×30")) return "PARCELA_30x30";
  if (tp.includes("3x3") || tp.includes("3×3")) return "SUBPARCELA_3x3";

  // fallback: se tem idSubparcela → subparcela; senão, parcela
  if (fields.idSubparcela) return "SUBPARCELA_3x3";
  return "PARCELA_30x30";
}

// Especie helpers
async function getOrCreateEspecie({ cientifico, popular }, { transaction } = {}) {
  const sci = clean(cientifico);
  const pop = clean(popular);

  // tenta por nome científico primeiro (case-insensitive)
  if (sci) {
    const found = await Especie.findOne({
      where: Sequelize.where(Sequelize.fn("lower", Sequelize.col("nome_cientifico")), sci.toLowerCase()),
      transaction,
    });
    if (found) return found;

    return await Especie.create(
      { nome_cientifico: sci, nome_popular: pop || null },
      { transaction }
    );
  }

  // tenta por popular se não houver científico
  if (pop) {
    const found = await Especie.findOne({
      where: Sequelize.where(Sequelize.fn("lower", Sequelize.col("nome_popular")), pop.toLowerCase()),
      transaction,
    });
    if (found) return found;

    return await Especie.create(
      { nome_cientifico: null, nome_popular: pop },
      { transaction }
    );
  }

  // Sem nomes → especie “Desconhecida” (ou null, conforme sua regra)
  const unk = await Especie.findOne({
    where: { nome_cientifico: null, nome_popular: "Desconhecida" },
    transaction,
  });
  if (unk) return unk;

  return await Especie.create(
    { nome_cientifico: null, nome_popular: "Desconhecida" },
    { transaction }
  );
}

async function getParcelaByExternalId(idParcela, { transaction } = {}) {
  if (!idParcela) return null;
  return await ParcelaMonitoramento.findOne({
    where: { idParcela: { [Op.iLike]: idParcela } },
    transaction,
  });
}

async function getSubparcela({ parcelaId, idSubparcela }, { transaction } = {}) {
  // Prioriza idSubparcela se veio no arquivo
  if (idSubparcela) {
    const found = await SubparcelaMonitoramento.findOne({
      where: { parcelaId, idSubparcela: { [Op.iLike]: idSubparcela } },
      transaction,
    });
    if (found) return found;
  }
  // Fallback: pega a “primeira” subparcela da parcela
  return await SubparcelaMonitoramento.findOne({ where: { parcelaId }, transaction });
}

// =============== Import principal ===============

export async function kb_importY0_Database(rows) {
  if (!Array.isArray(rows) || rows.length === 0) return { inserted: 0, updated: 0, skipped: 0 };

  let inserted = 0, updated = 0, skipped = 0;

  await ParcelaMonitoramento.sequelize.transaction(async (t) => {
    for (const raw of rows) {
      try {
        const f = extractCommonFields(raw);
        const tipo = classifyRowType(f);

        // Localiza a parcela base (criada na PPC/PACTO)
        const parcela = await getParcelaByExternalId(f.idParcela, { transaction: t });
        if (!parcela) {
          skipped++;
          // eslint-disable-next-line no-console
          console.warn(`[Y0] Parcela não encontrada para idParcela='${f.idParcela}'. Linha ignorada.`);
          continue;
        }

        if (tipo === "PARCELA_30x30") {
          // Contagem por espécie na parcela (30x30) → ArvorePlantadaDAP10
          const especie = await getOrCreateEspecie(
            { cientifico: f.especieCientifico, popular: f.especiePopular },
            { transaction: t }
          );

          // Idempotência: (parcelaId, especieId) único
          const [rec, created] = await ArvorePlantadaDAP10.findOrCreate({
            where: { parcelaId: parcela.id, especieId: especie.id },
            defaults: {
              parcelaId: parcela.id,
              especieId: especie.id,
              numeroArvores: f.quantidade ?? 0,
            },
            transaction: t,
          });

          if (!created) {
            // atualiza contagem (se quiser somar em vez de substituir, troque a lógica)
            const prev = rec.get("numeroArvores") ?? 0;
            const next = f.quantidade ?? prev;
            if (next !== prev) {
              await rec.update({ numeroArvores: next }, { transaction: t });
              updated++;
            } else {
              skipped++;
            }
          } else {
            inserted++;
          }
        } else if (tipo === "SUBPARCELA_3x3") {
          // Contagem por espécie na subparcela (3x3) → SubparcelaArvore
          const sub = await getSubparcela(
            { parcelaId: parcela.id, idSubparcela: f.idSubparcela },
            { transaction: t }
          );
          if (!sub) {
            skipped++;
            console.warn(`[Y0] Subparcela não encontrada para parcela='${f.idParcela}', idSubparcela='${f.idSubparcela || "(não informado)"}'. Linha ignorada.`);
            continue;
          }

          const especie = await getOrCreateEspecie(
            { cientifico: f.especieCientifico, popular: f.especiePopular },
            { transaction: t }
          );

          // Idempotência: (subparcelaId, especieId) único
          const [rec, created] = await SubparcelaArvore.findOrCreate({
            where: { subparcelaId: sub.id, especieId: especie.id },
            defaults: {
              subparcelaId: sub.id,
              especieId: especie.id,
              numeroArvoresEspecie: f.quantidade ?? 0,
            },
            transaction: t,
          });

          if (!created) {
            const prev = rec.get("numeroArvoresEspecie") ?? 0;
            const next = f.quantidade ?? prev;
            if (next !== prev) {
              await rec.update({ numeroArvoresEspecie: next }, { transaction: t });
              updated++;
            } else {
              skipped++;
            }
          } else {
            inserted++;
          }
        } else if (tipo === "DAP_INDIVIDUAL") {
          // Árvore individual (>10 cm) → Arvore
          const especie = await getOrCreateEspecie(
            { cientifico: f.especieCientifico, popular: f.especiePopular },
            { transaction: t }
          );

          // Chave idempotente: (parcelaId, especieId, numeroArvore, numeroFuste, dap_cm)
          // Se não houver número de árvore, usa só (parcelaId, especieId, dap_cm) como fallback.
          const where = {
            parcelaId: parcela.id,
            especieId: especie.id,
            dap_cm: f.dap_cm ?? null,
          };
          if (f.numeroArvore != null) where.numeroArvore = f.numeroArvore;
          if (f.numeroFuste != null) where.numeroFuste = f.numeroFuste;

          const [rec, created] = await Arvore.findOrCreate({
            where,
            defaults: {
              parcelaId: parcela.id,
              especieId: especie.id,
              dap_cm: f.dap_cm ?? null,
              numeroArvore: f.numeroArvore ?? null,
              numeroFuste: f.numeroFuste ?? null,
            },
            transaction: t,
          });

          if (!created) {
            // nada a atualizar por padrão; se quiser atualizar DAP em duplicata, faça aqui
            skipped++;
          } else {
            inserted++;
          }
        } else {
          skipped++;
          console.warn(`[Y0] Tipo de linha não reconhecido. idParcela='${f.idParcela}', tamanho='${f.tamanhoParcela}'`);
        }
      } catch (err) {
        skipped++;
        console.error("[Y0] Erro ao processar linha:", err?.message || err);
      }
    }
  });

  return { inserted, updated, skipped };
}
