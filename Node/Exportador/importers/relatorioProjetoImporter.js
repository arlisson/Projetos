import TMProjeto from "../models/terramatch/projeto/tm-projeto.model.js";
import TMRelatorioProjeto from "../models/terramatch/relatorio/projeto/tm-relatorio-projeto.model.js";
import TMRelatorioProjetoFoto from "../models/terramatch/relatorio/projeto/tm-relatorio-projeto-foto.association.js";
import TMEvidenciaRegistroFotografico from "../models/terramatch/relatorio/tm-evidencia-registro-fotografico.model.js";

import TMDemografiaDiasUteis from "../models/terramatch/relatorio/demografia/tm-demografia-dias-uteis.model.js";
import TMRelatorioProjetoHasDemografia from "../models/terramatch/relatorio/projeto/tm-relatorio-projeto-has-demografia.association.js";
import TMDemografiaHasGenero from "../models/terramatch/relatorio/demografia/tm-demografia-has-genero.association.js";
import TMDemografiaHasFaixaEtaria from "../models/terramatch/relatorio/demografia/tm-demografia-has-faixa-etaria.association.js";
import TMDemografiaHasEtnia from "../models/terramatch/relatorio/demografia/tm-demografia-has-etnia.association.js";

/**
 * Utilitário: parseia string do tipo:
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

// TODO: substituir por buscas reais nas tabelas de catálogo
async function resolveGeneroId(_) {
  return 1;
}
async function resolveFaixaEtariaId(_) {
  return 1;
}
async function resolveEtniaId(_) {
  return 1;
}

async function salvarDemografia(relatorioDb, raw, tipo, categoria) {
  if (!raw || raw.trim() === "") return;

  const parsed = parseDemografia(raw);

  // 🔑 garante que não cria duplicado
  const [demografia] = await TMDemografiaDiasUteis.findOrCreate({
    where: { tipo, categoria },
    defaults: { tipo, categoria },
  });

  // 🔗 vincula ao relatório
  await TMRelatorioProjetoHasDemografia.findOrCreate({
    where: {
      relatorio_projeto_id: relatorioDb.id,
      demografia_dos_dias_uteis_id: demografia.id,
    },
  });

  // popula detalhamento com logs
  for (const g of parsed.genero) {
    const [registro, created] = await TMDemografiaHasGenero.findOrCreate({
      where: {
        demografia_dos_dias_uteis_id: demografia.id,
        genero_id: await resolveGeneroId(g.nome),
      },
      defaults: {
        quantidade: g.qtd,
      },
    });

    if (created) {
      console.log(`👤 Gênero adicionado: ${g.nome} (${g.qtd}) no relatório ${relatorioDb.titulo}`);
    } else {
      console.log(`🔗 Gênero já existente: ${g.nome} no relatório ${relatorioDb.titulo}`);
    }
  }

  for (const f of parsed.faixaEtaria) {
    const [registro, created] = await TMDemografiaHasFaixaEtaria.findOrCreate({
      where: {
        demografia_dos_dias_uteis_id: demografia.id,
        faixa_etaria_id: await resolveFaixaEtariaId(f.nome),
      },
      defaults: {
        quantidade: f.qtd,
      },
    });

    if (created) {
      console.log(`📊 Faixa etária adicionada: ${f.nome} (${f.qtd}) no relatório ${relatorioDb.titulo}`);
    } else {
      console.log(`🔗 Faixa etária já existente: ${f.nome} no relatório ${relatorioDb.titulo}`);
    }
  }

  for (const e of parsed.etnia) {
    const [registro, created] = await TMDemografiaHasEtnia.findOrCreate({
      where: {
        demografia_dos_dias_uteis_id: demografia.id,
        etnia_id: await resolveEtniaId(e.nome),
      },
      defaults: {
        quantidade: e.qtd,
      },
    });

    if (created) {
      console.log(`🌍 Etnia adicionada: ${e.nome} (${e.qtd}) no relatório ${relatorioDb.titulo}`);
    } else {
      console.log(`🔗 Etnia já existente: ${e.nome} no relatório ${relatorioDb.titulo}`);
    }
  }
}


export async function importRelatoriosFromArray(relatorios) {
  for (const r of relatorios) {
    try {
      const uuid = r.uuid;

      // 🔍 encontra projeto
      const projeto = await TMProjeto.findOne({ where: { uuid: r.project_uuid } });
      
      if (!projeto) {

        console.warn(`⚠️ Projeto não encontrado para relatório ${r.title} (project_uuid: ${r.project_uuid})`);
        continue;
      }

      // 🔍 evita duplicados pelo uuid
      let relatorioDb = await TMRelatorioProjeto.findOne({ where: { uuid } });
      
      if (!relatorioDb) {
        relatorioDb = await TMRelatorioProjeto.create({
          uuid,
          projeto_id: projeto.id,
          data_prazo: r.due_date || null,
          titulo: r.title || null,
          narrativa_tecnica: r.technical_narrative || null,
          narrativa_publica: r.public_narrative || null,
          total_mudas_produzidas_relatorio: r.total_seedlings_grown_report || null,
          total_parceiros_restauracao_unicos: r.total_unique_restoration_partners || null,
          arquivo: r.file || null,
          outros_documentos_adicionais: r.other_additional_documents || null,
          dados_extras: JSON.stringify({
            workdays: {
              paid: r.workdays_paid,
              volunteer: r.workdays_volunteer,
              description: r.other_workdays_description,
            },
            restorationPartners: {
              directIncome: r.restorationPartnersDirectIncome,
              indirectIncome: r.restorationPartnersIndirectIncome,
              directBenefits: r.restorationPartnersDirectBenefits,
              indirectBenefits: r.restorationPartnersIndirectBenefits,
              directConservationPayments: r.restorationPartnersDirectConservationPayments,
              indirectConservationPayments: r.restorationPartnersIndirectConservationPayments,
              directMarketAccess: r.restorationPartnersDirectMarketAccess,
              indirectMarketAccess: r.restorationPartnersIndirectMarketAccess,
              directCapacity: r.restorationPartnersDirectCapacity,
              indirectCapacity: r.restorationPartnersIndirectCapacity,
              directTraining: r.restorationPartnersDirectTraining,
              indirectTraining: r.restorationPartnersIndirectTraining,
              directLandTitle: r.restorationPartnersDirectLandTitle,
              indirectLandTitle: r.restorationPartnersIndirectLandTitle,
              directLivelihoods: r.restorationPartnersDirectLivelihoods,
              indirectLivelihoods: r.restorationPartnersIndirectLivelihoods,
              directProductivity: r.restorationPartnersDirectProductivity,
              indirectProductivity: r.restorationPartnersIndirectProductivity,
              description: r.other_restoration_partners_description,
            },
          }),
        });

        console.log(`✅ Relatório criado: ${relatorioDb.titulo} (uuid: ${uuid})`);
      } else {
        console.log(`↔️ Relatório já existe: ${relatorioDb.titulo} (uuid: ${uuid})`);
      }

      // ============================
      // 📷 Importa fotos associadas
      // ============================
      if (r.photos && r.photos !== "") {
      const fotos = r.photos.split("|").map(f => f.trim()).filter(Boolean);

      for (const url of fotos) {
        const [evidencia] = await TMEvidenciaRegistroFotografico.findOrCreate({
          where: { link_registro_fotografico: url },
          defaults: {
            evidencias: `Foto importada do relatório ${relatorioDb.titulo}`,
            link_registro_fotografico: url,
          },
        });

        const [relFoto, created] = await TMRelatorioProjetoFoto.findOrCreate({
          where: {
            relatorio_id: relatorioDb.id,
            evidencia_id: evidencia.id,
          },
        });

        if (created) {
          console.log(`📷 Foto vinculada ao relatório: ${url}`);
        } else {
          console.log(`🔗 Foto já vinculada ao relatório: ${url}`);
        }
      }
    }


      // ============================
      // 👥 Importa demografia dos dias úteis
      // ============================
      await salvarDemografia(relatorioDb, r.workdaysPaidProjectManagement, "pago", "ProjectManagement");
      await salvarDemografia(relatorioDb, r.workdaysVolunteerProjectManagement, "voluntario", "ProjectManagement");
      await salvarDemografia(relatorioDb, r.workdaysPaidNurseryOperations, "pago", "NurseryOperations");
      await salvarDemografia(relatorioDb, r.workdaysVolunteerNurseryOperations, "voluntario", "NurseryOperations");
      await salvarDemografia(relatorioDb, r.workdaysPaidOtherActivities, "pago", "OtherActivities");
      await salvarDemografia(relatorioDb, r.workdaysVolunteerOtherActivities, "voluntario", "OtherActivities");

    } catch (err) {
      console.error(`❌ Erro ao importar relatório ${r.title} (id: ${r.id}):`, err);
    }
  }

  console.log(`🏁 Importação de ${relatorios.length} relatórios processada!`);
}
