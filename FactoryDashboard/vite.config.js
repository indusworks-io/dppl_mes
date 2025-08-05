import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import frappeui from 'frappe-ui/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    frappeui()
  ],
  optimizeDeps: {
		include: [
			'feather-icons',
			'engine.io-client',
			'tailwind.config.js',
      'interactjs',
		],
	},
  resolve: {
    alias: {
      'highlight.js/lib/core': 'highlight.js',
    },
  },
  build:{
    outDir: "../dppl_mes/public/frontend",
    emptyOutDir: true,
  }
})
