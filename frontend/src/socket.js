import { getCachedListResource } from "frappe-ui/src/resources/listResource"
import { getCachedResource } from "frappe-ui/src/resources/resources"
import { io } from "socket.io-client"

let socket = null

// Function to dynamically detect Frappe sitename
function getSitename() {
	// Method 1: Try frappe.boot.sitename if available
	if (typeof frappe !== "undefined" && frappe.boot && frappe.boot.sitename) {
		return frappe.boot.sitename
	}

	// Method 2: Use hostname as sitename (common Frappe setup)
	let sitename = window.location.hostname

	// Method 3: If hostname has port, use just the hostname part
	if (sitename.includes(":")) {
		sitename = sitename.split(":")[0]
	}

	console.log("🏠 Detected sitename:", sitename)
	return sitename
}

// Function to join appropriate Frappe rooms
function joinFrappeRooms(socket) {
	// Join 'all' room for global broadcasts
	socket.emit("join", "all")

	// Join doctype rooms for machine-related events
	socket.emit("join", "doctype:Machine")
	socket.emit("join", "doctype:Telemetry")

	console.log("🏠 Joined Frappe rooms: all, doctype:Machine, doctype:Telemetry")
}

export function initSocket() {
	// Return existing socket if already connected
	if (socket && socket.connected) {
		return socket
	}

	const host = window.location.hostname
	const socketio_port = 9000 // Frappe socketio server port

	// Dynamically detect sitename for Frappe namespace
	const sitename = getSitename()
	const url = `http://${host}:${socketio_port}/${sitename}`

	console.log("🔌 Initializing socket connection to:", url)
	console.log("🏠 Host:", host, "Port:", socketio_port)

	socket = io(url, {
		withCredentials: true,
		reconnectionAttempts: 5,
	})

	socket.on("connect", () => {
		console.log("✅ Socket connected successfully! ID:", socket.id)

		// Join appropriate Frappe rooms for receiving events
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
				getCachedResource(data.cache_key) ||
				getCachedListResource(data.cache_key)
			if (resource) {
				resource.reload()
			}
		}
	})

	return socket
}

export function useSocket() {
	return socket
}
