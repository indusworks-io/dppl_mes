<template>
  <div>
    <ListView
      doctype="Downtime Log"
      title="Downtime Logs"
      :columns="columns"
      :fields="['name', 'machine', 'start_date_time', 'end_date_time', 'duration', 'reason', 'category', 'status']"
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

      <!-- Custom Actions Cell -->
      <template #cell-actions="{ row }">
        <button
          v-if="!row.reason"
          @click.stop="openUpdateReasonDialog(row.name)"
          class="inline-flex items-center px-3 py-1.5 bg-blue-600 text-white text-xs font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          Update Reason
        </button>
        <span v-else class="text-xs text-gray-500">-</span>
      </template>
    </ListView>

    <!-- Update Reason Dialog -->
    <UpdateReasonDialog
      :visible="isDialogVisible"
      :downtimeId="selectedDowntimeId"
      @update="handleReasonUpdated"
      @cancel="closeDialog"
    />
  </div>
</template>

<script setup>
import { ref } from "vue"
import ListView from "../../components/ListView.vue"
import UpdateReasonDialog from "../../components/UpdateReasonDialog.vue"

// Column definitions for ListView
const columns = [
  { fieldname: "name", label: "Downtime Log ID" },
  { fieldname: "machine", label: "Machine" },
  { fieldname: "start_date_time", label: "Start Date Time" },
  { fieldname: "end_date_time", label: "End Date Time" },
  { fieldname: "duration", label: "Duration" },
  { fieldname: "reason", label: "Reason" },
  { fieldname: "category", label: "Category" },
  { fieldname: "status", label: "Status" },
  { fieldname: "actions", label: "Actions" },
]

// Filters
const filters = ref([])

// Dialog state
const isDialogVisible = ref(false)
const selectedDowntimeId = ref(null)

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

// Dialog handlers
const openUpdateReasonDialog = (downtimeId) => {
  selectedDowntimeId.value = downtimeId
  isDialogVisible.value = true
}

const closeDialog = () => {
  isDialogVisible.value = false
  selectedDowntimeId.value = null
}

const handleReasonUpdated = () => {
  // Close the dialog
  closeDialog()
  // Reload the page to refresh the data
  window.location.reload()
}
</script>
