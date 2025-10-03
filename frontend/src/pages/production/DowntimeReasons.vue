<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Downtime Reasons</h1>
      <p class="text-gray-600">Manage downtime reason codes and categories</p>
    </div>

    <div v-if="reasons.loading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p class="text-gray-600">Loading downtime reasons...</p>
      </div>
    </div>

    <div v-else-if="reasons.error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-800">Error loading downtime reasons: {{ reasons.error }}</p>
    </div>

    <div v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Reasons</p>
              <p class="text-2xl font-semibold text-gray-900">{{ reasons.data?.length || 0 }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Categories</p>
              <p class="text-2xl font-semibold text-gray-900">{{ uniqueCategories }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Active Reasons</p>
              <p class="text-2xl font-semibold text-gray-900">{{ activeReasonsCount }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Downtime Reasons Table -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Downtime Reason Codes</h2>
        </div>

        <div v-if="!reasons.data || reasons.data.length === 0" class="p-8 text-center">
          <svg class="mx-auto w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No downtime reasons found</h3>
          <p class="mt-1 text-sm text-gray-500">Downtime reason codes will appear here when created.</p>
        </div>

        <div v-else class="overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reason Code</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usage Count</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="reason in reasons.data" :key="reason.name" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ reason.name }}
                </td>
                <td class="px-6 py-4 text-sm text-gray-500">
                  {{ reason.description || 'No description' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ reason.category || 'Uncategorized' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <span :class="getPriorityClass(reason.priority)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                    {{ reason.priority || 'Medium' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusClass(reason.is_active)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                    {{ reason.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ reason.usage_count || 0 }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createListResource } from "frappe-ui"
import { computed } from "vue"

const reasons = createListResource({
	doctype: "Downtime Reason",
	fields: [
		"name",
		"description",
		"category",
		"priority",
		"is_active",
		"usage_count",
		"creation",
	],
	orderBy: "creation desc",
	pageLength: 50,
	auto: true,
})

const activeReasonsCount = computed(() => {
	if (!reasons.data) return 0
	return reasons.data.filter((reason) => reason.is_active).length
})

const uniqueCategories = computed(() => {
	if (!reasons.data) return 0
	const categories = [
		...new Set(
			reasons.data.map((reason) => reason.category || "Uncategorized"),
		),
	]
	return categories.length
})

const getPriorityClass = (priority) => {
	if (!priority || priority === "Medium") return "bg-yellow-100 text-yellow-800"
	const priorityLower = priority.toLowerCase()

	if (priorityLower === "high" || priorityLower === "critical") {
		return "bg-red-100 text-red-800"
	} else if (priorityLower === "low") {
		return "bg-green-100 text-green-800"
	}
	return "bg-yellow-100 text-yellow-800"
}

const getStatusClass = (isActive) => {
	return isActive ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"
}
</script>