// kb_coordPACTOImporter.js
// Importador da aba "Coord_PACTO" -> tabela kb_coordenadas_pacto
// - Usa o model CoordenadasPacto (kb_coordenadas_pacto)
// - Match implícito da parcela por idParcela (normalizado); se não achar, parcelaId = null
// - DEDUP: evita inserir duplicatas (parcelaId/plotId/vertice + X/Y)

import { Op } from "sequelize";
import CoordenadasPacto from "../models/kobo/coordenadas-pacto.model.js";
import ParcelaMonitoramento from "../models/kobo/parcela-monitoramento.model.js";

// ---------------- Utils -----------------
const clean = (v) => (v === undefined || v === null ? null : String(v).trim() || null);

const toFloat = (v) => {
  if (v === undefined || v === null || v === "") return null;
  const n = Number(String(v).replace(",", "."));
  return Number.isFinite(n) ? n : null;
};

const toInt = (v) => {
  if (v === undefined || v === null || v === "") return null;
  const n = parseInt(String(v), 10);
  return Number.isFinite(n) ? n : null;
};

// pega o primeiro valor dentre várias chaves possíveis (normalizadas e originais)
function getVal(row, keys = []) {
  for (const k of keys) {
    if (row[k] !== undefined && row[k] !== null && row[k] !== "") return row[k];
  }
  return null;
}

// normaliza rótulos de parcela vindos de planilha, removendo sufixos comuns
function normalizeParcelaLabel(label) {
  if (!label) return null;
  let s = String(label).trim();
  s = s.replace(/\s+/g, " ").trim();
  // remove tamanhos/sufixos: 30x30, 3x3, 4x25 e -Vn
  s = s.replace(/\b30\s*x\s*30\b/gi, "");
  s = s.replace(/\b3\s*x\s*3\b/gi, "");
  s = s.replace(/\b4\s*x\s*25\b/gi, "");
  s = s.replace(/-?v\s*\d+$/i, "");
  // normaliza separadores
  s = s.replace(/\s*-\s*/g, "-").replace(/\s+/g, " ").trim();
  return s;
}

// tenta resolver a parcela por idParcela (campo canônico/único no seu model)
async function findParcelaByLabel(label) {
  if (!label) return null;
  const norm = normalizeParcelaLabel(label);
  if (!norm) return null;

  let parcela = await ParcelaMonitoramento.findOne({
    where: { idParcela: { [Op.iLike]: norm } },
  });
  if (parcela) return parcela;

  parcela = await ParcelaMonitoramento.findOne({
    where: {
      [Op.or]: [
        { idParcela: { [Op.iLike]: `${norm}%` } },
        { idParcela: { [Op.iLike]: `%${norm}` } },
      ],
    },
  });
  return parcela;
}

const round2 = (n) => (n == null ? null : Math.round(Number(n) * 100) / 100);

// monta condição "campo = valor" OU "campo IS NULL" quando valor é null
const fieldEq = (field, value) =>
  value == null ? { [field]: { [Op.is]: null } } : { [field]: value };

/**
 * Regra de duplicidade para Coord_PACTO:
 * - Mesmo parcelaId (ou ambos null)
 * - e mesma plotId (ou ambos null)
 * - e mesmo vertice (ou ambos null)
 * - e mesmas coordenadas UTM X/Y (com 2 casas, compatível com DECIMAL(10,2))
 */
async function findDuplicatePacto({ parcelaId, plotId, vertice, x, y }) {
  return CoordenadasPacto.findOne({
    where: {
      [Op.and]: [
        parcelaId == null ? { parcelaId: { [Op.is]: null } } : { parcelaId },
        fieldEq("plotId", plotId),
        fieldEq("vertice", vertice),
        fieldEq("x_sirgas2000_utm23s", x),
        fieldEq("y_sirgas2000_utm23s", y),
      ],
    },
  });
}

// -------------- Importador ---------------
/**
 * Importa linhas da aba Coord_PACTO.
 * - Se "Vértices PACTO" contiver múltiplos valores (ex.: "1;2;3;4"), cria um registro por vértice.
 * @param {Array<Object>} rows - linhas já normalizadas (mas tolera cabeçalhos originais)
 * @returns {Promise<{inserted:number, skippedDuplicates:number, errors:number, unresolved:number}>}
 */
export async function kb_importCoord_PACTO(rows) {
  console.log(`\n▶ Importando Coord_PACTO… total de linhas: ${rows.length}`);

  let inserted = 0;
  let skippedDuplicates = 0;
  let errors = 0;
  const unresolvedLabels = new Set();

  for (let i = 0; i < rows.length; i++) {
    const r = rows[i];
    try {
      const parcelaLabel = clean(getVal(r, ["parcela", "Parcela"])) || null;
      const plotId = clean(getVal(r, ["plot_id", "Plot ID"])) || null;

      // pode vir "1" ou "1;2;3;4" etc.
      const verticesText = clean(getVal(r, ["vertices_pacto", "Vértices PACTO"])) || null;
      const vertices = verticesText
        ? verticesText
            .split(/[,;\s]+/)
            .map((v) => toInt(v))
            .filter((n) => Number.isFinite(n) && n >= 1 && n <= 4)
        : [null];

      // UTM 23S (SIRGAS 2000)
      const xUtm = round2(
        toFloat(
          getVal(r, [
            "x_-_latitude_(sirgas_2000_utm_23s)",
            "x - latitude (sirgas 2000 utm 23s)",
            "X - Latitude (SIRGAS 2000 UTM 23S)",
            "x_sirgas2000_utm23s",
          ])
        )
      );
      const yUtm = round2(
        toFloat(
          getVal(r, [
            "y_-_longitude_(sirgas_2000_utm_23s)",
            "y - longitude (sirgas 2000 utm 23s)",
            "Y - Longitude (SIRGAS 2000 UTM 23S)",
            "y_sirgas2000_utm23s",
          ])
        )
      );

      const notes = clean(getVal(r, ["notes_on_pacto", "Notes on PACTO"])) || null;

      // resolve parcela
      let parcelaId = null;
      if (parcelaLabel) {
        const parcela = await findParcelaByLabel(parcelaLabel);
        parcelaId = parcela?.id ?? null;
        if (!parcelaId) unresolvedLabels.add(parcelaLabel);
      }

      // explode por vértice
      for (const v of vertices) {
        // DEDUP
        const dup = await findDuplicatePacto({
          parcelaId,
          plotId,
          vertice: v,
          x: xUtm,
          y: yUtm,
        });
        if (dup) {
          skippedDuplicates++;
          continue;
        }

        await CoordenadasPacto.create({
          parcelaId, // pode ser null; reconciliação posterior preenche
          plotId,
          vertice: v,
          x_sirgas2000_utm23s: xUtm,
          y_sirgas2000_utm23s: yUtm,
          notes,
        });
        inserted++;
      }
    } catch (err) {
      errors++;
      console.error(`❌ Coord_PACTO erro na linha ${i + 1}:`, err?.message, r);
    }
  }

  const unresolved = unresolvedLabels.size;
  if (unresolved) {
    const sample = Array.from(unresolvedLabels).slice(0, 10).join(", ");
    console.warn(`⚠️ Coord_PACTO: ${unresolved} rótulo(s) sem match de parcela. Ex.: ${sample}`);
  }

  console.log(
    `✅ Coord_PACTO concluído. inserted=${inserted}, skippedDuplicates=${skippedDuplicates}, errors=${errors}, unresolved=${unresolved}`
  );
  return { inserted, skippedDuplicates, errors, unresolved };
}

// Sugestões de robustez no banco:
// - Índice único opcional para reforçar a dedup (avalie com cuidado):
//   CREATE UNIQUE INDEX uniq_kb_coordenadas_pacto
//   ON kb_coordenadas_pacto (COALESCE(parcela_id, 0), COALESCE(plot_id, ''), COALESCE(vertice, 0), x_sirgas2000_utm23s, y_sirgas2000_utm23s);
