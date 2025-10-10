import { createApp } from "vue"

import App from "./App.vue"
import router from "./router"
import { initSocket } from "./socket"

import "./serviceWorkerRegister"

import {
	Alert,
	Autocomplete,
	Badge,
	Button,
	Dialog,
	ErrorMessage,
	FormControl,
	Input,
	Sidebar,
	TextInput,
	frappeRequest,
	pageMetaPlugin,
	resourcesPlugin,
	setConfig,
} from "frappe-ui"

import "./index.css"

const globalComponents = {
	Alert,
	Autocomplete,
	Badge,
	Button,
	Dialog,
	ErrorMessage,
	FormControl,
	Input,
	Sidebar,
	TextInput,
}

const app = createApp(App)

setConfig("resourceFetcher", frappeRequest)

app.use(router)
app.use(resourcesPlugin)
app.use(pageMetaPlugin)

const socket = initSocket()
app.config.globalProperties.$socket = socket

for (const key in globalComponents) {
	app.component(key, globalComponents[key])
}

app.mount("#app")

// Handle navigation messages from service worker (push notification clicks)
if ("serviceWorker" in navigator) {
	navigator.serviceWorker.addEventListener("message", (event) => {
		const { action, url } = event.data || {}

		if (action === "navigate" && url) {
			console.log("📍 Navigating from push notification to:", url)

			// Navigate using Vue Router
			// Remove /frontend prefix if present as router is already scoped to /frontend
			const routePath = url.replace(/^\/frontend/, "") || "/"
			router.push(routePath).catch((err) => {
				console.error("Navigation error:", err)
			})
		}
	})

	console.log("✅ Service worker message listener registered")
}
