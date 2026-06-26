chrome.runtime.onMessage.addListener((e,o,t)=>{if(console.log("[EXT] content script carregado"),e?.type==="GET_SELECTION"){const n=window.getSelection()?.toString()??"";return t({selection:n}),!0}});
