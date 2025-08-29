import { io } from "socket.io-client"

let socket = null
export function initSocket() {
	// Don't initialize if already connected
	if (socket && socket.connected) {
		return socket
	}
	
	const host = window.location.hostname
	const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
	
	// Get site name from hostname or use default
	const siteName = host.split('.')[0] || 'dppl'
	
	// Get socketio port from boot config (default to 9000)
	const socketio_port = window.socketio_port || window.frappe?.boot?.socketio_port || 9000
	const port = socketio_port ? `:${socketio_port}` : ''
	
	// Construct URL with site name path like the working example
	const socketUrl = `${protocol}://${host}${port}/${siteName}`

	console.log('Initializing socket connection to:', socketUrl)
	console.log('Site name:', siteName, 'Port:', socketio_port)

	socket = io(socketUrl, {
		withCredentials: true,
		reconnectionAttempts: 10,
		reconnectionDelay: 1000,
		timeout: 20000,
		transports: ['websocket', 'polling'], // Allow fallback to polling if websocket fails
		forceNew: false, // Reuse existing connection if available
	})
	
	socket.on('connect', () => {
		console.log('Socket connected successfully', socket.id)
	})
	
	socket.on('connect_error', (error) => {
		console.error('Socket connection error:', error.message, error.type)
		console.log('Attempting to reconnect...')
	})
	
	socket.on('disconnect', (reason) => {
		console.log('Socket disconnected:', reason)
		if (reason === 'io server disconnect') {
			// The disconnection was initiated by the server, manually reconnect
			socket.connect()
		}
	})
	
	socket.on('reconnect', (attemptNumber) => {
		console.log('Socket reconnected after', attemptNumber, 'attempts')
	})
	
	socket.on('reconnect_failed', () => {
		console.error('Socket reconnection failed')
	})

	return socket
}

export function useSocket() {
	return socket
}
