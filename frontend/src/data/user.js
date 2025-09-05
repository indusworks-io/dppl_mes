import router from '@/router'
import { createResource } from 'frappe-ui'

export const userResource = createResource({
	url: 'frappe.auth.get_logged_user',
	cache: 'User',
	onError(error) {
		if (error && error.exc_type === 'AuthenticationError') {
			console.log('I was called from user.js')
			router.push({ name: "Home" })
		}
	},
})