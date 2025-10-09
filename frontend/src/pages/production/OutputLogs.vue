<template>
  <ListView
    doctype="Output Log"
    title="Output Logs"
    :columns="columns"
    :filters="filters"
    orderBy="creation desc"
    :pageLength="50"
    :enableRouting="true"
    routePrefix="/production/output-logs"
    :hideCreateButton="true"
  >
    <!-- Custom DateTime Cell -->
    <template #cell-timestamp="{ value }">
      {{ formatDateTime(value) }}
    </template>
  </ListView>
</template>

<script setup>
import { ref } from "vue"
import ListView from "../../components/ListView.vue"

// Column definitions for ListView
const columns = [
  { fieldname: "name", label: "Output Log ID" },
  { fieldname: "timestamp", label: "Timestamp" },
  { fieldname: "job_card", label: "Job Card" },
  { fieldname: "machine", label: "Machine" },
  { fieldname: "output", label: "Output" },
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
</script>
