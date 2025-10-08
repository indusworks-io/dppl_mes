<template>
  <ListView
    doctype="Job Card"
    title="Job Cards"
    :columns="columns"
    :fields="fields"
    :filters="filters"
    orderBy="creation desc"
    :pageLength="100"
    :enableRouting="true"
    routePrefix="/production/job-cards"
  >
    <!-- Custom Progress Cell -->
    <template #cell-progress="{ row }">
      <div class="flex items-center">
        <div class="w-full bg-gray-200 rounded-full h-2 mr-3">
          <div
            class="bg-blue-600 h-2 rounded-full"
            :style="{ width: getProgressPercentage(row) + '%' }"
          ></div>
        </div>
        <span class="text-xs text-gray-500 min-w-0">{{ getActualProgressPercentage(row) }}%</span>
      </div>
    </template>

    <!-- Custom Status Cell -->
    <template #cell-status="{ value }">
      <span :class="getStatusClass(value)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
        {{ value || 'Draft' }}
      </span>
    </template>

    <!-- Custom Date Cell -->
    <template #cell-date="{ value }">
      {{ formatDate(value) }}
    </template>
  </ListView>
</template>

<script setup>
import { ref } from "vue"
import ListView from "../../components/ListView.vue"

// Fields to fetch from backend (excluding computed fields)
const fields = [
  "name",
  "machine",
  "date",
  "shift",
  "job_name",
  "completed_quantity",
  "target_quantity",
  "status",
]

// Column definitions for ListView (including computed fields for display)
const columns = [
  { fieldname: "name", label: "Job Card ID" },
  { fieldname: "machine", label: "Machine" },
  { fieldname: "date", label: "Date" },
  { fieldname: "shift", label: "Shift" },
  { fieldname: "job_name", label: "Job Name" },
  { fieldname: "completed_quantity", label: "Completed Quantity" },
  { fieldname: "target_quantity", label: "Target Quantity" },
  { fieldname: "progress", label: "Progress" }, // Virtual column computed on frontend
  { fieldname: "status", label: "Status" },
]

// Filters
const filters = ref([])

// Utility functions
const getProgressPercentage = (job) => {
  if (!job.target_quantity || job.target_quantity === 0) return 0
  const completed = job.completed_quantity || 0
  const target = job.target_quantity
  const percentage = Math.round((completed / target) * 100)
  return Math.min(percentage, 100) // Cap at 100% for the progress bar
}

const getActualProgressPercentage = (job) => {
  if (!job.target_quantity || job.target_quantity === 0) return 0
  const completed = job.completed_quantity || 0
  const target = job.target_quantity
  return Math.round((completed / target) * 100) // Show actual percentage in text
}

const getStatusClass = (status) => {
  if (!status) return "bg-gray-100 text-gray-800"
  const statusLower = status.toLowerCase()

  if (
    statusLower.includes("active") ||
    statusLower.includes("progress") ||
    statusLower.includes("running")
  ) {
    return "bg-green-100 text-green-800"
  } else if (statusLower.includes("complete") || statusLower.includes("done")) {
    return "bg-blue-100 text-blue-800"
  } else if (
    statusLower.includes("cancelled") ||
    statusLower.includes("failed")
  ) {
    return "bg-red-100 text-red-800"
  }
  return "bg-yellow-100 text-yellow-800"
}

const formatDate = (dateString) => {
  if (!dateString) return "N/A"
  try {
    return new Date(dateString).toLocaleDateString("en-GB")
  } catch {
    return "Invalid Date"
  }
}
</script>
