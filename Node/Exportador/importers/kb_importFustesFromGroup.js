// importers/kb_importFustesFromGroup.js
import sequelize from "#config/postgres.config.js";
import models from "#models/kobo/index.js";
import { getPlotRepeatStage } from "../utils/stagePlotRepeatMap.js"; 

export async function kb_importFustesFromGroup(rows = []) {
  const { Arvore } = models;

  let inserted = 0;
  let unresolvedStage = 0;
  let skippedInvalid = 0;
  let skippedDuplicates = 0; // 👈 novo
  let errors = 0;

  const nonEmpty = (v) => v !== undefined && v !== null && String(v).trim() !== "";
  const clean = (v) => (nonEmpty(v) ? String(v).trim() : null);
  const pick = (row, keys) => {
    for (const k of keys) if (Object.prototype.hasOwnProperty.call(row, k) && nonEmpty(row[k])) return row[k];
    return null;
  };

  // 🔑 chaves de vínculo (ampliadas)
  const submissionUUIDKeys = [
    "_submission__uuid", "_uuid", "submission__uuid", "uuid",
    "instanceID", "instance_id",
    "_submission__id", "_id"
  ];
  const parentIndexKeys = ["_parent_index", "parent_index"];
  const parentTableKeys = ["_parent_table_name", "parent_table_name"];

  const numeroArvoreKeys = ["Número da Árvore","Numero da Árvore","Numero da Arvore","Número da Arvore","numero_da_arvore"];
  const numeroFusteKeys  = ["Fuste N.","Fuste","numero_do_fuste","fuste_n"];
  const dapKeys          = ["DAP (cm) da árvore à 1.3m de altura","DAP (cm)","dap_cm","DAP"];

  const toNumber = (v) => {
    if (v == null) return NaN;
    const n = Number(String(v).replace(",", "."));
    return Number.isFinite(n) ? n : NaN;
  };

  const isFrom30x30 = (row) => {
    const p = clean(pick(row, parentTableKeys));
    if (!p) return true;
    return String(p).includes("30x30_Plot_Repeat");
  };

  const t = await sequelize.transaction();
  try {
    for (const [i, row] of rows.entries()) {
      try {
        if (!isFrom30x30(row)) continue;

        const submissionUuid = clean(pick(row, submissionUUIDKeys));
        const parentIndex    = clean(pick(row, parentIndexKeys));

        if (!submissionUuid || parentIndex == null) {
          unresolvedStage++;
          continue;
        }

        const stage = getPlotRepeatStage(submissionUuid, parentIndex); // { parcelaId, especieId, tipoArvore }
        if (!stage) { unresolvedStage++; continue; }

        const { parcelaId, especieId, tipoArvore } = stage;

        const numeroArvore = toNumber(pick(row, numeroArvoreKeys));
        const numeroFuste  = toNumber(pick(row, numeroFusteKeys));
        const dap_cm       = toNumber(pick(row, dapKeys));

        if (!Number.isFinite(numeroArvore) || numeroArvore < 0) { skippedInvalid++; continue; }
        if (!Number.isFinite(numeroFuste)  || numeroFuste  < 0) { skippedInvalid++; continue; }
        if (!Number.isFinite(dap_cm)       || dap_cm <= 0 || dap_cm > 300) { skippedInvalid++; continue; }

        // ✅ evita duplicar: (parcelaId, especieId, numeroArvore, numeroFuste)
        const [rec, created] = await Arvore.findOrCreate({
          where: { parcelaId, especieId, numeroArvore, numeroFuste },
          defaults: { parcelaId, especieId, tipoArvore, numeroArvore, numeroFuste, dap_cm },
          transaction: t,
          hooks: false,
        });

        if (created) {
          inserted++;
        } else {
          // já existe — opcionalmente poderia atualizar dap_cm se quiser
          // await rec.update({ dap_cm }, { transaction: t, hooks: false });
          skippedDuplicates++;
        }
      } catch (err) {
        errors++;
        console.error(`❌ kb_importFustesFromGroup erro na linha ${i + 1}:`, {
          name: err.name, message: err.message,
          details: err.errors ? err.errors.map((e) => e.message) : null,
        });
      }
    }

    await t.commit();
  } catch (err) {
    // ✅ só faz rollback se a transação não foi finalizada
    try {
      if (!t.finished || t.finished === "rollback") {
        await t.rollback();
      }
    } catch (_e) {}
    console.error("kb_importFustesFromGroup fatal error:", err);
    throw err;
  }

  return { inserted, unresolvedStage, skippedInvalid, skippedDuplicates, errors };
}

export default kb_importFustesFromGroup;
