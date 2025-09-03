import { getCachedListResource } from "frappe-ui/src/resources/listResource"
import { getCachedResource } from "frappe-ui/src/resources/resources"
import { io } from "socket.io-client"

let socket = null

function getSitename() {
	if (typeof frappe !== "undefined" && frappe.boot?.sitename) {
		return frappe.boot.sitename
	}

	let sitename = window.location.hostname
	if (sitename.includes(":")) {
		sitename = sitename.split(":")[0]
	}

	console.log("🏠 Detected sitename:", sitename)
	return sitename
}

function joinFrappeRooms(socket) {
	socket.emit("join", "all")
	socket.emit("join", "doctype:Machine")
	socket.emit("join", "doctype:Telemetry")
	console.log("🏠 Joined Frappe rooms: all, doctype:Machine, doctype:Telemetry")
}

export function initSocket() {
	if (socket && socket.connected) return socket

	// Determine protocol (wss for HTTPS, ws for HTTP)
	const protocol = window.location.protocol === "https:" ? "wss" : "ws"

	// Determine socket.io port dynamically
	const socketio_port = frappe.boot?.socketio_port || 9000

	// Use current hostname for client connection
	let hostname = window.location.hostname

	// If you're using a dev DNS like frontend.localhost, map it to localhost for sockets
	if (hostname === "frontend.localhost") {
		hostname = "localhost"
	}

	// Build socket.io URL
	const url = `${protocol}://${hostname}:${socketio_port}/${getSitename()}`

	console.log("🔌 Initializing socket connection to:", url)

	socket = io(url, {
		withCredentials: true,
		reconnectionAttempts: 5,
		transports: ["websocket"], // Force WebSocket (optional, but avoids polling issues)
	})

	socket.on("connect", () => {
		console.log("✅ Socket connected successfully! ID:", socket.id)
		joinFrappeRooms(socket)
	})

	socket.on("connect_error", (error) => {
		console.error("❌ Socket connection error:", error.message)
	})

	socket.on("disconnect", (reason) => {
		console.log("🔌 Socket disconnected:", reason)
	})

	socket.on("reconnect", (attemptNumber) => {
		console.log("🔄 Socket reconnected after", attemptNumber, "attempts")
	})

	socket.on("refetch_resource", (data) => {
		if (data.cache_key) {
			const resource =
				getCachedResource(data.cache_key) || getCachedListResource(data.cache_key)
			if (resource) resource.reload()
		}
	})

	return socket
}

export function useSocket() {
	return socket
}
