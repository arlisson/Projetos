// importers/kb_import3x3SubplotRepeat.js
import sequelize from "#config/postgres.config.js";
import models from "#models/kobo/index.js";
import { Op } from "sequelize";
import Especie from "#models/catalogo/especie.model.js";
import { getOrCreateEspecieId } from "../utils/especieHelper.js";
import { getParcelaBySubmission } from "../utils/importMap.js";

/**
 * Importa "3x3_Subplot_Repeat" → SubparcelaMonitoramento + SubparcelaArvore (contagem por espécie)
 * Regras:
 *  - Parcela: idParcela → cache(_submission__uuid/_id) → UUID v4 banco
 *  - Subparcela: ID informado OU "SP-{_index}"
 *  - Sem lat/lon: cria subparcela com (0,0) e descrição "SEM COORDENADA (import automático)"
 *  - Espécie: resolve por helper; fallback "desconhecida"
 *  - Upsert em SubparcelaArvore por (subparcelaId, especieId, tipoArvore)
 */
export async function kb_import3x3SubplotRepeat(rows = []) {
  const {
    Monitoramento,
    ParcelaMonitoramento,
    SubparcelaMonitoramento,
    SubparcelaArvore,
  } = models;

  let insertedSubparcelas = 0;
  let updatedSubparcelas = 0;
  let insertedArvores = 0;
  let updatedArvores = 0;
  let unresolvedParcela = 0;
  let skippedSemIdSub = 0;
  let errors = 0;

  // helpers
  const nonEmpty = (v) => v !== undefined && v !== null && String(v).trim() !== "";
  const clean = (v) => (nonEmpty(v) ? String(v).trim() : null);
  const pick = (row, keys) => {
    for (const k of keys) {
      if (Object.prototype.hasOwnProperty.call(row, k) && nonEmpty(row[k])) return row[k];
    }
    return null;
  };
  const toNumber = (v) => {
    if (v == null || String(v).trim() === "") return null;
    const n = Number(String(v).replace(",", "."));
    return Number.isFinite(n) ? n : null;
  };
  const toIntPos = (v) => {
    const n = toNumber(v);
    return Number.isFinite(n) && n > 0 ? Math.trunc(n) : null;
  };
  const toBoolFallbackFalse = (v) => {
    if (v == null || String(v).trim() === "") return false;
    const s = String(v).trim().toLowerCase();
    return s.startsWith("s") || s === "true" || s === "1";
  };
  const normalizeTipoArvore = (raw) => {
    const s = clean(raw)?.toLowerCase() || "";
    if (s.includes("plant")) return "plantada";
    if (s.includes("regen") || s.includes("natural")) return "regenerando";
    if (s.includes("antes") || s.includes("preexist")) return "presente_antes";
    return "desconhecido";
  };

  // possíveis nomes
  const parcelaIdKeys = [
    "Identificação (ID) da Parcela de Monitoramento de Árvores",
    "Identificação da Parcela de Monitoramento de Árvores",
    "Identificação da Parcela",
    "ID da Parcela",
    "id_parcela",
    "plot_id",
    "Plot ID",
    "plotID",
  ];
  const submissionUUIDKeys = [
    "_submission__uuid", "_uuid", "submission__uuid", "uuid",
    "instanceID", "instance_id",
    "_submission__id", "_id",
  ];
  const subparcelaIdKeys = [
    "ID da Subparcela (3m x 3m)",
    "ID da Subparcela",
    "Identificação da Subparcela",
    "id_subparcela",
    "subplot_id",
  ];
  const indexKeys = ["_index", "index", "__index"];

  const latKeys  = ["_Centróide da subparcela de 3m x 3m_latitude", "Centróide da subparcela de 3m x 3m_latitude", "centroide_latitude", "centróide_latitude", "subplot_centroid_lat"];
  const lonKeys  = ["_Centróide da subparcela de 3m x 3m_longitude", "Centróide da subparcela de 3m x 3m_longitude", "centroide_longitude", "centróide_longitude", "subplot_centroid_lon"];
  const altKeys  = ["_Centróide da subparcela de 3m x 3m_altitude", "Centróide da subparcela de 3m x 3m_altitude", "centroide_altitude", "centróide_altitude", "subplot_centroid_alt"];
  const precKeys = ["_Centróide da subparcela de 3m x 3m_precision", "Centróide da subparcela de 3m x 3m_precision", "centroide_precision", "centróide_precision", "subplot_centroid_precision"];

  const fotoUrlKeys = ["Foto da subparcela 3mx3m_URL", "foto_subparcela_url", "subplot_photo_url"];
  const descLocalKeys = [
    "Descrição da localização da subparcela (3mx3m) dentro da parcela maior (30mx30m)",
    "descricao_localizacao_subparcela",
    "subplot_location_desc",
  ];
  const numAmostragensKeys = [
    "**Número de amostragens necessárias para a parcela de 3m x 3m**",
    "numero_amostragens_subparcela",
    "subplot_samples_required",
  ];
  const arvores19Keys = [
    "**Existem árvores de 1-9,9cm DAP na parcela de 3m x 3m?**",
    "arvores_1_9_presentes",
    "trees_1_9_present",
  ];

  const speciesKeys = [
    "Espécies de árvores (use nome científico)",
    "Espécies",
    "Espécie",
    "species",
  ];
  const countKeys = [
    "Número de Árvores desta Espécie",
    "quantidade",
    "numero_arvores",
    "count",
  ];
  const tipoKeys = ["Tipo de Árvore", "tipo_arvore", "tipo"];

  async function resolveParcelaId(row) {
    // A) idParcela direto
    const idParcelaRaw = pick(row, parcelaIdKeys);
    if (idParcelaRaw) {
      const parcela = await ParcelaMonitoramento.findOne({
        where: { idParcela: String(idParcelaRaw).trim() },
        attributes: ["id"],
        raw: true,
      });
      if (parcela?.id) return parcela.id;
    }

    // B) cache por submissionKey
    const subKeyRaw = pick(row, submissionUUIDKeys);
    if (subKeyRaw) {
      const fromCache = getParcelaBySubmission(subKeyRaw);
      if (fromCache) return fromCache;
    }

    // C) UUID v4 → Monitoramento → Parcela
    if (subKeyRaw) {
      const uuid = String(subKeyRaw).trim().toLowerCase();
      const UUID_V4_RX = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
      if (UUID_V4_RX.test(uuid)) {
        const mon = await Monitoramento.findOne({ where: { uuid }, attributes: ["id"], raw: true });
        if (mon?.id) {
          const parcela = await ParcelaMonitoramento.findOne({
            where: { monitoramentoId: mon.id },
            attributes: ["id"],
            raw: true,
          });
          if (parcela?.id) return parcela.id;
        }
      }
    }

    return null;
  }

  function buildSubparcelaDefaults(row, hasLatLon) {
    const lat = toNumber(pick(row, latKeys));
    const lon = toNumber(pick(row, lonKeys));
    const alt = toNumber(pick(row, altKeys));
    const prc = toNumber(pick(row, precKeys));

    // quando não houver lat/lon, criamos com (0,0) e marcamos na descrição
    const base = {
      centroideLatitude:  hasLatLon ? lat : 0,
      centroideLongitude: hasLatLon ? lon : 0,
      centroideAltitude:  hasLatLon ? alt : null,
      centroidePrecisao:  hasLatLon ? prc : null,
      fotoUrl:             clean(pick(row, fotoUrlKeys)),
      descricaoLocalizacao: clean(pick(row, descLocalKeys)) || (hasLatLon ? null : "SEM COORDENADA (import automático)"),
      numeroAmostragens:   toNumber(pick(row, numAmostragensKeys)),
      arvoresDAP_1_9_Presentes: toBoolFallbackFalse(pick(row, arvores19Keys)),
    };

    return base;
  }

  const t = await sequelize.transaction();
  try {
    for (const [i, row] of rows.entries()) {
      try {
        const parcelaId = await resolveParcelaId(row);
        if (!parcelaId) { unresolvedParcela++; continue; }

        const idSubRaw = clean(pick(row, subparcelaIdKeys));
        const idxRaw   = clean(pick(row, indexKeys));
        const idSubparcela = idSubRaw || (idxRaw ? `SP-${idxRaw}` : null);
        if (!idSubparcela) { skippedSemIdSub++; continue; }

        // checa se há lat/lon
        const lat = toNumber(pick(row, latKeys));
        const lon = toNumber(pick(row, lonKeys));
        const hasLatLon = Number.isFinite(lat) && Number.isFinite(lon);

        const subDefaults = buildSubparcelaDefaults(row, hasLatLon);

        // upsert da SUBPARCELA (com (0,0) quando faltar lat/lon)
        const [sub, createdSub] = await SubparcelaMonitoramento.findOrCreate({
          where: { idSubparcela, parcelaId },
          defaults: { idSubparcela, parcelaId, ...subDefaults },
          transaction: t,
        });

        if (createdSub) {
          insertedSubparcelas++;
        } else {
          await SubparcelaMonitoramento.update(subDefaults, {
            where: { id: sub.id },
            transaction: t,
          });
          updatedSubparcelas++;
        }

        // árvores (contagem por espécie)
        const especieRaw = clean(pick(row, speciesKeys));
        const tipoArvore = normalizeTipoArvore(pick(row, tipoKeys));
        const qt = toIntPos(pick(row, countKeys));
        if (!qt) continue; // sem quantidade válida, nada a fazer

        // resolve/cria espécie (fallback "desconhecida")
        let especieId = await getOrCreateEspecieId(especieRaw, { transaction: t });
        if (!especieId) {
          const ex = await Especie.findOne({
            where: { nome: { [Op.iLike]: "desconhecida" } },
            attributes: ["id"],
            raw: true,
            transaction: t,
          });
          if (ex?.id) especieId = ex.id;
          else {
            const created = await Especie.create(
              { nome: "desconhecida", nome_cientifico: null },
              { transaction: t }
            );
            especieId = created.id;
          }
        }

        
        // upsert em SubparcelaArvore por (subparcelaId, especieId, tipoArvore)
        const [arv, createdArv] = await SubparcelaArvore.findOrCreate({
        where: { subparcelaId: sub.id, especieId, tipoArvore },
        defaults: {
            subparcelaId: sub.id,
            especieId,
            tipoArvore,
            numeroArvoresEspecie: qt,   // 👈 nome correto do campo
        },
        transaction: t,
        hooks: false,
        });

        if (createdArv) {
        insertedArvores++;
        } else {
        await SubparcelaArvore.update(
            { numeroArvoresEspecie: qt }, // 👈 atualiza o campo correto
            { where: { id: arv.id }, transaction: t, hooks: false }
        );
        updatedArvores++;
        }

      } catch (err) {
        errors++;
        console.error(`❌ kb_import3x3SubplotRepeat erro na linha ${i + 1}:`, {
          name: err.name,
          message: err.message,
          details: err.errors ? err.errors.map((e) => e.message) : null,
        });
      }
    }

    await t.commit();
  } catch (err) {
    try { if (!t.finished || t.finished === "rollback") await t.rollback(); } catch (_) {}
    console.error("kb_import3x3SubplotRepeat fatal error:", err);
    throw err;
  }

  return {
    insertedSubparcelas,
    updatedSubparcelas,
    insertedArvores,
    updatedArvores,
    unresolvedParcela,
    skippedSemIdSub,
    errors,
  };
}

export default kb_import3x3SubplotRepeat;
