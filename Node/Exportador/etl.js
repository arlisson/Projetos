import fs from "fs";
import sequelize from "./config/postgres.config.js";
import { normalizeKeys } from "./utils/normalizeKeys.js";
import { normalizeSitesData } from "./utils/normalizeSitesData.js";
import { import_csv, import_xlsx } from "./utils/fileImporter.js";
import { importProjetosFromArray } from "./importers/projetoImporter.js";
import { importSitiosFromArray } from "./importers/sitioImporter.js";
import { importRelatoriosFromArray } from "./importers/relatorioProjetoImporter.js";


async function runETL() {
  try {
    await sequelize.authenticate();
    console.log("Conexão OK com o banco!");

    // lista de arquivos de entrada
    const files = [
      "../Arli/TerraMatch/projects-MDPS - Flagship/MDPS - Flagship - project establishment data.csv",
      "../Arli/TerraMatch/projects-MDPS - Flagship/MDPS - Flagship - site establishment data.csv",
      "../Arli/TerraMatch/projects-MDPS - Flagship/MDPS - Flagship - project reports.csv",
    ];

    for (const file of files) {
      let data;

      if (file.endsWith(".csv")) {
        data = await import_csv({ filePath: file });
        data = normalizeKeys(data);

      } else if (file.endsWith(".xlsx")) {
        data = import_xlsx({ filePath: file });
        data = normalizeKeys(data);

      } else if (file.endsWith(".json")) {
        const raw = fs.readFileSync(file, "utf-8");
        data = JSON.parse(raw);
        data = normalizeKeys(data); // 👈 funciona igual
      } else {
        console.warn(`⚠️ Tipo de arquivo não suportado: ${file}`);
        continue;
      }

      // chama o importador correto
      if (file.toLowerCase().includes("site")) {
        const sitiosNormalizados = await normalizeSitesData(data);
        await importSitiosFromArray(sitiosNormalizados);

      } else if (file.toLowerCase().includes("project establishment")) {
        await importProjetosFromArray(data);

      } else if (file.toLowerCase().includes("project reports")) {
        await importRelatoriosFromArray(data);
      }

    }

    await sequelize.close();
    console.log("ETL finalizado!");
  } catch (err) {
    console.error("❌ Erro no ETL:", err);
  }
}

runETL();
