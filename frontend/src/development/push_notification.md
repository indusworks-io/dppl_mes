You are an expert Vue 3 and Web Push developer.
My frontend app is a PWA built using Vite and Vue 3.
It already uses the `register-service-worker` package for service worker registration.
Your task: update the frontend to fully support **Web Push Notifications** 
integrated with a Frappe backend that uses `pywebpush`.

---

### 🧱 Backend context
The backend provides two API endpoints:

1. **Get VAPID Public Key**  
   `dppl_mes.api.get_vapid_public_key`

2. **Save Push Subscription**  
   `dppl_mes.api.save_push_subscription`  
   with form data:

### ⚙️ Requirements

#### 1️⃣ Update `/src/registerServiceWorker.js`

Keep the existing `register()` code from `register-service-worker`, but **extend it** as follows:

- After successful registration (`registered()` or `ready()` callbacks), 
add logic that:
1. Requests notification permission from the user:
  ```js
  const permission = await Notification.requestPermission()
  if (permission !== 'granted') {
    console.warn('Push permission not granted')
    return
  }
  ```
2. Fetches the public VAPID key:
  ```js
  const vapidPublicKey = await fetch('dppl_mes.api.get_vapid_public_key')
    .then(res => res.json())
    .then(data => data.message || data)
  ```
3. Converts the base64 public key to a `Uint8Array`:
  ```js
  function urlBase64ToUint8Array(base64String) { ... }
  ```
4. Subscribes to push notifications:
  ```js
  const subscription = await reg.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
  })
  ```
5. Sends the subscription JSON to Frappe:
  ```js example or use createdocumentresource from Frappe UI
  await fetch('dppl_mes.api.save_push_subscription', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `subscription_json=${encodeURIComponent(JSON.stringify(subscription.toJSON()))}`
  })
  console.log('Push subscription saved successfully!')
  ```
6. Add graceful error handling for each step.

- Ensure the new code runs **only in production** just like the rest of the script.

- Include proper logging messages (`console.log`, `console.error`) for clarity.

---

#### 2️⃣ Create or Update `/public/service-worker.js`

Extend the service worker with **push notification logic**.

Add the following event listeners:

```js
// Handle incoming push event
self.addEventListener('push', event => {
let data = {}
try {
 data = event.data.json()
} catch (e) {
 console.error('Push event data parsing failed', e)
}

const title = data.title || 'Notification'
const options = {
 body: data.body || '',
 data: data,
 tag: data.downtime_log || undefined,
 renotify: true
}

event.waitUntil(self.registration.showNotification(title, options))
})

// Handle notification click
self.addEventListener('notificationclick', event => {
event.notification.close()
const { url } = event.notification.data || {}

event.waitUntil(
 clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
   for (const client of clientList) {
     if ('focus' in client) {
       client.postMessage({ action: 'navigate', url })
       return client.focus()
     }
   }
   return clients.openWindow(url || '/')
 })
)
})
````

Keep any existing Workbox caching logic from VitePWA; just append this code.

---

#### 3️⃣ Update `/src/main.js`

At the end of your app initialization (after router is set up):

```js
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.addEventListener('message', event => {
    const { action, url } = event.data || {}
    if (action === 'navigate' && url) {
      router.push(url)
    }
  })
}
```

This ensures that when a notification is clicked,
the app navigates to the appropriate downtime log page (e.g. `/downtime/LOG-001`).

---

### 🧠 Development Notes

* Do **not** install Firebase — use only native `PushManager` + `Notification` APIs.
* Ensure that the `/public/service-worker.js` file is included in your Vite PWA build.
* Ensure that your app is served over HTTPS (required for Push API).
* Handle denied notification permissions gracefully (log and skip).
* Use async/await for clarity and proper error handling.

---

### 🎯 Deliverables

1. Updated **`/src/registerServiceWorker.js`** with integrated push subscription flow.
2. Updated **`/public/service-worker.js`** with push & click handlers.
3. Updated **`/src/main.js`** with message listener and router integration.
4. A short summary of how these files interact in runtime.

---

### ⚡ Before coding

Claude should:

* Read the existing `/src/registerServiceWorker.js` and `/public/service-worker.js` files to merge logic safely.
* Preserve the existing offline caching and update messages.
* Only add new push-related code.

After reviewing the files, generate the final code updates.