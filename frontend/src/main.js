import { createApp } from "vue"

import App from "./App.vue"
import router from "./router"
import { initSocket } from "./socket"

import "./serviceWorkerRegister"

import {
	Alert,
	Badge,
	Button,
	Dialog,
	ErrorMessage,
	FormControl,
	Input,
	TextInput,
	frappeRequest,
	pageMetaPlugin,
	resourcesPlugin,
	setConfig,
} from "frappe-ui"

import "./index.css"

const globalComponents = {
	Button,
	TextInput,
	Input,
	FormControl,
	ErrorMessage,
	Dialog,
	Alert,
	Badge,
}

const app = createApp(App)

setConfig("resourceFetcher", frappeRequest)

app.use(router)
app.use(resourcesPlugin)
app.use(pageMetaPlugin)

for (const key in globalComponents) {
	app.component(key, globalComponents[key])
}

let socket
if (import.meta.env.DEV) {
	// In development, fetch context first, then initialize socket
	frappeRequest({
		url: "/api/method/dppl_mes.api.get_context_for_dev",
		type: "POST",
	})
		.then((values) => {
			// Set context values to window object, including frappe boot data
			for (const key in values) {
				window[key] = values[key]
			}

			// Set up frappe boot object for proper integration
			if (!window.frappe) {
				window.frappe = {}
			}
			window.frappe.boot = values

			console.log("✅ Development context loaded:", values)

			// Now initialize socket with proper context
			socket = initSocket()
			app.config.globalProperties.$socket = socket
			app.mount("#app")
		})
		.catch((error) => {
			console.error("❌ Failed to load development context:", error)
			// Fallback: mount without socket if context loading fails
			app.mount("#app")
		})
} else {
	// In production, context should already be available
	socket = initSocket()
	app.config.globalProperties.$socket = socket
	app.mount("#app")
}
