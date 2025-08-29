import { io } from 'socket.io-client'
import { getCachedListResource } from 'frappe-ui/src/resources/listResource'
import { getCachedResource } from 'frappe-ui/src/resources/resources'

let socket = null

export function initSocket() {
  // Return existing socket if already connected
  if (socket && socket.connected) {
    return socket
  }

  let host = window.location.hostname
  let socketio_port = 9000  // Frappe socketio server port
  
  // Connect to Frappe socketio server without namespace (default namespace)
  let url = `http://${host}:${socketio_port}`

  console.log('🔌 Initializing socket connection to:', url)
  console.log('🏠 Host:', host, 'Port:', socketio_port)

  socket = io(url, {
    withCredentials: true,
    reconnectionAttempts: 5,
  })

  socket.on('connect', () => {
    console.log('✅ Socket connected successfully! ID:', socket.id)
  })

  socket.on('connect_error', (error) => {
    console.error('❌ Socket connection error:', error.message)
  })

  socket.on('disconnect', (reason) => {
    console.log('🔌 Socket disconnected:', reason)
  })

  socket.on('reconnect', (attemptNumber) => {
    console.log('🔄 Socket reconnected after', attemptNumber, 'attempts')
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

export function useSocket() {
  return socket
}