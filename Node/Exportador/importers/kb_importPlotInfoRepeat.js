// importers/kb_importPlotInfoRepeat.js
import sequelize from "#config/postgres.config.js";
import models from "#models/kobo/index.js";

/**
 * Importa "Plot_Info_Repeat" → MidiaAdicionalParcela
 * Estratégia de resolução da parcela:
 *  A) por idParcela (se a aba trouxer esse campo)
 *  B) por _submission__uuid → Monitoramento.uuid → ParcelaMonitoramento (1:1)
 */
export async function kb_importPlotInfoRepeat(rows = []) {
  const { Monitoramento, ParcelaMonitoramento, MidiaAdicionalParcela } = models;

  let inserted = 0;
  let skippedDuplicates = 0;
  let unresolved = 0;
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

  // mídias
  const fotoNomeKeys = ['Fotos Adicionais (Opcional)','Foto Adicional','Fotos Adicionais','Foto'];
  const fotoUrlKeys  = ['Fotos Adicionais (Opcional)_URL','Foto Adicional_URL','Fotos Adicionais_URL','Foto_URL'];
  const arquivoNomeKeys = ['Arquivos Adicionais (Opcional)','Arquivo Adicional','Arquivos Adicionais','Arquivo'];
  const arquivoUrlKeys  = ['Arquivos Adicionais (Opcional)_URL','Arquivo Adicional_URL','Arquivos Adicionais_URL','Arquivo_URL'];

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

      // validação simples de UUID v4 (mesma do seu import principal)
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

  async function isDuplicate({ parcelaId, fotoUrl, arquivoUrl }) {
    if (!parcelaId) return false;
    if (fotoUrl) {
      const ex = await MidiaAdicionalParcela.findOne({
        where: { parcelaId, fotoUrl },
        attributes: ['id'],
        raw: true,
      });
      if (ex) return true;
    }
    if (arquivoUrl) {
      const ex = await MidiaAdicionalParcela.findOne({
        where: { parcelaId, arquivoUrl },
        attributes: ['id'],
        raw: true,
      });
      if (ex) return true;
    }
    return false;
  }

  const t = await sequelize.transaction();
  try {
    for (const row of rows) {
      const parcelaId = await resolveParcelaId(row);
      if (!parcelaId) {
        unresolved++;
        continue;
      }

      const fotoNome = clean(pick(row, fotoNomeKeys));
      const fotoUrl = clean(pick(row, fotoUrlKeys));
      const arquivoNome = clean(pick(row, arquivoNomeKeys));
      const arquivoUrl = clean(pick(row, arquivoUrlKeys));

      if (!fotoNome && !fotoUrl && !arquivoNome && !arquivoUrl) {
        skippedDuplicates++; // nada para gravar
        continue;
      }

      if (await isDuplicate({ parcelaId, fotoUrl, arquivoUrl })) {
        skippedDuplicates++;
        continue;
      }

      await MidiaAdicionalParcela.create(
        { parcelaId, fotoNome: fotoNome ?? null, fotoUrl: fotoUrl ?? null, arquivoNome: arquivoNome ?? null, arquivoUrl: arquivoUrl ?? null },
        { transaction: t }
      );

      inserted++;
    }

    await t.commit();
  } catch (err) {
    await t.rollback();
    errors++;
    console.error("kb_importPlotInfoRepeat error:", err);
    throw err;
  }

  return { inserted, skippedDuplicates, unresolved, errors };
}

export default kb_importPlotInfoRepeat;
