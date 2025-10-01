import { createResource } from 'frappe-ui'

export const userResource = createResource({
	url: 'frappe.auth.get_logged_user',
	cache: 'User',
	onError(error) {
		if (error && error.exc_type === 'AuthenticationError') {
			console.log('I was called from user.js')
			window.location.href = "/login?redirect-to=/frontend"
		}
	},
})

export const userDetailsResource = createResource({
	url: 'frappe.client.get_value',
	params: () => ({
		doctype: 'User',
		fieldname: ['first_name', 'last_name', 'full_name', 'email'],
		filters: { name: userResource.data }
	}),
	cache: 'UserDetails',
	onError(error) {
		console.error('Failed to load user details:', error)
	},
})