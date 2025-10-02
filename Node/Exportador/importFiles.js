import fs from "fs";
import sequelize from "./config/postgres.config.js";
import { normalizeKeys } from "./utils/normalizeKeys.js";
import { normalizeSitesData } from "./utils/normalizeSitesData.js";
import { import_csv, import_xlsx } from "./utils/fileImporter.js";
import { importProjetosFromArray } from "./importers/projetoImporter.js";
import { importSitiosFromArray } from "./importers/sitioImporter.js";
import { importRelatoriosFromArray } from "./importers/relatorioProjetoImporter.js";
import { importRelatoriosSitioFromArray } from "./importers/relatorioSitioImporter.js";
import { importGeometriaSitio } from "./importers/importGeometriaSitio.js";
import { kb_importPPC_Pacto_CERT } from "./importers/kb_ppcPactoImporter.js";
import { kb_importY0_Database } from "./importers/kb_Y0DatabaseImporter.js";
import { kb_importCoord_PPC } from "./importers/kb_coordPpcImporter.js";

//TODO: Escrever o importador de atualizações.
//TODO: Escrever a regex para generalizar os nomes dos projetos e sitios.
//TODO: Forçar a organização de importação de arquivos seguindo a ordem: 
// projetos e seus relacionados (relatórios do projeto),
// sítios e seus relacionados (geometria e relatórios),
// relatórios de projetos

/**
 * Executa o ETL em uma lista de arquivos fornecidos.
 * @param {string[]} files - Caminhos dos arquivos a serem importados
 */
export async function importFiles(files = []) {
  try {
    await sequelize.authenticate();
    console.log("Conexão OK com o banco!");

    for (const file of files) {
      let data;

      if (file.endsWith(".csv")) {
        data = await import_csv({ filePath: file });
        data = normalizeKeys(data);

      } else if (file.endsWith(".xlsx")) {
        const sheetsData = import_xlsx({ filePath: file }); // { SheetName: rows[] }

        // percorre cada aba
        for (const [sheetName, rows] of Object.entries(sheetsData)) {
          const normalized = normalizeKeys(rows);

          // agora decide o importador, mas baseado no nome do arquivo + nome da aba
          if (file.toLowerCase().includes("site establishment")) {
            const sitiosNormalizados = await normalizeSitesData(normalized);
            await importSitiosFromArray(sitiosNormalizados);

          } else if (file.toLowerCase().includes("project establishment")) {
            await importProjetosFromArray(normalized);

          } else if (file.toLowerCase().includes("project reports")) {
            await importRelatoriosFromArray(normalized);

          } else if (file.toLowerCase().includes("site reports")) {
            await importRelatoriosSitioFromArray(normalized);

          }else if (sheetName.toLowerCase().includes("ppc_pacto_cert")) { 
              console.log('Importando dados do PPC_Pacto_CERT...');
              await kb_importPPC_Pacto_CERT(normalized);
          }else if (sheetName.toLowerCase().includes("controle")) {
            console.log('Importando dados de Controle...');
          } else if (sheetName.toLowerCase().includes("y0_database")) {
            
            console.log("Importando dados de Y0_Database...");
            const { inserted, updated, skipped } = await kb_importY0_Database(normalized);
            console.log(`Y0_Database → inserted: ${inserted}, updated: ${updated}, skipped: ${skipped}`);

          } else if (sheetName.toLowerCase().includes("coord_ppc")) {
            console.log("Importando dados de Coord_PPC...");
            const { inserted, errors } = await kb_importCoord_PPC(normalized);
            console.log(`Coord_PPC → inserted: ${inserted}, errors: ${errors}`);
          } else if (sheetName.toLowerCase().includes("coord_pacto")) {
            console.log('Importando dados de Coord_Pacto...');
          } else {
            console.warn(`⚠️ Aba ignorada: ${sheetName} em ${file}`);
          }
        }
        continue;
      } else if (file.endsWith(".json") || file.endsWith(".geojson")) {
        const raw = fs.readFileSync(file, "utf-8");
        data = JSON.parse(raw);

        if (file.endsWith(".geojson")) {
          data = data.features; // 👈 pega só o array de features
        }

        data = normalizeKeys(data);
      } else {
        console.warn(`⚠️ Tipo de arquivo não suportado: ${file}`);
        continue;
      }

      // chama o importador correto
      if (file.toLowerCase().includes("site establishment")) {
        const sitiosNormalizados = await normalizeSitesData(data);
        await importSitiosFromArray(sitiosNormalizados);

      } else if (file.toLowerCase().includes("project establishment")) {
        await importProjetosFromArray(data);

      } else if (file.toLowerCase().includes("project reports")) {
        await importRelatoriosFromArray(data);

      } else if (file.toLowerCase().includes("site reports")) {
        await importRelatoriosSitioFromArray(data);

      } else if (file.toLowerCase().endsWith(".geojson")) {
        await importGeometriaSitio(file);

      } 

    }

    await sequelize.close();
    console.log("ETL finalizado!");
  } catch (err) {
    console.error("❌ Erro no ETL:", err);
  }
}
