// utils/normalizeKeys.js
export function normalizeKeys(input) {
  const clean = (key) =>
    String(key)
      .replace(/^\uFEFF/, "")
      .replace(/^"+|"+$/g, "")
      .replace(/^\\"|\\"$/g, "")
      .replace(/^"|"$|/g, ""); // mantém sua limpeza original

  // 1) Array de linhas
  if (Array.isArray(input)) {
    return input.map((obj) => {
      const newObj = {};
      for (const key in obj) {
        if (!Object.prototype.hasOwnProperty.call(obj, key)) continue;
        newObj[clean(key)] = obj[key];
      }
      return newObj;
    });
  }

  // 2) Objeto de abas { Aba1: [...], Aba2: [...] }
  if (input && typeof input === "object") {
    const out = {};
    for (const [sheetName, rows] of Object.entries(input)) {
      out[sheetName] = Array.isArray(rows) ? normalizeKeys(rows) : rows;
    }
    return out;
  }

  // 3) Qualquer outro tipo: retorna como veio
  return input;
}


// utils/ppcPactoNormalizer.js
// Normaliza linhas do "PPC_PACTO Tree Monitoring" para o formato esperado
// pelo kb_ppcPactoImporter.js (CERT).

const clean = (v) =>
  v === undefined || v === null ? null : String(v).trim() || null;

const getVal = (row, keys = []) => {
  for (const k of keys) {
    if (Object.prototype.hasOwnProperty.call(row, k)) {
      const v = row[k];
      if (v !== undefined && v !== null && String(v).trim() !== "") return v;
    }
  }
  return null;
};

/**
 * Converte uma linha do PPC_PACTO → linha compatível com kb_ppcPactoImporter.
 * Saída usa *exatamente* as chaves que seu importador já consome.
 */
export function normalizePPCPACTORow(row) {
  return {
    _uuid: clean(getVal(row, ["_uuid", "uuid", "instanceID", "instance_id"])),

    "ID do Sítio": clean(
      getVal(row, ["ID do Sítio", "plot_id", "plotID", "Plot ID", "id_sitio"])
    ),
    "Tipo do Sítio": clean(
      getVal(row, ["Tipo do Sítio", "site_type", "Tipo do sitio"])
    ),
    "Selecione seu País": clean(
      getVal(row, ["Selecione seu País", "country", "país", "pais"])
    ),
    "Período de Amostragem": clean(
      getVal(row, ["Período de Amostragem", "sampling_period", "periodo", "Período"])
    ),
    "Insira uma data": clean(getVal(row, ["Insira uma data", "date", "data"])),
    "Hora de Início": clean(
      getVal(row, ["Hora de Início", "start", "hora_inicio", "start_time"])
    ),
    "Hora de Fim": clean(
      getVal(row, ["Hora de Fim", "end", "hora_fim", "end_time"])
    ),
    "Observações": clean(getVal(row, ["Observações", "notes", "obs", "Observacoes"])),

    // Campos opcionais – seu importador aceita null
    "Nome do Responsável pela Coleta": clean(
      getVal(row, [
        "Nome do Responsável pela Coleta",
        "responsavel",
        "collector_name",
        "nome_responsavel",
      ])
    ),
    "Nome da Organização": clean(
      getVal(row, [
        "Nome da Organização",
        "organization",
        "organizacao",
        "org",
        "Nome da Organizacao",
      ])
    ),
  };
}

/**
 * Normaliza um array de linhas do PPC_PACTO.
 */
export function normalizePPCPACTO(rows = []) {
  return rows.map(normalizePPCPACTORow);
}
