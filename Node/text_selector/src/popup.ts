import { detectType } from "./detect";

async function getActiveTabId(): Promise<number> {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) throw new Error("Aba ativa não encontrada.");
  return tab.id;
}

async function readSelection() {
  const status = document.getElementById("status") as HTMLParagraphElement;
  status.textContent = "";

  const tabId = await getActiveTabId();

  const injectionResults = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => window.getSelection()?.toString() ?? ""
  });

  const result = injectionResults[0]?.result ?? "";
  const raw = (result ?? "").trim();

  const rawEl = document.getElementById("raw") as HTMLTextAreaElement;
  const typeEl = document.getElementById("type") as HTMLInputElement;
  const valueEl = document.getElementById("value") as HTMLInputElement;

  rawEl.value = raw;

  const detected = detectType(raw);
  typeEl.value = detected.type;
  valueEl.value = detected.value;

  status.textContent = raw ? "Seleção carregada." : "Nenhum texto selecionado.";
}

async function copyValue() {
  const valueEl = document.getElementById("value") as HTMLInputElement;
  await navigator.clipboard.writeText(valueEl.value || "");
  (document.getElementById("status") as HTMLParagraphElement).textContent =
    "Copiado para a área de transferência.";
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("refresh")?.addEventListener("click", () => readSelection().catch(console.error));
  document.getElementById("copy")?.addEventListener("click", () => copyValue().catch(console.error));
  readSelection().catch(() => {});
});
