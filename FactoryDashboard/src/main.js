
import { createApp } from 'vue'
import router from './router' // Import the router instance
import App from './App.vue'
import { setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui'

import VueKonva from 'vue-konva'


const app = createApp(App)
setConfig('resourceFetcher', frappeRequest)

// app.use(FrappeUI)
app.use(resourcesPlugin) // Use the resources plugin


app.use(router) // Use the router
app.use(VueKonva)
app.mount('#app')
