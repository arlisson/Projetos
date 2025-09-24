import TMProjeto from "../models/terramatch/projeto/tm-projeto.model.js";
import Especie from "../models/catalogo/especie.model.js";
import TMProjetoTemEspecieArvore from "../models/terramatch/projeto/tm-projeto-especie-arvore.association.js";

import Tecnica from "../models/catalogo/tecnica.model.js";
import Metodologia from "../models/catalogo/metodologia.model.js";
import TMProjetoTemTecnica from "../models/terramatch/projeto/tm-projeto-tecnica.association.js";

import TipoUsoSolo from "../models/catalogo/tipo-uso-solo.model.js";
import TMProjetoTemTipoUsoSolo from "../models/terramatch/projeto/tm-projeto-tipo-uso-solo.association.js";

export async function importProjetosFromArray(projects) {
  for (const p of projects) {
    try {
      const idProjeto = parseInt(p.id || p["﻿\"id\""], 10);
      const uuid = p.uuid || p.project_uuid || null;
      const nome = p.project_name || p.nome;
      const organizacao = p["organization-name"] || p.organizacao;

      // 🔍 verifica se já existe pelo id
      let projetoDb = await TMProjeto.findOne({ where: { id: idProjeto } });

      if (!projetoDb) {
        // cria novo projeto com id forçado
        projetoDb = await TMProjeto.create({
          id: idProjeto,
          uuid,
          nome,
          organizacao,
          status: p.status || null,
          hectares_objetivo: p.total_hectares_restored_goal || null,
          taxa_sobrevivencia: p.survival_rate || null,
          meta_cobertura_cinco_anos: p.year_five_crown_cover || null,
          data_inicio_plantio: p.planting_start_date || null,
          data_fim_plantio: p.planting_end_date || null,
          continente: p.continent,
          pais: p.country,
          descricao_timeline: p.description_of_project_timeline,
          historico: p.history,
          arquivos_adicionais: p.other_additional_documents,
          dados_extras: JSON.stringify({
            trees_grown_goal: p.trees_grown_goal,
          }),
        });

        console.log(`✅ Projeto criado: ${nome} (id: ${idProjeto})`);
      } else {
        console.log(`↔️ Projeto já existe: ${nome} (id: ${idProjeto})`);
      }

      
      // ============================
      // 🌱 Importa espécies associadas ao projeto
      // ============================
      let treeSpecies = [];

      try {
        if (p.treeSpecies && p.treeSpecies !== "")
          treeSpecies = JSON.parse(p.treeSpecies);
      } catch {
        console.warn(`⚠️ Erro parseando treeSpecies do projeto ${nome}`);
      }

      for (const sp of treeSpecies) {
        const nomeCientifico = sp.name?.trim();
        if (!nomeCientifico) continue;

        let especie = await Especie.findOne({
          where: { nome_cientifico: nomeCientifico },
        });

        if (!especie) {
          especie = await Especie.create({
            nome_cientifico: nomeCientifico,
            nome_popular: sp.common_name || null,
          });
          console.log(`🌱 Espécie criada: ${nomeCientifico}`);
        }

        await TMProjetoTemEspecieArvore.findOrCreate({
          where: {
            tm_projeto_id: projetoDb.id,
            especie_id: especie.id,
          },
          defaults: {
            invasora: false, // 👈 sempre false para projeto
            observacao: sp.type || null,
          },
        });
      }


      // ============================
      // 🔧 Importa técnicas associadas
      // ============================
      if (p.restoration_strategy && p.restoration_strategy !== "") {
        const estrategias = p.restoration_strategy
          .split("|")
          .map((item) => item.split("??").pop().trim())
          .filter((x) => x);

        for (const estrategia of estrategias) {
          let tecnica = await Tecnica.findOne({ where: { titulo: estrategia } });

          if (!tecnica) {
            // garante metodologia padrão
            const [metodologia] = await Metodologia.findOrCreate({
              where: { nome: "Desconhecida" },
              defaults: {
                nome: "Desconhecida",
                descricao: "Metodologia padrão para técnicas importadas automaticamente",
              },
            });

            tecnica = await Tecnica.create({
              titulo: estrategia,
              metodologia_id: metodologia.id,
            });
            console.log(`🔧 Técnica criada: ${estrategia}`);
          }

          await TMProjetoTemTecnica.findOrCreate({
            where: {
              tm_projeto_id: projetoDb.id,
              tecnica_id: tecnica.id,
            },
            defaults: {
              observacao: null,
            },
          });
        }
      }

      // ============================
      // 🌍 Importa tipos de uso do solo
      // ============================
      if (p.land_use_types && p.land_use_types !== "") {
        const usos = p.land_use_types
          .split("|")
          .map((item) => item.split("??").pop().trim())
          .filter((x) => x);

        for (const uso of usos) {
          let tipoUso = await TipoUsoSolo.findOne({ where: { titulo: uso } });

          if (!tipoUso) {
            tipoUso = await TipoUsoSolo.create({ titulo: uso });
            console.log(`🌍 Tipo de uso do solo criado: ${uso}`);
          }

          await TMProjetoTemTipoUsoSolo.findOrCreate({
            where: {
              tm_projeto_id: projetoDb.id,
              tipo_uso_solo_id: tipoUso.id,
            },
            defaults: {
              observacao: null,
            },
          });
        }
      }
    } catch (err) {
      console.error(`❌ Erro ao importar projeto ${p.project_name || p.nome} (id: ${p.id || p["﻿\"id\""]}):`, err);

    }
  }

  console.log(`🏁 Importação de ${projects.length} projetos processada!`);
}