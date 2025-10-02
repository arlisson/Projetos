// kb_y0DatabaseImporter.js
// Importador para a aba Y0_Database (PPC/PACTO)
// 30x30 → ArvorePlantadaDAP10; 3x3 → SubparcelaArvore; DAP>10 → Arvore
// Compatível com ENUMs: 'plantada' | 'regenerando' | 'presente_antes' | 'desconhecido'
// Recompute de kb_y0_database_arvore embutido ao final (sem alterar models)

import { Op, Sequelize } from "sequelize";

// ==== Ajuste os paths conforme seu projeto ====
import ParcelaMonitoramento from "../models/kobo/parcela-monitoramento.model.js";
import SubparcelaMonitoramento from "../models/kobo/subparcela-monitoramento.model.js";
import ArvorePlantadaDAP10 from "../models/kobo/arvore-dap-10cm.model.js";
import SubparcelaArvore from "../models/kobo/subparcela-arvore.model.js";
import Arvore from "../models/kobo/arvore.model.js";
import Especie from "../models/catalogo/especie.model.js";
import Y0DatabaseArvore from "../models/kobo/y0-database-arvore.model.js"; // <-- ajuste o path

// ================== Utils ==================
const clean = (v) => {
  if (v === undefined || v === null) return null;
  const s = String(v).trim();
  return s.length ? s : null;
};

const toFloat = (v) => {
  if (v === undefined || v === null || v === "") return null;
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

// Busca tolerante de chave (nome exato → regex contém)
function getVal(row, candidates) {
  for (const c of candidates) {
    for (const key of Object.keys(row)) {
      if (key.toLowerCase() === c.toLowerCase()) return row[key];
    }
  }
  for (const c of candidates) {
    const rx = new RegExp(c, "i");
    for (const key of Object.keys(row)) {
      if (rx.test(key)) return row[key];
    }
  }
  return null;
}

// Normaliza idParcela para casar "03" ↔ "3"
function variantsForIdParcela(raw, padLen = 2) {
  const s = String(raw || "").trim();
  if (!s) return [];
  const set = new Set([s]);
  const noLead = s.replace(/^0+/, "") || "0";
  set.add(noLead);
  if (/^\d+$/.test(noLead)) set.add(noLead.padStart(padLen, "0"));
  return Array.from(set);
}

// ================== ENUM helper ==================
/** ENUM aceito no banco: */
const ENUM_TIPO = new Set(["plantada", "regenerando", "presente_antes", "desconhecido"]);

/**
 * Mapeia qualquer string da planilha para UM dos 4 valores do ENUM.
 * - Se não vier nada (null/empty) → retorna null (não força).
 * - Se vier algo não reconhecido → 'desconhecido'.
 */
function normalizeTipoArvoreToEnum(raw) {
  const s = clean(raw);
  if (!s) return null;

  const v = s.toLowerCase();

  // plantada
  if (/(^|\W)plantad/.test(v) || /(muda|replant)/.test(v)) return "plantada";

  // regenerando (regeneração natural / rebrota / brotação / espontânea)
  if (/(regener|natural|espont|rebrota|brota[cç][aã]o)/.test(v)) return "regenerando";

  // presente_antes (preexistente / remanescente / anterior / existente)
  if (/(presente\s*antes|preexist|remanesc|anterior|existente)/.test(v)) return "presente_antes";

  // desconhecido / não informado
  if (/(desconhec|nao\s*inform|não\s*inform|n[ãa]o\s*inf)/.test(v)) return "desconhecido";

  // termos avulsos → melhor fallback seguro
  if (/(nativa|invasor|ex[oó]tic)/.test(v)) return "presente_antes";

  return "desconhecido";
}

// ================== Extractors ==================
function extractCommonFields(row) {
  const tamanhoParcela = clean(
    getVal(row, [
      "Tamanho_parcela",
      "Tamanho da parcela",
      "Tipo de Parcela (30x30/3x3)",
      "Tamanho da Parcela",
    ])
  );

  // Y0 costuma usar "Parcela"
  const idParcela = clean(
    getVal(row, [
      "Parcela", // <- principal no Y0
      "ID da Parcela",
      "ID Parcela",
      "Parcela_ID",
      "Identificação (ID) da Parcela de Monitoramento de Árvores",
      "Identificação da Parcela",
    ])
  );

  const idSubparcela = clean(
    getVal(row, ["ID Subparcela", "Subparcela_ID", "Identificação da Subparcela"])
  );

  // Y0 costuma usar "Nome_Científico"
  const especieCientifico = clean(
    getVal(row, [
      "Nome_Científico", // <- principal no Y0
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
    getVal(row, ["Nome comum", "Nome_popular", "Nome popular", "Popular", "Comum"])
  );

  // Tipo de árvore → ENUM
  const tipoArvore = normalizeTipoArvoreToEnum(
    getVal(row, [
      "Arvore_Tipo",
      "Árvore_Tipo",
      "Tipo_Arvore",
      "Tipo_Árvore",
      "Tipo da árvore",
      "Tipo de árvore",
      "Tipo da Arvore",
      "Tipo de Arvore",
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

  const dap_cm =
    toFloat(getVal(row, ["DAP (diam)", "DAP cm", "DAP", "Diametro à altura do peito (cm)"])) ??
    toFloat(getVal(row, ["DAP_cm", "DAP (cm)"]));

  const numeroArvore = toInt(
    getVal(row, [
      "Número da árvore",
      "Numero da arvore",
      "Número_Árvore",
      "Arvore_N",
      "Árvore N",
      "Tree #",
    ])
  );
  const numeroFuste = toInt(
    getVal(row, ["Número de fuste", "Numero de fuste", "Fuste_N", "Número_Fuste"])
  );

  return {
    tamanhoParcela,
    idParcela,
    idSubparcela,
    especieCientifico,
    especiePopular,
    tipoArvore, // ENUM ou null
    quantidade,
    dap_cm,
    numeroArvore,
    numeroFuste,
  };
}

function classifyRowType(f) {
  const tp = (f.tamanhoParcela || "").replace(/\s/g, "").toLowerCase();
  const hasDap = f.dap_cm !== null && f.dap_cm !== undefined;
  if (hasDap) return "DAP_INDIVIDUAL";
  if (tp.includes("30x30") || tp.includes("30×30")) return "PARCELA_30x30";
  if (tp.includes("3x3") || tp.includes("3×3")) return "SUBPARCELA_3x3";
  if (f.idSubparcela) return "SUBPARCELA_3x3";
  return "PARCELA_30x30";
}

// ================== Lookups ==================
async function getOrCreateEspecie({ cientifico, popular }, { transaction } = {}) {
  const sci = clean(cientifico);
  const pop = clean(popular);

  if (sci) {
    const found = await Especie.findOne({
      where: Sequelize.where(
        Sequelize.fn("lower", Sequelize.col("nome_cientifico")),
        sci.toLowerCase()
      ),
      transaction,
    });
    if (found) return found;

    return await Especie.create(
      { nome_cientifico: sci, nome: pop || null },
      { transaction }
    );
  }

  if (pop) {
    const found = await Especie.findOne({
      where: Sequelize.where(Sequelize.fn("lower", Sequelize.col("nome")), pop.toLowerCase()),
      transaction,
    });
    if (found) return found;

    return await Especie.create({ nome_cientifico: null, nome: pop }, { transaction });
  }

  const unk = await Especie.findOne({
    where: { nome_cientifico: null, nome: "Desconhecida" },
    transaction,
  });
  if (unk) return unk;

  return await Especie.create({ nome_cientifico: null, nome: "Desconhecida" }, { transaction });
}

async function getParcelaByExternalId(idParcela, { transaction } = {}) {
  const opts = variantsForIdParcela(idParcela, 2);
  if (!opts.length) return null;
  return await ParcelaMonitoramento.findOne({ where: { idParcela: { [Op.in]: opts } }, transaction });
}

async function getSubparcela({ parcelaId, idSubparcela }, { transaction } = {}) {
  if (idSubparcela) {
    const found = await SubparcelaMonitoramento.findOne({
      where: { parcelaId, idSubparcela: { [Op.iLike]: idSubparcela } },
      transaction,
    });
    if (found) return found;
  }
  return await SubparcelaMonitoramento.findOne({ where: { parcelaId }, transaction });
}

// ================== Recompute embutido (usando a instância importada) ==================
async function recomputeY0WithoutModelChanges(sequelize) {
  // Usamos os models importados no topo do arquivo:
  // - Arvore (>=10 cm)
  // - Y0DatabaseArvore (tabela de agregados)
  // Para <10 cm, usamos SQL cru (não depende de associate).

  // 1) Totais >=10 cm por parcela (ORM)
  const gte10 = await Arvore.findAll({
    attributes: ["parcelaId", [sequelize.fn("COUNT", sequelize.col("id")), "cnt"]],
    group: ["parcelaId"],
    raw: true,
  });
  const mapGTE = new Map(gte10.map((r) => [Number(r.parcelaId), Number(r.cnt)]));

  // 2) Totais <10 cm por parcela (RAW SQL → não depende de associação)
  const [lt10] = await sequelize.query(`
    SELECT sp.parcela_id AS "parcelaId",
           COALESCE(SUM(sa.numero_arvores_especie), 0) AS "sum"
    FROM kb_subparcela_arvore sa
    JOIN kb_subparcela sp ON sp.id = sa.subparcela_id
    GROUP BY sp.parcela_id
  `);
  const mapLT = new Map(lt10.map((r) => [Number(r.parcelaId), Number(r.sum) || 0]));

  // 3) Universo e upsert manual usando a instância importada de Y0DatabaseArvore
  const parcelas = new Set([...mapGTE.keys(), ...mapLT.keys()]);

  await sequelize.transaction(async (t) => {
    for (const parcelaId of parcelas) {
      const totalArvoresGTE10 = mapGTE.get(parcelaId) || 0;
      const totalArvoresLT10 = mapLT.get(parcelaId) || 0;
      const totalGeral = totalArvoresGTE10 + totalArvoresLT10;

      const existing = await Y0DatabaseArvore.findOne({ where: { parcelaId }, transaction: t });

      if (existing) {
        await existing.update(
          { totalArvoresGTE10, totalArvoresLT10, totalGeral },
          { transaction: t }
        );
      } else {
        await Y0DatabaseArvore.create(
          { parcelaId, totalArvoresGTE10, totalArvoresLT10, totalGeral },
          { transaction: t }
        );
      }
    }
  });
}


// ================== Import principal ==================
export async function kb_importY0_Database(rows) {
  if (!Array.isArray(rows) || rows.length === 0) {
    return { inserted: 0, updated: 0, skipped: 0 };
  }

  let inserted = 0,
    updated = 0,
    skipped = 0;

  await ParcelaMonitoramento.sequelize.transaction(async (t) => {
    for (const raw of rows) {
      try {
        const f = extractCommonFields(raw);
        const tipo = classifyRowType(f);

        // localizar parcela criada na aba PPC/PACTO
        const parcela = await getParcelaByExternalId(f.idParcela, { transaction: t });
        if (!parcela) {
          skipped++;
          console.warn(`[Y0] Parcela não encontrado para idParcela='${f.idParcela}'. Linha ignorada.`);
          continue;
        }

        if (tipo === "PARCELA_30x30") {
          // Contagem por espécie (30x30)
          const especie = await getOrCreateEspecie(
            { cientifico: f.especieCientifico, popular: f.especiePopular },
            { transaction: t }
          );

          const [rec, created] = await ArvorePlantadaDAP10.findOrCreate({
            where: { parcelaId: parcela.id, especieId: especie.id },
            defaults: {
              parcelaId: parcela.id,
              especieId: especie.id,
              numeroArvores: f.quantidade ?? 0,
              ...(f.tipoArvore ? { tipoArvore: f.tipoArvore } : {}),
            },
            transaction: t,
          });

          if (!created) {
            const prevNum = rec.get("numeroArvores") ?? 0;
            const nextNum = f.quantidade ?? prevNum;

            const patch = {};
            if (nextNum !== prevNum) patch.numeroArvores = nextNum;

            const prevTipo = rec.get("tipoArvore") ?? null;
            if (f.tipoArvore && f.tipoArvore !== prevTipo) patch.tipoArvore = f.tipoArvore;

            if (Object.keys(patch).length) {
              await rec.update(patch, { transaction: t });
              updated++;
            } else {
              skipped++;
            }
          } else {
            inserted++;
          }
        } else if (tipo === "SUBPARCELA_3x3") {
          // Contagem por espécie (3x3)
          const sub = await getSubparcela({ parcelaId: parcela.id, idSubparcela: f.idSubparcela }, { transaction: t });
          if (!sub) {
            skipped++;
            console.warn(
              `[Y0] Subparcela não encontrada. parcela='${f.idParcela}', idSubparcela='${f.idSubparcela || "(não informado)"}'.`
            );
            continue;
          }

          const especie = await getOrCreateEspecie(
            { cientifico: f.especieCientifico, popular: f.especiePopular },
            { transaction: t }
          );

          const [rec, created] = await SubparcelaArvore.findOrCreate({
            where: { subparcelaId: sub.id, especieId: especie.id },
            defaults: {
              subparcelaId: sub.id,
              especieId: especie.id,
              numeroArvoresEspecie: f.quantidade ?? 0,
              ...(f.tipoArvore ? { tipoArvore: f.tipoArvore } : {}),
            },
            transaction: t,
          });

          if (!created) {
            const prevNum = rec.get("numeroArvoresEspecie") ?? 0;
            const nextNum = f.quantidade ?? prevNum;

            const patch = {};
            if (nextNum !== prevNum) patch.numeroArvoresEspecie = nextNum;

            const prevTipo = rec.get("tipoArvore") ?? null;
            if (f.tipoArvore && f.tipoArvore !== prevTipo) patch.tipoArvore = f.tipoArvore;

            if (Object.keys(patch).length) {
              await rec.update(patch, { transaction: t });
              updated++;
            } else {
              skipped++;
            }
          } else {
            inserted++;
          }
        } else if (tipo === "DAP_INDIVIDUAL") {
          // Árvore individual (>10cm)
          const especie = await getOrCreateEspecie(
            { cientifico: f.especieCientifico, popular: f.especiePopular },
            { transaction: t }
          );

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
              ...(f.tipoArvore ? { tipoArvore: f.tipoArvore } : {}),
            },
            transaction: t,
          });

          if (!created) {
            const prevTipo = rec.get("tipoArvore") ?? null;
            if (f.tipoArvore && f.tipoArvore !== prevTipo) {
              await rec.update({ tipoArvore: f.tipoArvore }, { transaction: t });
              updated++;
            } else {
              skipped++;
            }
          } else {
            inserted++;
          }
        } else {
          skipped++;
          console.warn(
            `[Y0] Tipo de linha não reconhecido. idParcela='${f.idParcela}', tamanho='${f.tamanhoParcela}'.`
          );
        }
      } catch (err) {
        skipped++;
        console.error("[Y0] Erro ao processar linha:", err?.message || err);
      }
    }
  });

  // ======= Recompute KB_Y0_DATABASE_ARVORE (fora da transação acima) =======
  try {
    await recomputeY0WithoutModelChanges(ParcelaMonitoramento.sequelize);
    console.log("Y0_Database → agregados recalculados (kb_y0_database_arvore).");
  } catch (e) {
    console.warn("Y0_Database → falha ao recomputar agregados:", e?.message || e);
  }

  return { inserted, updated, skipped };
}
