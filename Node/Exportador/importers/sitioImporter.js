import TMSitio from "../models/terramatch/sitio/tm-sitio.model.js";
import TMProjeto from "../models/terramatch/projeto/tm-projeto.model.js";
import Categoria from "../models/catalogo/categoria.model.js";
import Especie from "../models/catalogo/especie.model.js";
import TMSitioTemEspecieArvore from "../models/terramatch/sitio/tm-sitio-especie-arvore.association.js";
import Tecnica from "../models/catalogo/tecnica.model.js";
import TMSitioTemTecnica from "../models/terramatch/sitio/tm-sitio-tecnica.association.js";
import Metodologia from "../models/catalogo/metodologia.model.js";
import TipoUsoSolo from "../models/catalogo/tipo-uso-solo.model.js";
import TMSitioTemTipoUsoSolo from "../models/terramatch/sitio/tm-sitio-tipo-uso-solo.association.js";


export async function importSitiosFromArray(sitios) {
  for (const s of sitios) {
    try {
      const idSitio = s.id || s["﻿\"id\""] || s["id"];
      const uuid = s.uuid;
      const projectUuid =
        s.project_uuid || s["project-uuid"] || s.projectUuid || null;

      // 🔍 encontra projeto
      const projeto = await TMProjeto.findOne({ where: { uuid: projectUuid } });
      if (!projeto) {
        console.warn(
          `⚠️ Projeto não encontrado para o sítio ${s.name || s.nome} (project-id: ${s["project-id"]})`
        );
        continue;
      }

      // 🔍 resolve ou cria categoria
      let posseCategoriaId = null;
      if (s.land_tenures) {
        const tenureRaw = s.land_tenures.split("??").pop().trim().toLowerCase();
        const descricao =
          tenureRaw.charAt(0).toUpperCase() + tenureRaw.slice(1);

        const [categoria] = await Categoria.findOrCreate({
          where: { descricao },
          defaults: { descricao },
        });

        posseCategoriaId = categoria.id;
      }

      // 🔍 evita duplicados
      let sitioDb = await TMSitio.findOne({ where: { id: idSitio } });
      if (!sitioDb) {
        sitioDb = await TMSitio.create({
          id: idSitio,
          uuid,
          projeto_id: projeto.id,
          nome: s.name || s.nome,
          link_terramatch: s.link_to_terramatch || null,
          status: s.status || null,
          descricao: s.description || s.descricao,
          historico: s.history || null,
          data_inicio: s.start_date || null,
          data_fim: s.end_date || null,
          posse_categoria_id: posseCategoriaId,
          taxa_sobrevivencia_plantada: s.survival_rate_planted || null,
          meta_cobertura_cinco_anos: s.aim_year_five_crown_cover || null,
          taxa_sobrevivencia_semeadura_direta:
            s.direct_seeding_survival_rate || null,
          arvores_regeneracao_natural_por_hectare:
            s.a_nat_regeneration_trees_per_hectare || null,
          regeneracao_natural_indice: s.a_nat_regeneration || null,
          meta_numero_arvores_maduras: s.aim_number_of_mature_trees || null,
          condicao_solo: s.soil_condition || null,
          padrao_plantio: s.planting_pattern || null,
          estratos: s.stratas || null,
          sementes: s.seedings || null,
          arquivos_adicionais:
            s.document_files || s.other_additional_documents || null,
        });

        console.log(`✅ Sítio criado: ${s.name || s.nome} (id: ${idSitio})`);
      } else {
        console.log(`↔️ Sítio já existe: ${s.name || s.nome} (id: ${idSitio})`);
      }

      // ============================
      // 🌱 Importa espécies associadas
      // ============================
      let invasives = [];
      let treeSpecies = [];

      try {
        if (s.invasives) invasives = JSON.parse(s.invasives);
      } catch {
        console.warn(`⚠️ Erro parseando invasives do sítio ${s.name}`);
      }

      try {
        if (s.treeSpecies) treeSpecies = JSON.parse(s.treeSpecies);
      } catch {
        console.warn(`⚠️ Erro parseando treeSpecies do sítio ${s.name}`);
      }

      const invasivesList = invasives.map((sp) => ({
        ...sp,
        invasora: true,
      }));

      const treeSpeciesList = treeSpecies.map((sp) => ({
        ...sp,
        invasora: false,
      }));

      const allSpecies = [...invasivesList, ...treeSpeciesList];

      for (const sp of allSpecies) {
        const nome = sp.name?.trim();
        if (!nome) continue;

        let especie = await Especie.findOne({
          where: { nome_cientifico: nome },
        });

        if (!especie) {
          especie = await Especie.create({
            nome_cientifico: nome,
            nome_popular: sp.common_name || null,
          });
          console.log(`🌱 Espécie criada: ${nome}`);
        }

        await TMSitioTemEspecieArvore.findOrCreate({
          where: {
            tm_sitio_id: sitioDb.id,
            especie_id: especie.id,
          },
          defaults: {
            invasora: sp.invasora,
            observacao: sp.type || null,
          },
        });
      }

      // ============================
      // 🔧 Importa técnicas associadas
      // ============================
      if (s.restoration_strategy) {
        const estrategias = s.restoration_strategy
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
                descricao:
                  "Metodologia padrão para técnicas importadas automaticamente",
              },
            });

            tecnica = await Tecnica.create({
              titulo: estrategia,
              metodologia_id: metodologia.id,
            });
            console.log(`🔧 Técnica criada: ${estrategia}`);
          }

          await TMSitioTemTecnica.findOrCreate({
            where: {
              tm_sitio_id: sitioDb.id,
              tecnica_id: tecnica.id,
            },
            defaults: {
              observacao: null,
            },
          });
        }
      }

      if (s.land_use_types) {
        const usos = s.land_use_types
          .split("|")
          .map((item) => item.split("??").pop().trim())
          .filter((x) => x);

        for (const uso of usos) {
          let tipoUso = await TipoUsoSolo.findOne({ where: { titulo: uso } });

          if (!tipoUso) {
            tipoUso = await TipoUsoSolo.create({ titulo: uso });
            console.log(`🌍 Tipo de uso do solo criado: ${uso}`);
          }

          await TMSitioTemTipoUsoSolo.findOrCreate({
            where: {
              tm_sitio_id: sitioDb.id,
              tipo_uso_solo_id: tipoUso.id,
            },
            defaults: {
              observacao: null,
            },
          });
        }
      }
    } catch (err) {
      console.error(`❌ Erro ao importar sítio ${s.name || s.nome}:`, err);
    }
  }

  console.log(`🏁 Importação de ${sitios.length} sítios concluída!`);
}
