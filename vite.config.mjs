// vite.config.js
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import path from "path";

export default defineConfig({
  plugins: [svelte()],
  build: {
    outDir: path.resolve(__dirname, "staticfiles_build/static/svelte-js"), // Adjust path to your Django app's static folder
    rollupOptions: {
      input: {
        Dashboard: "./src/Dashboard-entry.js",
        AsistenDashboard: "./src/AsistenDashboard-entry.js",
      },
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "[name]-[hash].js",
        assetFileNames: "[name][extname]",
      },
      emptyOutDir: true,
    },
    watch: {
      usePolling: true, // Forces Vite to poll for changes (useful for certain environments)
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"), // Alias for easy imports if needed
    },
  },
  server: {
    port: 5173,
    strictPort: true,
    hmr: true,
  },
});
