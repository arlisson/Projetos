// importers/state/stagePlotRepeatMap.js
// Stage em memória para o repeat 30x30.
// Chave: `${submissionUuidLower}#${index}` → { parcelaId, especieId, tipoArvore }

const stageMap = new Map();

function makeKey(submissionUuid, index) {
  if (submissionUuid == null || index == null) return null;
  return `${String(submissionUuid).toLowerCase()}#${String(index)}`;
}

/**
 * Armazena no stage os metadados do item do 30x30_Plot_Repeat.
 * payload esperado: { parcelaId:number, especieId:number, tipoArvore:string }
 */
export function setPlotRepeatStage(submissionUuid, index, payload) {
  const key = makeKey(submissionUuid, index);
  if (!key || !payload) return;
  stageMap.set(key, { ...payload });
}

/** Recupera o payload previamente salvo para (submissionUuid, index). */
export function getPlotRepeatStage(submissionUuid, index) {
  const key = makeKey(submissionUuid, index);
  if (!key) return null;
  return stageMap.get(key) ?? null;
}

/** Limpa todo o stage (útil entre arquivos ou ao fim do ETL). */
export function clearPlotRepeatStage() {
  stageMap.clear();
}

/** (Opcional) Tamanho atual do stage. */
export function stagePlotRepeatSize() {
  return stageMap.size;
}


const submissionToParcela = new Map();

export function setParcelaForSubmission(submissionKey, parcelaId) {
  if (submissionKey == null || parcelaId == null) return;
  submissionToParcela.set(String(submissionKey), Number(parcelaId));
}

export function getParcelaBySubmission(submissionKey) {
  if (submissionKey == null) return null;
  const key = String(submissionKey);
  const val = submissionToParcela.get(key);
  return val == null ? null : Number(val);
}

export function clearImportMap() {
  submissionToParcela.clear();
}

