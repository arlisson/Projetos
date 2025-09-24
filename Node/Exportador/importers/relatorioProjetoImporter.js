import TMProjeto from "../models/terramatch/projeto/tm-projeto.model.js";
import TMRelatorioProjeto from "../models/terramatch/relatorio/projeto/tm-relatorio-projeto.model.js";
import TMRelatorioProjetoFoto from "../models/terramatch/relatorio/projeto/tm-relatorio-projeto-foto.association.js";
import TMEvidenciaRegistroFotografico from "../models/terramatch/relatorio/tm-evidencia-registro-fotografico.model.js";

export async function importRelatoriosFromArray(relatorios) {
  for (const r of relatorios) {
    try {
      const uuid = r.uuid;

      // 🔍 encontra projeto
      const projeto = await TMProjeto.findOne({ where: { uuid: r.project_uuid } });
      if (!projeto) {
        console.warn(
          `⚠️ Projeto não encontrado para relatório ${r.title} (project_uuid: ${r.project_uuid})`
        );
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
              paidProjectManagement: r.workdaysPaidProjectManagement,
              volunteerProjectManagement: r.workdaysVolunteerProjectManagement,
              paidNursery: r.workdaysPaidNurseryOperations,
              volunteerNursery: r.workdaysVolunteerNurseryOperations,
              paidOther: r.workdaysPaidOtherActivities,
              volunteerOther: r.workdaysVolunteerOtherActivities,
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
          // 1. Cria ou encontra a evidência fotográfica
          const [evidencia] = await TMEvidenciaRegistroFotografico.findOrCreate({
            where: { link_registro_fotografico: url },
            defaults: {
              evidencias: relatorioDb.id,
              link_registro_fotografico: url,
            },
          });

          // 2. Cria a ligação com o relatório
          await TMRelatorioProjetoFoto.findOrCreate({
            where: {
              relatorio_id: relatorioDb.id,
              evidencia_id: evidencia.id,
            },
          });

          console.log(`📷 Foto vinculada: ${url}`);
        }
      }

    } catch (err) {
      console.error(`❌ Erro ao importar relatório ${r.title} (id: ${r.id}):`, err);
    }
  }

  console.log(`🏁 Importação de ${relatorios.length} relatórios processada!`);
}
