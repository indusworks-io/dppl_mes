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
