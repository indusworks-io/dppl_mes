import "./index.css"

import { createPinia } from "pinia"
import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"
import { initSocket } from "./socket"
import { posthogPlugin } from "./telemetry"
import translationPlugin from "./translation"
import { createDialog } from "./utils/dialogs"

import {
	Alert,
	Badge,
	Button,
	Dialog,
	ErrorMessage,
	FeatherIcon,
	FormControl,
	FrappeUI,
	Input,
	TextInput,
	frappeRequest,
	setConfig,
} from "frappe-ui"

const globalComponents = {
	Button,
	TextInput,
	Input,
	FormControl,
	ErrorMessage,
	Dialog,
	Alert,
	Badge,
	FeatherIcon,
}

// create a pinia instance
const pinia = createPinia()

const app = createApp(App)

setConfig("resourceFetcher", frappeRequest)
app.use(FrappeUI)
app.use(pinia)
app.use(router)
app.use(translationPlugin)
app.use(posthogPlugin)
for (const key in globalComponents) {
	app.component(key, globalComponents[key])
}

app.config.globalProperties.$dialog = createDialog

let socket
if (import.meta.env.DEV) {
	frappeRequest({ url: "/api/method/crm.www.crm.get_context_for_dev" }).then(
		(values) => {
			for (const key in values) {
				window[key] = values[key]
			}
			socket = initSocket()
			app.config.globalProperties.$socket = socket
			app.mount("#app")
		},
	)
} else {
	socket = initSocket()
	app.config.globalProperties.$socket = socket
	app.mount("#app")
}

if (import.meta.env.DEV) {
	window.$dialog = createDialog
}
