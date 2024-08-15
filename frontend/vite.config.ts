import { defineConfig } from "vite";
import { fileURLToPath } from "url";

import vue from "@vitejs/plugin-vue";
import path from "path";
import dotenv from "dotenv";

dotenv.config({ path: path.resolve(__dirname, "../.env") });

const host: string = process.env.VITE_HOST || "127.0.0.1";
const port: string = process.env.VITE_PORT || "8000";
const protocol: string = process.env.VITE_PROTOCOL || "http";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@modules": fileURLToPath(new URL("./src/modules", import.meta.url)),
      "@assets": fileURLToPath(new URL("./src/assets", import.meta.url)),
    },
  },
  server: {
    proxy: {
      "/v1": {
        target: `${protocol}://${host}:${port}`,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/v1/, ""),
      },
    },
  },
});
