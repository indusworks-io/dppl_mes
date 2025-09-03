import { createApp } from "vue"

import { initSocket } from "./socket"
import App from "./App.vue"
import router from "./router"

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

async function setupAppContext() {
	try {
		const values = await frappeRequest({ url: "/api/method/dppl_mes.api.get_context_for_dev" })
		
		for (const key in values) {
			window[key] = values[key]
		}
		
		socket = initSocket()
		app.config.globalProperties.$socket = socket
		app.mount("#app")
	} catch (error) {
		console.error("Failed to setup app context:", error)
	}
}

setupAppContext()