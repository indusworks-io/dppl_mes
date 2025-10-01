<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Downtime Logs</h1>
      <p class="text-gray-600">Monitor machine downtime and analyze efficiency</p>
    </div>

    <div v-if="downtimeLogs.loading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p class="text-gray-600">Loading downtime logs...</p>
      </div>
    </div>

    <div v-else-if="downtimeLogs.error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-800">Error loading downtime logs: {{ downtimeLogs.error }}</p>
    </div>

    <div v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Events</p>
              <p class="text-2xl font-semibold text-gray-900">{{ downtimeLogs.data?.length || 0 }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Active Downtime</p>
              <p class="text-2xl font-semibold text-gray-900">{{ activeDowntimeCount }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Duration</p>
              <p class="text-2xl font-semibold text-gray-900">{{ totalDowntimeHours }}h</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Avg Duration</p>
              <p class="text-2xl font-semibold text-gray-900">{{ averageDowntimeMinutes }}m</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Downtime Logs Table -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Recent Downtime Events</h2>
        </div>

        <div v-if="!downtimeLogs.data || downtimeLogs.data.length === 0" class="p-8 text-center">
          <svg class="mx-auto w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No downtime events found</h3>
          <p class="mt-1 text-sm text-gray-500">Downtime logs will appear here when machines experience issues.</p>
        </div>

        <div v-else class="overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Machine</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Start Time</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">End Time</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duration</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reason</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="log in downtimeLogs.data" :key="log.name" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ log.machine || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDateTime(log.start_date_time) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDateTime(log.end_date_time) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDuration(log.duration) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ log.reason || 'Unknown' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusClass(log.status)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                    {{ log.status || 'Unknown' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <router-link
                    :to="`/downtime-log/${log.name}`"
                    class="text-blue-600 hover:text-blue-900 transition-colors"
                  >
                    View Details
                  </router-link>
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

const downtimeLogs = createListResource({
  doctype: "Downtime Log",
  fields: [
    "name",
    "machine",
    "start_date_time",
    "end_date_time",
    "duration",
    "reason",
    "status",
    "creation"
  ],
  orderBy: "creation desc",
  pageLength: 50,
  auto: true,
})

const activeDowntimeCount = computed(() => {
  if (!downtimeLogs.data) return 0
  return downtimeLogs.data.filter(log =>
    log.status === 'Active' || log.status === 'Ongoing' || !log.end_date_time
  ).length
})

const totalDowntimeHours = computed(() => {
  if (!downtimeLogs.data) return 0
  const totalSeconds = downtimeLogs.data.reduce((sum, log) => sum + (log.duration || 0), 0)
  return Math.round(totalSeconds / 3600)
})

const averageDowntimeMinutes = computed(() => {
  if (!downtimeLogs.data || downtimeLogs.data.length === 0) return 0
  const totalSeconds = downtimeLogs.data.reduce((sum, log) => sum + (log.duration || 0), 0)
  return Math.round(totalSeconds / 60 / downtimeLogs.data.length)
})

const formatDateTime = (dateTimeString) => {
  if (!dateTimeString) return "N/A"
  try {
    return new Date(dateTimeString).toLocaleString("en-GB")
  } catch {
    return "Invalid DateTime"
  }
}

const formatDuration = (seconds) => {
  if (!seconds || seconds === 0) return "N/A"

  const totalSeconds = Math.floor(seconds)
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)

  if (hours > 0) {
    return `${hours}h ${minutes}m`
  } else if (minutes > 0) {
    return `${minutes}m`
  } else {
    return "< 1m"
  }
}

const getStatusClass = (status) => {
  if (!status) return "bg-gray-100 text-gray-800"
  const statusLower = status.toLowerCase()

  if (statusLower.includes('active') || statusLower.includes('ongoing')) {
    return "bg-red-100 text-red-800"
  } else if (statusLower.includes('resolved') || statusLower.includes('closed')) {
    return "bg-green-100 text-green-800"
  }
  return "bg-yellow-100 text-yellow-800"
}
</script>