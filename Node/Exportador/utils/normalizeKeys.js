export function normalizeKeys(data) {
  return data.map((obj) => {
    const newObj = {};
    for (const key in obj) {
      if (!Object.prototype.hasOwnProperty.call(obj, key)) continue;

      // remove BOM e aspas extras
      const cleanKey = key
        .replace(/^\uFEFF/, "") // remove BOM
        .replace(/^"+|"+$/g, "") // remove aspas no início/fim
        .replace(/^\\+"|\\+"$/g, "") // remove aspas escapadas
        .replace(/^\"|\"$/g, ""); // remove aspas duplas literais

      newObj[cleanKey] = obj[key];
    }
    return newObj;
  });
}
