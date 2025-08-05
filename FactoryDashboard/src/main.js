import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Import the router instance
import VueKonva from 'vue-konva'
import { FrappeUI, setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui'

const app = createApp(App)
setConfig('resourceFetcher', frappeRequest)

// app.use(FrappeUI)
app.use(resourcesPlugin) // Use the resources plugin


app.use(router) // Use the router
app.use(VueKonva)
app.mount('#app')
