import { createDocumentResource } from 'frappe-ui'

export const websiteSettingsResource = createDocumentResource({
	doctype: 'Website Settings',
	name: 'Website Settings',
	cache: 'WebsiteSettings',
	onError(error) {
		console.error('Failed to load website settings:', error)
	},
})