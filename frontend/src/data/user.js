import { createResource } from "frappe-ui"

export const userResource = createResource({
	url: "frappe.auth.get_logged_user",
	cache: "User",
	onError(error) {
		if (error && error.exc_type === "AuthenticationError") {
			window.location.href = "/login?redirect-to=/frontend"
		}
	},
})

export const userDetailsResource = createResource({
	url: "dppl_mes.api.get_current_user_details",
	cache: "UserDetails",
	auto: false,
	transform(data) {
		// Custom API returns { status: "success", data: { ... } }
		return data?.data || data
	},
	onError(error) {
		console.error("Failed to load user details:", error)
	},
})