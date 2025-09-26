import TMSitio from "../models/terramatch/sitio/tm-sitio.model.js"
import TMRelatorioSitio from "../models/terramatch/relatorio/sitio/tm-relatorio-sitio.model.js";
import TMRelatorioSitioFoto from "../models/terramatch/relatorio/sitio/tm-relatorio-sitio-foto.association.js";
import TMEvidenciaRegistroFotografico from "../models/terramatch/relatorio/tm-evidencia-registro-fotografico.model.js";
import TMRelatorioSitioTemEspecieArvore from "../models/terramatch/relatorio/sitio/tm-relatorio-sitio-especie-arvore.association.js";
import TMRelatorioSitioHasDemografia from "../models/terramatch/relatorio/sitio/tm-relatorio-sitio-has-demografia.association.js";
import TMDemografiaDiasUteis from "../models/terramatch/relatorio/demografia/tm-demografia-dias-uteis.model.js";
import TMDemografiaHasGenero from "../models/terramatch/relatorio/demografia/tm-demografia-has-genero.association.js";
import TMDemografiaHasFaixaEtaria from "../models/terramatch/relatorio/demografia/tm-demografia-has-faixa-etaria.association.js";
import TMDemografiaHasEtnia from "../models/terramatch/relatorio/demografia/tm-demografia-has-etnia.association.js";
import TMDisturbio from "../models/terramatch/relatorio/sitio/tm-disturbio.model.js";

/**
 * Parse string do tipo:
 * "gender:(2:male)(3:female)|age:(5:adult)|ethnicity:(7:unknown:)"
 */
function parseDemografia(raw) {
  const blocks = raw.split("|");
  const parsed = { genero: [], faixaEtaria: [], etnia: [] };

  for (const block of blocks) {
    if (block.startsWith("gender:")) {
      const matches = [...block.matchAll(/\((\d+):([^)]+)\)/g)];
      parsed.genero = matches.map(([_, qtd, nome]) => ({ qtd: parseInt(qtd), nome }));
    }
    if (block.startsWith("age:")) {
      const matches = [...block.matchAll(/\((\d+):([^)]+)\)/g)];
      parsed.faixaEtaria = matches.map(([_, qtd, nome]) => ({ qtd: parseInt(qtd), nome }));
    }
    if (block.startsWith("ethnicity:")) {
      const matches = [...block.matchAll(/\((\d+):([^)]+)\)/g)];
      parsed.etnia = matches.map(([_, qtd, nome]) => ({ qtd: parseInt(qtd), nome }));
    }
  }

  return parsed;
}

// TODO: ligar com tabelas reais
async function resolveGeneroId(nome) { return 1; }
async function resolveFaixaEtariaId(nome) { return 1; }
async function resolveEtniaId(nome) { return 1; }

async function salvarDemografia(relatorioDb, raw, tipo, categoria) {
  if (!raw || raw.trim() === "") return;

  const parsed = parseDemografia(raw);

  const [demografia] = await TMDemografiaDiasUteis.findOrCreate({
    where: { tipo, categoria },
    defaults: { tipo, categoria },
  });

  await TMRelatorioSitioHasDemografia.findOrCreate({
    where: {
      relatorio_sitio_id: relatorioDb.id,
      demografia_dos_dias_uteis_id: demografia.id,
    },
  });

  for (const g of parsed.genero) {
    await TMDemografiaHasGenero.findOrCreate({
      where: {
        demografia_dos_dias_uteis_id: demografia.id,
        genero_id: await resolveGeneroId(g.nome),
      },
      defaults: { quantidade: g.qtd },
    });
  }

  for (const f of parsed.faixaEtaria) {
    await TMDemografiaHasFaixaEtaria.findOrCreate({
      where: {
        demografia_dos_dias_uteis_id: demografia.id,
        faixa_etaria_id: await resolveFaixaEtariaId(f.nome),
      },
      defaults: { quantidade: f.qtd },
    });
  }

  for (const e of parsed.etnia) {
    await TMDemografiaHasEtnia.findOrCreate({
      where: {
        demografia_dos_dias_uteis_id: demografia.id,
        etnia_id: await resolveEtniaId(e.nome),
      },
      defaults: { quantidade: e.qtd },
    });
  }
}

export async function importRelatoriosSitioFromArray(relatorios) {
  for (const r of relatorios) {
    try {
      const siteId = parseInt(r["site-id"], 10);      
      const relatorioUuid = r.uuid;

      if (!siteId) {
        console.warn(`⚠️ Relatório ${r["site-name"]} não tem site-id definido`);
        continue;
      }

      const sitio = await TMSitio.findOne({ where: { id: siteId } });

      if (!sitio) {
        console.warn(`⚠️ Sítio não encontrado para relatório ${r['site-name']} (site-id: ${siteId})`);
        continue;
      }

      let relatorioDb = await TMRelatorioSitio.findOne({ where: { uuid: relatorioUuid } });
      if (!relatorioDb) {
        relatorioDb = await TMRelatorioSitio.create({
          uuid: relatorioUuid,
          tm_sitio_id: sitio.id, // 👈 corrigido para bater com o model
          data_de_vencimento: r.due_date || null,
          titulo: r['site-name'] || null,
          narrativa_tecnica: r.technical_narrative || null,
          narrativa_publica: r.public_narrative || null,
          total_arvores_plantadas: r.total_trees_planted || null,
          total_sementes_plantadas: r.total_seeds_planted || null,
          numero_arvores_regenerando: r.num_trees_regenerating || null,
          descricao_da_regeneracao: r.regeneration_description || null,
          outros_documentos_adicionais: r.other_additional_documents
                ? r.other_additional_documents.split("|")[0].trim()
                : null,


            
        });
        console.log(`✅ Relatório de sítio criado : ${relatorioDb.titulo}`);
      } else {
        console.log(`↔️ Relatório de sítio já existe : ${relatorioDb.titulo}`);
      }

      // 📷 Fotos
      if (r.media && r.media !== "") {
        const fotos = r.media.split("|").map(f => f.trim()).filter(Boolean);
        for (const url of fotos) {
          const [evidencia] = await TMEvidenciaRegistroFotografico.findOrCreate({
            where: { link_registro_fotografico: url },
            defaults: {
              evidencias: `Foto importada do relatório de sítio : ${relatorioDb.titulo}`,
              link_registro_fotografico: url,
            },
          });
          await TMRelatorioSitioFoto.findOrCreate({
            where: {
              relatorio_id: relatorioDb.id,
              evidencia_id: evidencia.id,
            },
          });
        }
      }

      // 🌱 Espécies
      if (r.treeSpecies && r.treeSpecies !== "") {
        const especies = r.treeSpecies.split("|").map(e => e.trim()).filter(Boolean);
        for (const especieStr of especies) {
          const [nome, qtd] = especieStr.split(":");
          await TMRelatorioSitioTemEspecieArvore.findOrCreate({
            where: {
              relatorio_sitio_id: relatorioDb.id,
              especie_id: 1, // TODO: mapear espécie pelo nome real
            },
            defaults: { quantidade: parseInt(qtd) || 0 },
          });
        }
      }

      // ⚡ Distúrbios
      if (r.disturbances && r.disturbances !== "") {
        const disturbios = JSON.parse(r.disturbances);
        for (const d of disturbios) {
          await TMDisturbio.findOrCreate({
            where: {
              relatorio_sitio_id: relatorioDb.id,
              titulo: d.title,
            },
            defaults: { descricao: d.description },
          });
        }
      }

      // 👥 Demografia
      await salvarDemografia(relatorioDb, r.workdaysPaidSiteEstablishment, "pago", "SiteEstablishment");
      await salvarDemografia(relatorioDb, r.workdaysVolunteerSiteEstablishment, "voluntario", "SiteEstablishment");
      await salvarDemografia(relatorioDb, r.workdaysPaidPlanting, "pago", "Planting");
      await salvarDemografia(relatorioDb, r.workdaysVolunteerPlanting, "voluntario", "Planting");
      await salvarDemografia(relatorioDb, r.workdaysPaidSiteMaintenance, "pago", "Maintenance");
      await salvarDemografia(relatorioDb, r.workdaysVolunteerSiteMaintenance, "voluntario", "Maintenance");
      await salvarDemografia(relatorioDb, r.workdaysPaidSiteMonitoring, "pago", "Monitoring");
      await salvarDemografia(relatorioDb, r.workdaysVolunteerSiteMonitoring, "voluntario", "Monitoring");
      await salvarDemografia(relatorioDb, r.workdaysPaidOtherActivities, "pago", "OtherActivities");
      await salvarDemografia(relatorioDb, r.workdaysVolunteerOtherActivities, "voluntario", "OtherActivities");

    } catch (err) {
      console.error(`❌ Erro ao importar relatório de sítio ${r["site-name"]} (uuid: ${r.uuid}):`, err);
    }
  }

  console.log(`🏁 Importação de ${relatorios.length} relatórios de sítio processada!`);
}