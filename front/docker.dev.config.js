import { defineConfig } from "vite";

export default defineConfig({
    server: {
        host: true,
        watch: {
          usePolling: true
        },
        hmr: {
           port: 8021,
        },
    },
    plugins: [
    {
      name: "client-host",
      transform(code, id) {
        console.log('transform',id)
        // if (
        //   id.endsWith("dist/client/client.mjs") ||
        //   id.endsWith("dist/client/env.mjs")
        // ) {
        //   return code.replace(
        //     "__HMR_HOSTNAME__",
        //     JSON.stringify("http://localhost:8015")
        //   );
        // }

        // return code;
      },
    },
  ], 
});