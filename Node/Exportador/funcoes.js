import fs from "fs";
import csv from "csv-parser";       
import xlsx from "xlsx";

export function import_csv({ filePath = null, separator = ",", export_json = false }) {
  return new Promise((resolve, reject) => {
    const results = [];

    try {
      fs.createReadStream(filePath)
        .pipe(csv({ separator }))
        .on("data", (data) => results.push(data))
        .on("end", () => {
          console.log("CSV lido com sucesso!");

          if (export_json) {
            const jsonResults = JSON.stringify(results, null, 2);
            fs.writeFileSync(filePath.replace(".csv", ".json"), jsonResults, "utf8");
            console.log("JSON exportado com sucesso!");
          }

          resolve(results);
        })
        .on("error", (err) => {
          console.error("Erro ao ler o arquivo CSV:", err);
          reject(err);
        });
    } catch (error) {
      console.error("Erro ao ler o arquivo CSV:", error);
      reject(error);
    }
  });
}


export function import_xlsx({ filePath = null, export_json = false }) {
  try {
    // Lê o arquivo
    const workbook = xlsx.readFile(filePath);

    // Pega a primeira aba
    const sheetName = workbook.SheetNames[0];

    // Converte a aba em JSON (array de objetos)
    const data = xlsx.utils.sheet_to_json(workbook.Sheets[sheetName]);

    console.log("XLSX lido com sucesso!");

    if (export_json) {
      // Gera JSON legível (indentado)
      const jsonResults = JSON.stringify(data, null, 2);

      // Decide nome do arquivo de saída
      const outFile = filePath.replace(/\.xlsx?$/i, ".json");

      // Salva JSON no disco
      fs.writeFileSync(outFile, jsonResults, "utf8");

      console.log(`JSON exportado com sucesso para: ${outFile}`);
    }

    return data;
  } catch (error) {
    console.error("Erro ao ler o arquivo XLSX:", error);
    throw error;
  }
}