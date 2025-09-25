# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Factory(Document):
	def on_update(self):
		"""
		Logic: Whenever the document is updated do the following on self.supervisors field
		- if a user is added in the field then create a new record in User Permission DocType Where:
			- user is self.supervisors user
			- allow is 'Factory'
			- for_value is 'self'
			- apply_to_all_doctypes is true
		- if a user is removed from the then delete the coorsponding record from User Permission DocType
		"""
		self.manage_supervisors_permissions()

	def manage_supervisors_permissions(self):
		"""Manage User Permissions based on changes to supervisors field"""
		# Get current factory heads
		current_users = set()
		for row in self.supervisors:
			if row.user:
				current_users.add(row.user)

		# Get previous factory heads from database
		previous_users = set()
		if not self.is_new():
			doc_before_save = self.get_doc_before_save()
			if doc_before_save and doc_before_save.supervisors:
				for row in doc_before_save.supervisors:
					if row.user:
						previous_users.add(row.user)

		# Find users to add and remove
		users_to_add = current_users - previous_users
		users_to_remove = previous_users - current_users

		# Add permissions for new users
		for user in users_to_add:
			self.create_user_permission(user)

		# Remove permissions for removed users
		for user in users_to_remove:
			self.delete_user_permission(user)

	def create_user_permission(self, user):
		"""Create User Permission record for factory access"""
		try:
			# Check if permission already exists
			existing = frappe.db.exists("User Permission", {
				"user": user,
				"allow": "Factory",
				"for_value": self.name
			})

			if not existing:
				user_permission = frappe.get_doc({
					"doctype": "User Permission",
					"user": user,
					"allow": "Factory",
					"for_value": self.name,
					"apply_to_all_doctypes": 1
				})
				user_permission.insert(ignore_permissions=True)
				frappe.db.commit()

		except Exception as e:
			frappe.log_error(f"Error creating User Permission for user {user}: {str(e)}")

	def delete_user_permission(self, user):
		"""Delete User Permission record for factory access"""
		try:
			existing_permissions = frappe.get_list("User Permission", {
				"user": user,
				"allow": "Factory",
				"for_value": self.name
			}, pluck="name")

			for permission_name in existing_permissions:
				frappe.delete_doc("User Permission", permission_name, ignore_permissions=True)

			if existing_permissions:
				frappe.db.commit()

		except Exception as e:
			frappe.log_error(f"Error deleting User Permission for user {user}: {str(e)}")