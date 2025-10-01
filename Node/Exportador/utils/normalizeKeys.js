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
