import { io } from 'socket.io-client'
import { getCachedListResource } from 'frappe-ui/src/resources/listResource'
import { getCachedResource } from 'frappe-ui/src/resources/resources'
import { socketio_port } from '../../../../sites/common_site_config.json'

let socket = null

export function initSocket() {
  if (socket && socket.connected) {
    return socket
  }

  let host = window.location.hostname
  let siteName = 'frontend'
  let port = window.location.port ? `:${socketio_port}` : ''
  let protocol = port ? 'http' : 'https'
  let url = `${protocol}://${host}${port}/${siteName}`
  console.log(url)

  socket = io(url, {
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

export function useSocket() {
  return socket
}