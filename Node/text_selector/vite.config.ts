import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        popup: "public/popup.html",
        content: "src/content.ts"
      },
      output: {
        entryFileNames: (chunk) => (chunk.name === "content" ? "content.js" : "[name].js")
      }
    }
  },
  publicDir: "public"
});
