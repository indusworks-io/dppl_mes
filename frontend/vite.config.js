import path from "node:path"
import vue from "@vitejs/plugin-vue"
import frappeui from "frappe-ui/vite"
import { defineConfig } from "vite"
import { VitePWA } from "vite-plugin-pwa"

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		VitePWA({
			registerType: "autoUpdate",
			devOptions: {
				enabled: true,
				type: "module",
			},
			manifest: {
				name: "SoundSeal MES",
				short_name: "SoundSeal MES",
				icons: [
					{
						src: "android/android-launchericon-512-512.png",
						sizes: "512x512",
						type: "image/png",
						purpose: "any maskable",
					},
					{
						src: "android/android-launchericon-192-192.png",
						sizes: "192x192",
						type: "image/png",
						purpose: "any maskable",
					},
					{
						src: "android/android-launchericon-144-144.png",
						sizes: "144x144",
						type: "image/png",
						purpose: "any",
					},
					{
						src: "android/android-launchericon-96-96.png",
						sizes: "96x96",
						type: "image/png",
						purpose: "any",
					},
					{
						src: "android/android-launchericon-72-72.png",
						sizes: "72x72",
						type: "image/png",
						purpose: "any",
					},
					{
						src: "android/android-launchericon-48-48.png",
						sizes: "48x48",
						type: "image/png",
						purpose: "any",
					},
					{
						src: "ios/180.png",
						sizes: "180x180",
						type: "image/png",
						purpose: "any",
					},
					{
						src: "ios/152.png",
						sizes: "152x152",
						type: "image/png",
						purpose: "any",
					},
					{
						src: "ios/120.png",
						sizes: "120x120",
						type: "image/png",
						purpose: "any",
					},
				],
				start_url: "/frontend",
				display: "standalone",
				background_color: "#FFFFFF",
				theme_color: "#FFFFFF",
			},
			workbox: {
				maximumFileSizeToCacheInBytes: 6 * 1024 * 1024,
				runtimeCaching: [
					{
						urlPattern: /^https:\/\/jsonplaceholder\.typicode\.com\/.*/i,
						handler: "NetworkFirst",
						options: { cacheName: "api-cache" },
					},
				],
			},
		}),
		frappeui({
			frappeProxy: true,
			jinjaBootData: true,
			lucideIcons: true,
			buildConfig: {
				indexHtmlPath: "../dppl_mes/www/frontend.html",
				outDir: "../dppl_mes/public/frontend", // ✅ Added this
				emptyOutDir: true,
				sourcemap: true,
			},
		}),
		vue(),
	],
	build: {
		chunkSizeWarningLimit: 1500,
		outDir: "../dppl_mes/public/frontend",
		emptyOutDir: true,
		target: "es2015",
		sourcemap: true,
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"),
			"tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
		},
	},
	optimizeDeps: {
		include: ["feather-icons", "showdown", "highlight.js/lib/core"],
	},
	server: {
		allowedHosts: true,
	},
})
