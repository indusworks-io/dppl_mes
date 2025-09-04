import { io } from "socket.io-client"
import { socketio_port } from "../../../../sites/common_site_config.json"

let socket = null
export function initSocket() {
	const host = window.location.hostname
	const siteName = window.site_name
	const port = window.location.port ? `:${socketio_port}` : ""
	const protocol = port ? "http" : "https"
	const url = `${protocol}://${host}${port}/${siteName}`

	socket = io(url, {
		withCredentials: true,
		reconnectionAttempts: 5,
	})
	return socket
}

export function useSocket() {
	return socket
}

// import { io } from "socket.io-client"
// import { socketio_port } from "../../../../sites/common_site_config.json"

// let socket = null

// export function initSocket() {
// 	const host = window.location.hostname
// 	const siteName = window.site_name || 'frontend'
// 	const isLocal = host.includes("localhost")
// 	const port = isLocal ? `:${socketio_port}` : ""
// 	const protocol = window.location.protocol
// 	const url = `${protocol}//${host}${port}/${siteName}`

// 	// Debug logs
// 	console.log("🔍 Socket Debug Info:")
// 	console.log("host:", host)
// 	console.log("siteName:", siteName)
// 	console.log("isLocal:", isLocal)
// 	console.log("socketio_port from config:", socketio_port)
// 	console.log("port (computed):", port)
// 	console.log("protocol:", protocol)
// 	console.log("Final Socket URL:", url)

// 	socket = io(url, {
// 		withCredentials: true,
// 		reconnectionAttempts: 5,
// 	})

// 	return socket
// }

// export function useSocket() {
// 	return socket
// }
