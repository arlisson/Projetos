// kb_coordPPCImporter.js
// Importador da aba "Coord_PPC" (linhas -> tabela kb_coordenadas_ppc)
// - Match implícito por idParcela normalizado
// - Date parsing robusto
// - DEDUP: evita inserir coordenadas já existentes (ver regra abaixo)

import { Op, where, fn, col, literal } from "sequelize";
import CoordenadasPPC from "../models/kobo/coordenadas-ppc.model.js";
import ParcelaMonitoramento from "../models/kobo/parcela-monitoramento.model.js";

// ---------------- Utils -----------------
const clean = (v) => (v === undefined || v === null ? null : String(v).trim() || null);
const toFloat = (v) => {
  if (v === undefined || v === null || v === "") return null;
  const n = Number(String(v).replace(",", "."));
  return Number.isFinite(n) ? n : null;
};
const round6 = (n) => (n == null ? null : Math.round(Number(n) * 1e6) / 1e6);

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
  // remove tamanhos/sufixos: 30x30, 3x3, 4x25 (variações com espaços) e -Vn
  s = s.replace(/\b30\s*x\s*30\b/gi, "");
  s = s.replace(/\b3\s*x\s*3\b/gi, "");
  s = s.replace(/\b4\s*x\s*25\b/gi, "");
  s = s.replace(/-?v\s*\d+$/i, "");
  s = s.replace(/\s*-\s*/g, "-").replace(/\s+/g, " ").trim();
  return s;
}

// converte número serial do Excel (dias desde 1899-12-30) para Date
function excelSerialToDate(n) {
  const ms = (n - 25569) * 86400000;
  const d = new Date(ms);
  return isNaN(d.getTime()) ? null : d;
}

// parse flexível para "Data e Hora"
function parseDateFlexible(value) {
  const s = clean(value);
  if (!s || s === "-" || /^0+$/.test(s)) return null;

  const maybeNum = Number(s);
  if (Number.isFinite(maybeNum) && maybeNum > 20000 && maybeNum < 90000) {
    const d = excelSerialToDate(maybeNum);
    if (d) return d;
  }

  let d = new Date(s);
  if (!isNaN(d.getTime())) return d;

  d = new Date(s.replace(" ", "T"));
  if (!isNaN(d.getTime())) return d;

  const m = s.match(
    /^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})(?:[ T](\d{1,2}):(\d{2})(?::(\d{2})(?:\.(\d{1,3}))?)?)?$/
  );
  if (m) {
    const [, dd, mm, yyyy, HH = "0", MM = "0", SS = "0", ms = "0"] = m;
    const iso = `${yyyy}-${mm.padStart(2, "0")}-${dd.padStart(
      2,
      "0"
    )}T${HH.padStart(2, "0")}:${MM.padStart(2, "0")}:${SS.padStart(2, "0")}.${ms.padStart(3, "0")}Z`;
    d = new Date(iso);
    if (!isNaN(d.getTime())) return d;
  }

  const m2 = s.match(
    /^(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})(?:[ T](\d{1,2}):(\d{2})(?::(\d{2})(?:\.(\d{1,3}))?)?)?$/
  );
  if (m2) {
    const [, yyyy, mm, dd, HH = "0", MM = "0", SS = "0", ms = "0"] = m2;
    const iso = `${yyyy}-${mm.padStart(2, "0")}-${dd.padStart(
      2,
      "0"
    )}T${HH.padStart(2, "0")}:${MM.padStart(2, "0")}:${SS.padStart(2, "0")}.${ms.padStart(3, "0")}Z`;
    d = new Date(iso);
    if (!isNaN(d.getTime())) return d;
  }

  return null;
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

// monta condição "campo = valor" OU "campo IS NULL" quando valor é null
const fieldEq = (field, value) =>
  value == null ? { [field]: { [Op.is]: null } } : { [field]: value };

/**
 * Encontra um registro existente que seja "igual" segundo a regra de duplicidade:
 * - Mesmo parcelaId (ou ambos null)
 * - e (mesma dupla WGS84 ou mesma dupla SIRGAS/UTM)
 * - e mesma dataHora (ou ambas null)
 */
async function findDuplicateCoord({ parcelaId, latWgs, lonWgs, latSirgas, lonSirgas, dataHora }) {
  // normaliza para reduzir ruído de double
  const nLatWgs = round6(latWgs);
  const nLonWgs = round6(lonWgs);
  const nLatSir = round6(latSirgas);
  const nLonSir = round6(lonSirgas);

  const andParcela = parcelaId == null ? { parcelaId: { [Op.is]: null } } : { parcelaId };

  const andDate =
    dataHora == null
      ? { dataHora: { [Op.is]: null } }
      : { dataHora }; // se quiser tolerância por minuto, precisaria usar BETWEEN

  // Conjunto 1: casa por WGS84
  const byWgs = {
    ...fieldEq("latitudeWGS84", nLatWgs),
    ...fieldEq("longitudeWGS84", nLonWgs),
  };

  // Conjunto 2: casa por SIRGAS/UTM
  const bySirgas = {
    ...fieldEq("x_sirgas2000_utm23s", nLatSir),
    ...fieldEq("y_sirgas2000_utm23s", nLonSir),
  };

  return CoordenadasPPC.findOne({
    where: {
      [Op.and]: [
        andParcela,
        andDate,
        {
          [Op.or]: [
            // se ambos de WGS vieram null, este ramo não ajuda; mas o OR cobre Sirgas
            byWgs,
            bySirgas,
          ],
        },
      ],
    },
  });
}

// -------------- Importador ---------------
/**
 * Importa linhas da aba Coord_PPC.
 * @param {Array<Object>} rows - linhas já normalizadas por normalizeKeys (mas tolera cabeçalhos originais)
 * @returns {Promise<{inserted:number, errors:number, unresolved:number, skippedDuplicates:number}>}
 */
export async function kb_importCoord_PPC(rows) {
  console.log(`\n▶ Importando Coord_PPC… total de linhas: ${rows.length}`);

  let inserted = 0;
  let skippedDuplicates = 0;
  let errors = 0;
  const unresolvedLabels = new Set();

  for (let i = 0; i < rows.length; i++) {
    const r = rows[i];
    try {
      const label = clean(getVal(r, ["parcela", "Parcela"]));

      // WGS84
      const latWgs = toFloat(
        getVal(r, ["latitude_wgs_84", "latitude_wgs84", "latitude (wgs 84)", "Latitude (WGS 84)"])
      );
      const lonWgs = toFloat(
        getVal(r, ["longitude_wgs_84", "longitude_wgs84", "longitude (wgs 84)", "Longitude (WGS 84)"])
      );

      // SIRGAS/UTM
      const latSirgas = toFloat(
        getVal(r, [
          "latitude_sirgas_2000",
          "latitude (sirgas 2000)",
          "Latitude (SIRGAS 2000)",
          "x - latitude (sirgas 2000 utm 23s)",
          "x_sirgas2000_utm23s",
        ])
      );
      const lonSirgas = toFloat(
        getVal(r, [
          "longitude_sirgas_2000",
          "longitude (sirgas 2000)",
          "Longitude (SIRGAS 2000)",
          "y - longitude (sirgas 2000 utm 23s)",
          "y_sirgas2000_utm23s",
        ])
      );

      const elev = toFloat(getVal(r, ["elevacao", "elevacao_m", "elevação", "Elevação"]));
      const dataHora = parseDateFlexible(
        getVal(r, ["data_e_hora", "data_hora", "datahora", "Data e Hora"])
      );

      // resolve parcela
      let parcelaId = null;
      if (label) {
        const parcela = await findParcelaByLabel(label);
        parcelaId = parcela?.id ?? null;
        if (!parcelaId) unresolvedLabels.add(label);
      }

      // DEDUP: não insere se já existir (regra descrita acima)
      const dup = await findDuplicateCoord({
        parcelaId,
        latWgs: round6(latWgs),
        lonWgs: round6(lonWgs),
        latSirgas: round6(latSirgas),
        lonSirgas: round6(lonSirgas),
        dataHora,
      });
      if (dup) {
        skippedDuplicates++;
        continue;
      }

      // gravação (append-only)
      await CoordenadasPPC.create({
        parcelaId,
        latitudeWGS84: round6(latWgs),
        longitudeWGS84: round6(lonWgs),
        x_sirgas2000_utm23s: round6(latSirgas),
        y_sirgas2000_utm23s: round6(lonSirgas),
        elevacao: elev,
        dataHora,
      });

      inserted++;
    } catch (err) {
      errors++;
      console.error(`❌ Coord_PPC erro na linha ${i + 1}:`, err?.message, r);
    }
  }

  const unresolved = unresolvedLabels.size;
  if (unresolved) {
    const sample = Array.from(unresolvedLabels).slice(0, 10).join(", ");
    console.warn(`⚠️ Coord_PPC: ${unresolved} rótulo(s) sem match de parcela. Ex.: ${sample}`);
  }

  console.log(
    `✅ Coord_PPC concluído. inserted=${inserted}, skippedDuplicates=${skippedDuplicates}, errors=${errors}, unresolved=${unresolved}`
  );
  return { inserted, skippedDuplicates, errors, unresolved };
}

// Sugestões de robustez no banco:
// 1) Criar índice único opcional para reforçar a regra de duplicidade (se fizer sentido no seu caso):
//    CREATE UNIQUE INDEX uniq_kb_coordenadas_ppc
//    ON kb_coordenadas_ppc (COALESCE(parcela_id, 0), data_hora, latitude_wgs84, longitude_wgs84, x_sirgas2000_utm23s, y_sirgas2000_utm23s);
//    (ajuste nomes das colunas conforme o schema real)
// 2) Se quiser tolerância temporal (ex.: ~1 minuto), troque a comparação exata de data_hora por uma janela (BETWEEN) no findDuplicateCoord.
