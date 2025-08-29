# Homepage Development

## Instructions:
    - Following is the expected outcome for the Homepage Functionality.
    - Some of the functionality is already done
    - Read code in the file before making changes

## Files To Use/Modify
    - Home.vue -- Path: dppl_mes/frontend/src/pages/Home.vue
    - NavBar.vue -- Path: dppl_mes/frontend/src/components/NavBar.vue
    - HomePageControls.vue -- Path: dppl_mes/frontend/src/components/HomePageControls.vue
    - FactoryFloorMap.vue -- Path: dppl_mes/frontend/src/components/FactoryFloorMap.vue
    - DashboardComponent.vue -- Path: dppl_mes/frontend/src/components/DashboardComponent.vue
    - MachineCard.vue -- Path: dppl_mes/frontend/src/components/MachineCard.vue
    - FactoryFilter.vue -- Path: dppl_mes/frontend/src/components/FactoryFilter.vue
    - Machine.vue -- Path: dppl_mes/frontend/src/pages/Machine.vue
    - router.js -- Path: dppl_mes/frontend/src/router.js
    - api.py -- Path: dppl_mes/dppl_mes/api.py

## Expected Outcomes:
    1. Have following components:
        - Navbar
        - Homepage
        - Homepage Controls Bar
            - Factory Filter
            - Dashboard Switcher
        - Homepage Section

    2. Fetch & Update Factory List:
        - Fetch Factory List From 'Factory' DocType from the backend with following params:
            - Filter: is_active == 1
            - Fields: name, factory_name, floor_plan
        - Append the name in Factory Filter
        - Fetch Default Factory from Organization Settings & Select/Update in the Factory List

    3. Fetch & Update Area List:
        - Fetch All Areas From Area DocType with following params:
            - Fields: name, area_name, factory, sequence_number

    4. Fetch & Update Machine List:
        - Fetch All Machines From Machine DocType For All Factories In The Factory List With Following Params
            - Fields: name, machine_name, is_active, area, sequence_number, machine_image

    5. Build/Update Factory Floor Map:
        - In FactoryFloorMap.vue file render machine_image SVG
        - Make The SVG take 100% of the View Port Width while having some padding on all sides
        - The SVG path of each machine where the id of the path is same as name of Machine. example:
            In SVG: <path id="XL-D" d="M29 21V79H11V21H29Z" fill="#808080" stroke="black" stroke-width="2"/>
            In Backend: Machine Name is XL-D
        - Connect the path in the SVG with the machine from backend
        - If for a path there is not machine found then fill that path with gray color
        - In api.py there is a realtime event called job_metrics_update under create_telemetry(). Use that event to update te SVG as following:
            - if run_rate_indicator == 1 then green else red
        - If a user clicks on the machine path open a overlay/popup to show:
            - Job Name
            - Job Number
            - Target Quantity
            - Completed Quantity
            - Button That Will Take Them To Machine Details Page (Machine.vue)
        - if a user clicks anywhere else then close the overlay/popup
    
# Fixes
## Requirement:
- Need to Fix The Realtime Update Of Job Metrics in FactoryFloorMap.vue
- Currently the socket connection is not working properly. Here is the output from the terminal:
    [vite] connecting... client:495:9
    [vite] connected. client:614:15
    Initializing socket connection to: ws://dppl.localhost:9000/dppl socket.js:23:10
    Site name: dppl Port: 9000 socket.js:24:10
    Socket connection error: Invalid namespace undefined socket.js:40:11
    Attempting to reconnect... socket.js:41:11
    Initializing socket connection to: ws://dppl.localhost:9000/dppl socket.js:23:10
    Site name: dppl Port: 9000 socket.js:24:10
    Initializing socket connection to: ws://dppl.localhost:9000/dppl socket.js:23:10
    Site name: dppl Port: 9000 socket.js:24:10
    🔧 Socket listeners setup completed. Testing connection... FactoryFloorMap.vue:245:10
    ⚠️  Socket is not connected yet FactoryFloorMap.vue:249:11
    Socket connection error: Invalid namespace undefined socket.js:40:11
    Attempting to reconnect... socket.js:41:11
    Socket connection error: Invalid namespace undefined socket.js:40:11
    Attempting to reconnect... socket.js:41:11

- Here is an example code from a frappe application called gameplan:
    URL of the code example: https://github.com/frappe/gameplan/blob/9f9332cf29496afe5e912e4f1734fbf1142cb18c/frontend/src/socket.js#L13

    Path: frontend/src/socket.js

    Code:
    import { io } from 'socket.io-client'
    import { socketio_port } from '../../../../sites/common_site_config.json'
    import { getCachedListResource } from 'frappe-ui/src/resources/listResource'
    import { getCachedResource } from 'frappe-ui/src/resources/resources'

    export function initSocket() {
    let host = window.location.hostname
    let siteName = window.site_name
    let port = window.location.port ? `:${socketio_port}` : ''
    let protocol = port ? 'http' : 'https'
    let url = `${protocol}://${host}${port}/${siteName}`

    let socket = io(url, {
        withCredentials: true,
        reconnectionAttempts: 5,
    })
    socket.on('refetch_resource', (data) => {
        if (data.cache_key) {
        let resource =
            getCachedResource(data.cache_key) ||
            getCachedListResource(data.cache_key)
        if (resource) {
            resource.reload()
        }
        }
    })
    return socket
    }

- Files to focus on:
    - FactoryFloorMap.vue -- Path: dppl_mes/frontend/src/components/FactoryFloorMap.vue
    - socket.js -- Path: dppl_mes/frontend/src/socket.js

First create a To Do List Before starting code editing & development.

The Code is still not working correctly... Here is more code from gameplan application

Socket.js Code:
import { io } from 'socket.io-client'
import { socketio_port } from '../../../../sites/common_site_config.json'
import { getCachedListResource } from 'frappe-ui/src/resources/listResource'
import { getCachedResource } from 'frappe-ui/src/resources/resources'

export function initSocket() {
  let host = window.location.hostname
  let siteName = window.site_name
  let port = window.location.port ? `:${socketio_port}` : ''
  let protocol = port ? 'http' : 'https'
  let url = `${protocol}://${host}${port}/${siteName}`

  let socket = io(url, {
    withCredentials: true,
    reconnectionAttempts: 5,
  })
  socket.on('refetch_resource', (data) => {
    if (data.cache_key) {
      let resource =
        getCachedResource(data.cache_key) ||
        getCachedListResource(data.cache_key)
      if (resource) {
        resource.reload()
      }
    }
  })
  return socket
}

code from main.js
import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createDialog } from './utils/dialogs'
import { initSocket } from './socket'
import router from './router'
import translationPlugin from './translation'
import { posthogPlugin } from './telemetry'
import App from './App.vue'

import {
  FrappeUI,
  Button,
  Input,
  TextInput,
  FormControl,
  ErrorMessage,
  Dialog,
  Alert,
  Badge,
  setConfig,
  frappeRequest,
  FeatherIcon,
} from 'frappe-ui'

let globalComponents = {
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
let pinia = createPinia()

let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)
app.use(FrappeUI)
app.use(pinia)
app.use(router)
app.use(translationPlugin)
app.use(posthogPlugin)
for (let key in globalComponents) {
  app.component(key, globalComponents[key])
}

app.config.globalProperties.$dialog = createDialog

let socket
if (import.meta.env.DEV) {
  frappeRequest({ url: '/api/method/crm.www.crm.get_context_for_dev' }).then(
    (values) => {
      for (let key in values) {
        window[key] = values[key]
      }
      socket = initSocket()
      app.config.globalProperties.$socket = socket
      app.mount('#app')
    },
  )
} else {
  socket = initSocket()
  app.config.globalProperties.$socket = socket
  app.mount('#app')
}

if (import.meta.env.DEV) {
  window.$dialog = createDialog
}

See if we have made some errors in our implementation and create a plan to fix it