<template>
  <ListView
    doctype="Downtime Reason"
    title="Downtime Reasons"
    :columns="columns"
    :filters="filters"
    orderBy="creation desc"
    :pageLength="50"
    :enableRouting="true"
    routePrefix="/production/downtime-reasons"
  >
    <!-- Custom Status Cell -->
    <template #cell-is_active="{ value }">
      <span :class="getStatusClass(value)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
        {{ value ? 'Active' : 'Inactive' }}
      </span>
    </template>
  </ListView>
</template>

<script setup>
import { ref } from "vue"
import ListView from "../../components/ListView.vue"

// Column definitions for ListView
const columns = [
  { fieldname: "downtime_reason", label: "Downtime Reason" },
  { fieldname: "category", label: "Category" },
  { fieldname: "is_active", label: "Is Active?" },
]

// Filters
const filters = ref([])

// Utility functions
const getStatusClass = (isActive) => {
  return isActive ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"
}
</script>
