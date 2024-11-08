// vite.config.js
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import path from "path";

export default defineConfig({
  plugins: [svelte()],
  build: {
    outDir: path.resolve(__dirname, "static/svelte-js"), // Adjust path to your Django app's static folder
    rollupOptions: {
      input: "./src/svelte-entry.js",
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
