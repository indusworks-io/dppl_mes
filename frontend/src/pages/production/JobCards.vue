<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Job Cards</h1>
      <p class="text-gray-600">Monitor and manage production job cards</p>
    </div>

    <!-- Loading State -->
    <div v-if="jobCards.loading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p class="text-gray-600">Loading job cards...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="jobCards.error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-800">Error loading job cards: {{ jobCards.error }}</p>
    </div>

    <!-- Content -->
    <div v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Jobs</p>
              <p class="text-2xl font-semibold text-gray-900">{{ jobCards.data?.length || 0 }}</p>
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
              <p class="text-2xl font-semibold text-gray-900">{{ activeJobsCount }}</p>
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
              <p class="text-sm font-medium text-gray-600">Pending</p>
              <p class="text-2xl font-semibold text-gray-900">{{ pendingJobsCount }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Completed</p>
              <p class="text-2xl font-semibold text-gray-900">{{ completedJobsCount }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Job Cards List -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Recent Job Cards</h2>
        </div>

        <div v-if="!jobCards.data || jobCards.data.length === 0" class="p-8 text-center">
          <svg class="mx-auto w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No job cards found</h3>
          <p class="mt-1 text-sm text-gray-500">Job cards will appear here once created.</p>
        </div>

        <div v-else class="overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job Card</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Machine</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Shift</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Progress</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="job in jobCards.data" :key="job.name" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ job.name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ job.machine || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(job.date) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ job.shift || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <div class="flex items-center">
                    <div class="w-full bg-gray-200 rounded-full h-2 mr-3">
                      <div
                        class="bg-blue-600 h-2 rounded-full"
                        :style="{ width: getProgressPercentage(job) + '%' }"
                      ></div>
                    </div>
                    <span class="text-xs text-gray-500 min-w-0">{{ getProgressPercentage(job) }}%</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusClass(job.status)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                    {{ job.status || 'Draft' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <router-link
                    :to="`/job-card/${job.name}`"
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

// Fetch job cards
const jobCards = createListResource({
  doctype: "Job Card",
  fields: [
    "name",
    "machine",
    "date",
    "shift",
    "status",
    "target_quantity",
    "completed_quantity",
    "creation"
  ],
  orderBy: "creation desc",
  pageLength: 100,
  auto: true,
})

// Computed properties for statistics
const activeJobsCount = computed(() => {
  if (!jobCards.data) return 0
  return jobCards.data.filter(job =>
    job.status === 'Active' ||
    job.status === 'In Progress' ||
    job.status === 'Running'
  ).length
})

const pendingJobsCount = computed(() => {
  if (!jobCards.data) return 0
  return jobCards.data.filter(job =>
    job.status === 'Draft' ||
    job.status === 'Pending' ||
    job.status === 'Ready'
  ).length
})

const completedJobsCount = computed(() => {
  if (!jobCards.data) return 0
  return jobCards.data.filter(job =>
    job.status === 'Completed' ||
    job.status === 'Done'
  ).length
})

// Utility functions
const formatDate = (dateString) => {
  if (!dateString) return "N/A"
  try {
    return new Date(dateString).toLocaleDateString("en-GB")
  } catch {
    return "Invalid Date"
  }
}

const getProgressPercentage = (job) => {
  if (!job.target_quantity || job.target_quantity === 0) return 0
  const completed = job.completed_quantity || 0
  const target = job.target_quantity
  return Math.round((completed / target) * 100)
}

const getStatusClass = (status) => {
  if (!status) return "bg-gray-100 text-gray-800"
  const statusLower = status.toLowerCase()

  if (statusLower.includes('active') || statusLower.includes('progress') || statusLower.includes('running')) {
    return "bg-green-100 text-green-800"
  } else if (statusLower.includes('complete') || statusLower.includes('done')) {
    return "bg-blue-100 text-blue-800"
  } else if (statusLower.includes('cancelled') || statusLower.includes('failed')) {
    return "bg-red-100 text-red-800"
  }
  return "bg-yellow-100 text-yellow-800"
}
</script>