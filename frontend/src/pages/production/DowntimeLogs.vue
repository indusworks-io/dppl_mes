<template>
  <ListView
    doctype="Downtime Log"
    title="Downtime Logs"
    :columns="columns"
    :filters="filters"
    orderBy="creation desc"
    :pageLength="50"
    :enableRouting="true"
    routePrefix="/production/downtime-logs"
    :hideCreateButton="true"
  >
    <!-- Custom DateTime Cells -->
    <template #cell-start_date_time="{ value }">
      {{ formatDateTime(value) }}
    </template>

    <template #cell-end_date_time="{ value }">
      {{ formatDateTime(value) }}
    </template>

    <!-- Custom Duration Cell -->
    <template #cell-duration="{ value }">
      {{ formatDuration(value) }}
    </template>

    <!-- Custom Status Cell -->
    <template #cell-status="{ value }">
      <span :class="getStatusClass(value)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
        {{ value || 'Unknown' }}
      </span>
    </template>
  </ListView>
</template>

<script setup>
import { ref } from "vue"
import ListView from "../../components/ListView.vue"

// Column definitions for ListView
const columns = [
  { fieldname: "name", label: "Downtime Log ID" },
  { fieldname: "machine", label: "Machine" },
  { fieldname: "start_date_time", label: "Start Date Time" },
  { fieldname: "end_date_time", label: "End Date Time" },
  { fieldname: "duration", label: "Duration" },
  { fieldname: "reason", label: "Reason" },
  { fieldname: "status", label: "Status" },
]

// Filters
const filters = ref([])

// Utility functions
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

  if (statusLower.includes("active") || statusLower.includes("ongoing")) {
    return "bg-red-100 text-red-800"
  } else if (
    statusLower.includes("resolved") ||
    statusLower.includes("closed")
  ) {
    return "bg-green-100 text-green-800"
  }
  return "bg-yellow-100 text-yellow-800"
}
</script>
