# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Area(Document):
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
		"""Manage User Permissions based on changes to supervisors field and factory assignment"""
		# Get current supervisors
		current_users = set()
		for row in self.supervisors:
			if row.user:
				current_users.add(row.user)

		# Get previous data from database
		previous_users = set()
		previous_factory = None
		if not self.is_new():
			doc_before_save = self.get_doc_before_save()
			if doc_before_save:
				previous_factory = doc_before_save.factory
				if doc_before_save.supervisors:
					for row in doc_before_save.supervisors:
						if row.user:
							previous_users.add(row.user)

		# Check if factory has changed
		factory_changed = previous_factory != self.factory

		# Find users to add and remove
		users_to_add = current_users - previous_users
		users_to_remove = previous_users - current_users
		users_unchanged = current_users & previous_users

		# Handle factory change for existing users
		if factory_changed and users_unchanged:
			for user in users_unchanged:
				# Remove old factory permissions
				if previous_factory:
					self.remove_factory_permission(user, previous_factory)
				# Add new factory permissions
				if self.factory:
					self.add_factory_permission(user, self.factory)

		# Add permissions for new users
		for user in users_to_add:
			self.create_user_permission(user)

		# Remove permissions for removed users
		for user in users_to_remove:
			self.delete_user_permission_for_previous_factory(user, previous_factory)

	def create_user_permission(self, user):
		"""Create User Permission records for both Area and Factory access"""
		try:
			# Create Area permission
			existing_area = frappe.db.exists("User Permission", {
				"user": user,
				"allow": "Area",
				"for_value": self.name
			})

			if not existing_area:
				area_permission = frappe.get_doc({
					"doctype": "User Permission",
					"user": user,
					"allow": "Area",
					"for_value": self.name,
					"apply_to_all_doctypes": 1
				})
				area_permission.insert(ignore_permissions=True)

			# Create Factory permission for the assigned factory
			if self.factory:
				existing_factory = frappe.db.exists("User Permission", {
					"user": user,
					"allow": "Factory",
					"for_value": self.factory
				})

				if not existing_factory:
					factory_permission = frappe.get_doc({
						"doctype": "User Permission",
						"user": user,
						"allow": "Factory",
						"for_value": self.factory,
						"apply_to_all_doctypes": 1
					})
					factory_permission.insert(ignore_permissions=True)

			frappe.db.commit()

		except Exception as e:
			frappe.log_error(f"Error creating User Permission for user {user}: {str(e)}")

	def delete_user_permission(self, user):
		"""Delete User Permission records for both Area and Factory access"""
		try:
			# Delete Area permissions
			existing_area_permissions = frappe.get_list("User Permission", {
				"user": user,
				"allow": "Area",
				"for_value": self.name
			}, pluck="name")

			for permission_name in existing_area_permissions:
				frappe.delete_doc("User Permission", permission_name, ignore_permissions=True)

			# Delete Factory permissions for this area's factory
			if self.factory:
				existing_factory_permissions = frappe.get_list("User Permission", {
					"user": user,
					"allow": "Factory",
					"for_value": self.factory
				}, pluck="name")

				for permission_name in existing_factory_permissions:
					frappe.delete_doc("User Permission", permission_name, ignore_permissions=True)

			if existing_area_permissions or (self.factory and existing_factory_permissions):
				frappe.db.commit()

		except Exception as e:
			frappe.log_error(f"Error deleting User Permission for user {user}: {str(e)}")

	def remove_factory_permission(self, user, factory):
		"""Remove Factory permission for a specific factory"""
		try:
			if factory:
				existing_factory_permissions = frappe.get_list("User Permission", {
					"user": user,
					"allow": "Factory",
					"for_value": factory
				}, pluck="name")

				for permission_name in existing_factory_permissions:
					frappe.delete_doc("User Permission", permission_name, ignore_permissions=True)

				if existing_factory_permissions:
					frappe.db.commit()

		except Exception as e:
			frappe.log_error(f"Error removing Factory permission for user {user}, factory {factory}: {str(e)}")

	def add_factory_permission(self, user, factory):
		"""Add Factory permission for a specific factory"""
		try:
			if factory:
				existing = frappe.db.exists("User Permission", {
					"user": user,
					"allow": "Factory",
					"for_value": factory
				})

				if not existing:
					factory_permission = frappe.get_doc({
						"doctype": "User Permission",
						"user": user,
						"allow": "Factory",
						"for_value": factory,
						"apply_to_all_doctypes": 1
					})
					factory_permission.insert(ignore_permissions=True)
					frappe.db.commit()

		except Exception as e:
			frappe.log_error(f"Error adding Factory permission for user {user}, factory {factory}: {str(e)}")

	def delete_user_permission_for_previous_factory(self, user, previous_factory):
		"""Delete User Permission records for both Area and specific previous Factory"""
		try:
			# Delete Area permissions
			existing_area_permissions = frappe.get_list("User Permission", {
				"user": user,
				"allow": "Area",
				"for_value": self.name
			}, pluck="name")

			for permission_name in existing_area_permissions:
				frappe.delete_doc("User Permission", permission_name, ignore_permissions=True)

			# Delete Factory permissions for the previous factory
			if previous_factory:
				existing_factory_permissions = frappe.get_list("User Permission", {
					"user": user,
					"allow": "Factory",
					"for_value": previous_factory
				}, pluck="name")

				for permission_name in existing_factory_permissions:
					frappe.delete_doc("User Permission", permission_name, ignore_permissions=True)

			if existing_area_permissions or (previous_factory and existing_factory_permissions):
				frappe.db.commit()

		except Exception as e:
			frappe.log_error(f"Error deleting User Permission for user {user}, previous factory {previous_factory}: {str(e)}")
