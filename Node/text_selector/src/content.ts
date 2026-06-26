chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
    console.log("[EXT] content script carregado");

  if (msg?.type === "GET_SELECTION") {
    const selection = window.getSelection()?.toString() ?? "";
    sendResponse({ selection });
    return true;
  }
});
