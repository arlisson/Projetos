// importers/kb_stagePlotRepeat.js
import sequelize from "#config/postgres.config.js";
import models from "#models/kobo/index.js";
import Especie from "#models/catalogo/especie.model.js";
import { Op } from "sequelize";
import { getOrCreateEspecieId } from "../utils/especieHelper.js";
import { setPlotRepeatStage } from "../utils/stagePlotRepeatMap.js";

/**
 * Faz o stage do "30x30_Plot_Repeat" para consumo pelo importador de fustes (group_un3bb19).
 * Para cada linha:
 *  - Resolve a parcela (idParcela OU _submission__uuid → Monitoramento → Parcela)
 *  - Resolve a espécie (com fallback para "desconhecida")
 *  - Normaliza o tipo de árvore
 *  - Salva no stage em memória: key = (_submission__uuid, _index)
 *
 * Retorna métricas: { staged, unresolved, noSpecies, errors }
 */
export async function kb_stagePlotRepeat(rows = []) {
  const { Monitoramento, ParcelaMonitoramento } = models;

  let staged = 0;
  let unresolved = 0;
  let noSpecies = 0;
  let errors = 0;

  const nonEmpty = (v) => v !== undefined && v !== null && String(v).trim() !== "";
  const clean = (v) => {
    if (!nonEmpty(v)) return null;
    const s = String(v).trim();
    return s.length ? s : null;
  };
  const pick = (row, keys) => {
    for (const k of keys) {
      if (Object.prototype.hasOwnProperty.call(row, k) && nonEmpty(row[k])) {
        return row[k];
      }
    }
    return null;
  };

  // possíveis nomes de idParcela
  const parcelaIdKeys = [
    'Identificação (ID) da Parcela de Monitoramento de Árvores',
    'Identificação da Parcela de Monitoramento de Árvores',
    'Identificação da Parcela',
    'ID da Parcela',
    'id_parcela',
    'plot_id',
    'Plot ID',
    'plotID',
  ];

  // chaves de vínculo de repeat
  const submissionUUIDKeys = ['_submission__uuid', '_uuid', 'submission__uuid', 'uuid', 'instanceID', 'instance_id'];
  const indexKeys = ['_index', 'index', '__index'];

  // colunas de espécie e tipo
  const speciesKeys = [
    'Espécies de árvores (use nome científico)',
    'Espécies',
    'Espécie',
    'species',
  ];
  const tipoKeys = ['Tipo de Árvore', 'tipo_arvore', 'tipo'];

  function normalizeTipoArvore(raw) {
    const s = clean(raw)?.toLowerCase();
    if (!s) return 'desconhecido';
    if (s.includes('plant')) return 'plantada';
    if (s.includes('regen') || s.includes('natural')) return 'regenerando';
    if (s.includes('antes') || s.includes('preexist')) return 'presente_antes';
    return 'desconhecido';
  }

  async function resolveParcelaId(row) {
    // A) tentar por idParcela direto
    const idParcelaRaw = pick(row, parcelaIdKeys);
    if (idParcelaRaw) {
      const parcela = await ParcelaMonitoramento.findOne({
        where: { idParcela: String(idParcelaRaw).trim() },
        attributes: ['id'],
        raw: true,
      });
      if (parcela?.id) return parcela.id;
    }

    // B) tentar por _submission__uuid → monitoramento.uuid → parcela do monitoramento
    const uuidRaw = pick(row, submissionUUIDKeys);
    if (uuidRaw) {
      const uuid = String(uuidRaw).trim().toLowerCase();

      // validação simples de UUID v4 (igual ao import principal)
      const UUID_V4_RX = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
      if (UUID_V4_RX.test(uuid)) {
        const mon = await Monitoramento.findOne({
          where: { uuid },
          attributes: ['id'],
          raw: true,
        });
        if (mon?.id) {
          // assumindo 1:1 (se houver mais de uma parcela por monitoramento, ajuste o where)
          const parcela = await ParcelaMonitoramento.findOne({
            where: { monitoramentoId: mon.id },
            attributes: ['id'],
            raw: true,
          });
          if (parcela?.id) return parcela.id;
        }
      }
    }

    return null;
  }

  const t = await sequelize.transaction();
  try {
    for (const [i, row] of rows.entries()) {
      try {
        const submissionUuid = clean(pick(row, submissionUUIDKeys));
        const indexVal = clean(pick(row, indexKeys));

        if (!submissionUuid || indexVal == null) {
          unresolved++;
          continue;
        }

        const parcelaId = await resolveParcelaId(row);
        if (!parcelaId) {
          unresolved++;
          continue;
        }

        // espécie (com fallback para "desconhecida")
        const especieRaw = clean(pick(row, speciesKeys));
        let especieId = await getOrCreateEspecieId(especieRaw, { transaction: t });

        if (!especieId) {
          const ex = await Especie.findOne({
            where: { nome: { [Op.iLike]: 'desconhecida' } },
            attributes: ['id'],
            raw: true,
            transaction: t,
          });
          if (ex?.id) {
            especieId = ex.id;
          } else {
            const created = await Especie.create(
              { nome: 'desconhecida', nome_cientifico: null },
              { transaction: t }
            );
            especieId = created.id;
          }
          noSpecies++;
        }

        const tipoArvore = normalizeTipoArvore(pick(row, tipoKeys));

        // grava no stage de memória: key = (submissionUuid, index)
        setPlotRepeatStage(submissionUuid, indexVal, {
          parcelaId,
          especieId,
          tipoArvore,
        });

        staged++;
      } catch (err) {
        errors++;
        console.error(`❌ kb_stagePlotRepeat erro na linha ${i + 1}:`, {
          name: err.name,
          message: err.message,
          details: err.errors ? err.errors.map((e) => e.message) : null,
        });
      }
    }

    await t.commit();
  } catch (err) {
    await t.rollback();
    errors++;
    console.error("kb_stagePlotRepeat fatal error:", err);
    throw err;
  }

  return { staged, unresolved, noSpecies, errors };
}

export default kb_stagePlotRepeat;
