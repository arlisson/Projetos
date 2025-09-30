// funcoes.js — versão: salvar JSON por aba / arquivo conforme solicitado
import fs from "fs";
import fsPromises from "fs/promises";
import path from "path";
import csv from "csv-parser";
import xlsx from "xlsx";

/**
 * Normaliza um nome de arquivo/aba para ser seguro no sistema de arquivos.
 */
function safeName(name = "") {
  return name
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "") // remove acentos
    .replace(/[\/\\:*?"<>|]/g, "_")  // caracteres inválidos em nomes de arquivo
    .replace(/\s+/g, "_")
    .replace(/__+/g, "_")
    .trim();
}

/**
 * Lê um CSV e, se export_json=true, salva o JSON.
 * - Se for um único CSV, salva: <basename>.json
 *
 * @param {Object} opts
 *   - filePath: string (obrigatório)
 *   - separator: string (default ',')
 *   - export_json: boolean (default false)
 *   - jsonOutDir: string | null (diretório para salvar o JSON; default: mesma pasta do arquivo)
 * @returns {Promise<Array<Object>>} rows
 */
export function import_csv({ filePath = null, separator = ",", export_json = false, jsonOutDir = null } = {}) {
  return new Promise((resolve, reject) => {
    if (!filePath) return reject(new Error("filePath é obrigatório"));

    const results = [];
    try {
      const stream = fs.createReadStream(filePath);
      stream
        .pipe(csv({ separator }))
        .on("data", (data) => results.push(data))
        .on("end", async () => {
          try {
            if (export_json) {
              const outDir = jsonOutDir || path.dirname(filePath);
              if (!fs.existsSync(outDir)) await fsPromises.mkdir(outDir, { recursive: true });

              const base = path.basename(filePath).replace(/\.[^.]+$/, ""); // remove extensão
              const outFile = path.join(outDir, `${safeName(base)}.json`);
              await fsPromises.writeFile(outFile, JSON.stringify(results, null, 2), "utf8");
              console.log(`CSV -> JSON exportado: ${outFile}`);
            }
            resolve(results);
          } catch (err) {
            reject(err);
          }
        })
        .on("error", (err) => {
          console.error("Erro ao ler o arquivo CSV:", err);
          reject(err);
        });
    } catch (error) {
      console.error("Erro ao processar CSV:", error);
      reject(error);
    }
  });
}

/**
 * Lê múltiplos CSVs em série (salva um JSON por CSV se export_json=true).
 * Retorna um objeto { filePath: rowsArray, ... }
 */
export async function import_multiple_csv(filePaths = [], opts = {}) {
  const out = {};
  for (const fp of filePaths) {
    out[fp] = await import_csv({ filePath: fp, ...opts });
  }
  return out;
}

/**
 * Lê um XLSX:
 * - Se o workbook contém mais de 1 aba -> salva um JSON por aba: <basename>.<sheetName>.json
 * - Se contém exatamente 1 aba -> salva um único JSON: <basename>.json
 *
 * options:
 *  - filePath: string (obrigatório)
 *  - export_json: boolean (default false)
 *  - sheets: array|null -> se passado, filtra por esses nomes (case sensitive)
 *  - jsonOutDir: string|null -> diretório destino para os JSONs (default: mesma pasta do arquivo)
 *
 * Retorna: objeto { sheetName: rows[] } com todas as abas lidas (ou somente as requisitadas).
 */
export function import_xlsx({ filePath = null, export_json = false, sheets = null, jsonOutDir = null } = {}) {
  if (!filePath) throw new Error("filePath é obrigatório");

  // importante: cellDates:true faz com que células com formato de data sejam lidas como Date objects
  const workbook = xlsx.readFile(filePath, { cellDates: true });

  const allSheetNames = workbook.SheetNames || [];
  const toRead = Array.isArray(sheets) && sheets.length
    ? allSheetNames.filter(n => sheets.includes(n))
    : allSheetNames;

  const result = {};

  toRead.forEach(sheetName => {
    const sheet = workbook.Sheets[sheetName];
    if (!sheet) {
      result[sheetName] = [];
      return;
    }

    // raw:false aplica formatação; dateNF define o formato de saída das datas (YYYY-MM-DD)
    // defval:null evita cells undefined
    const rows = xlsx.utils.sheet_to_json(sheet, { defval: null, raw: false, dateNF: 'yyyy-mm-dd' });

    result[sheetName] = rows;
  });

  // salvar JSON(s) conforme regra pedida
  if (export_json) {
    const outDir = jsonOutDir || path.dirname(filePath);
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

    const base = path.basename(filePath).replace(/\.[^.]+$/, ""); // nome do arquivo sem extensão

    if (toRead.length <= 1) {
      // apenas 1 aba (ou nenhuma) -> salvar <basename>.json
      const singleSheetName = toRead[0] || allSheetNames[0] || "sheet";
      const rows = result[singleSheetName] || [];
      const outFile = path.join(outDir, `${safeName(base)}.json`);
      fs.writeFileSync(outFile, JSON.stringify(rows, null, 2), "utf8");
      console.log(`XLSX -> JSON exportado (única aba) -> ${outFile}`);
    } else {
      // múltiplas abas -> um arquivo por aba: <basename>.<sheetName>.json
      for (const sheetName of toRead) {
        const rows = result[sheetName] || [];
        const safeSheet = safeName(sheetName || "sheet");
        const outFile = path.join(outDir, `${safeName(base)}.${safeSheet}.json`);
        fs.writeFileSync(outFile, JSON.stringify(rows, null, 2), "utf8");
        console.log(`XLSX -> JSON exportado (aba) -> ${outFile}`);
      }
    }
  }

  console.log(`XLSX lido com sucesso: ${filePath} (abas lidas: ${toRead.join(", ")})`);
  return result;
}

/**
 * Lê múltiplos XLSX (array de paths).
 * Para cada arquivo aplica a regra de salvar JSONs por aba/arquivo.
 * Retorna objeto { filePath: { sheetName: rows[] } }
 */
export async function import_multiple_xlsx(filePaths = [], opts = {}) {
  const out = {};
  for (const fp of filePaths) {
    out[fp] = import_xlsx({ filePath: fp, ...opts });
  }
  return out;
}