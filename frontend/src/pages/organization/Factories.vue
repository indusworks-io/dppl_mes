<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Factories</h1>
      <p class="text-gray-600">Manage factory locations and configurations</p>
    </div>

    <div v-if="factories.loading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p class="text-gray-600">Loading factories...</p>
      </div>
    </div>

    <div v-else-if="factories.error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-800">Error loading factories: {{ factories.error }}</p>
    </div>

    <div v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Factories</p>
              <p class="text-2xl font-semibold text-gray-900">{{ factories.data?.length || 0 }}</p>
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
              <p class="text-sm font-medium text-gray-600">Active</p>
              <p class="text-2xl font-semibold text-gray-900">{{ activeFactoriesCount }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Locations</p>
              <p class="text-2xl font-semibold text-gray-900">{{ uniqueLocations }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Factories Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="factory in factories.data"
          :key="factory.name"
          class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
        >
          <div class="p-6">
            <div class="flex items-start justify-between mb-4">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">
                  {{ factory.factory_name || factory.name }}
                </h3>
                <p class="text-sm text-gray-500">{{ factory.name }}</p>
              </div>
              <span :class="factory.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                    class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                {{ factory.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>

            <div class="space-y-2 text-sm text-gray-600">
              <div class="flex items-center" v-if="factory.location">
                <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                {{ factory.location }}
              </div>

              <div class="flex items-center" v-if="factory.contact_person">
                <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                {{ factory.contact_person }}
              </div>

              <div class="flex items-center" v-if="factory.phone">
                <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                </svg>
                {{ factory.phone }}
              </div>
            </div>

            <div class="mt-4 pt-4 border-t border-gray-100">
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-500">Created:</span>
                <span class="text-gray-900">{{ formatDate(factory.creation) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!factories.data || factories.data.length === 0" class="col-span-full">
          <div class="text-center py-12">
            <svg class="mx-auto w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No factories found</h3>
            <p class="mt-1 text-sm text-gray-500">Factory configurations will appear here when created.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createListResource } from "frappe-ui"
import { computed } from "vue"

const factories = createListResource({
	doctype: "Factory",
	fields: [
		"name",
		"factory_name",
		"location",
		"contact_person",
		"phone",
		"email",
		"is_active",
		"creation",
	],
	orderBy: "creation desc",
	pageLength: 50,
	auto: true,
})

const activeFactoriesCount = computed(() => {
	if (!factories.data) return 0
	return factories.data.filter((factory) => factory.is_active).length
})

const uniqueLocations = computed(() => {
	if (!factories.data) return 0
	const locations = [
		...new Set(factories.data.filter((f) => f.location).map((f) => f.location)),
	]
	return locations.length
})

const formatDate = (dateString) => {
	if (!dateString) return "N/A"
	try {
		return new Date(dateString).toLocaleDateString("en-GB")
	} catch {
		return "Invalid Date"
	}
}
</script>