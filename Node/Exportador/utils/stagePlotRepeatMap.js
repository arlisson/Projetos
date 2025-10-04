// importers/state/stagePlotRepeatMap.js
// Stage em memória para o repeat 30x30.
// Chave: `${submissionUuidLower}#${index}` → { parcelaId, especieId, tipoArvore }

const map = new Map();

/**
 * key: `${submissionUuidLower}#${index}`
 */
function makeKey(submissionUuid, index) {
  if (!submissionUuid || index === undefined || index === null) return null;
  return `${String(submissionUuid).toLowerCase()}#${String(index)}`;
}

export function setPlotRepeatStage(submissionUuid, index, payload) {
  const key = makeKey(submissionUuid, index);
  if (!key) return;
  map.set(key, { ...payload });
}

export function getPlotRepeatStage(submissionUuid, index) {
  const key = makeKey(submissionUuid, index);
  if (!key) return null;
  return map.get(key) ?? null;
}

export function clearPlotRepeatStage() {
  map.clear();
}
