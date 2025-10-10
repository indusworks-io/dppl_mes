import { registerSW } from "virtual:pwa-register"
import { call } from "frappe-ui"

/**
 * Convert base64 VAPID public key to Uint8Array format required by Push API
 */
function urlBase64ToUint8Array(base64String) {
	const padding = "=".repeat((4 - (base64String.length % 4)) % 4)
	const base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/")
	const rawData = window.atob(base64)
	const outputArray = new Uint8Array(rawData.length)
	for (let i = 0; i < rawData.length; ++i) {
		outputArray[i] = rawData.charCodeAt(i)
	}
	return outputArray
}

/**
 * Subscribe to push notifications and save subscription to backend
 */
async function subscribeToPushNotifications(registration) {
	try {
		// Check if notifications are supported
		if (!("Notification" in window)) {
			console.warn("This browser does not support notifications")
			return
		}

		// Request notification permission
		const permission = await Notification.requestPermission()
		if (permission !== "granted") {
			console.warn("Push notification permission not granted")
			return
		}

		console.log("✅ Notification permission granted")

		// Fetch VAPID public key from backend
		console.log("📡 Fetching VAPID public key...")
		const vapidPublicKey = await call("dppl_mes.api.get_vapid_public_key")

		if (!vapidPublicKey) {
			console.error("❌ Failed to fetch VAPID public key")
			return
		}

		console.log("✅ VAPID public key received")

		// Subscribe to push notifications
		console.log("🔔 Subscribing to push notifications...")
		const subscription = await registration.pushManager.subscribe({
			userVisibleOnly: true,
			applicationServerKey: urlBase64ToUint8Array(vapidPublicKey),
		})

		console.log("✅ Push subscription successful")

		// Get device information for labeling
		const deviceLabel = `${navigator.userAgent.includes("Mobile") ? "Mobile" : "Desktop"} - ${new Date().toLocaleString()}`

		// Save subscription to backend
		console.log("💾 Saving push subscription to backend...")
		await call("dppl_mes.api.save_push_subscription", {
			subscription_json: JSON.stringify(subscription.toJSON()),
			device_label: deviceLabel,
		})

		console.log("✅ Push subscription saved successfully!")
	} catch (error) {
		console.error("❌ Error setting up push notifications:", error)
	}
}

const updateSW = registerSW({
	onNeedRefresh() {
		if (confirm("New content available. Reload?")) {
			updateSW(true)
		}
	},
	onOfflineReady() {
		console.log("App is ready for offline use.")
	},
	onRegisteredSW(swScriptUrl, registration) {
		console.log("Service worker registered:", swScriptUrl)

		// Set up push notifications after registration
		// Only in production and after user is logged in
		if (import.meta.env.PROD && registration) {
			// Small delay to ensure app is fully loaded
			setTimeout(() => {
				subscribeToPushNotifications(registration)
			}, 2000)
		}
	},
})
