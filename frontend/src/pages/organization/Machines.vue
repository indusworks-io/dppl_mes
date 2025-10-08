<template>
  <ListView
    doctype="Machine"
    title="Machines"
    :columns="columns"
    :filters="filters"
    orderBy="sequence_number asc, creation desc"
    :pageLength="100"
    :enableRouting="true"
    routePrefix="/organization/machine"
  >
    <!-- Custom Machine Name Cell -->
    <template #cell-machine_name="{ value, row }">
      {{ value || row.name }}
    </template>

    <!-- Custom Status Cell -->
    <template #cell-is_active="{ value }">
      <span :class="value ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
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
  { fieldname: "machine_name", label: "Machine Name" },
  { fieldname: "area", label: "Area" },
  { fieldname: "factory", label: "Factory" },
  { fieldname: "is_active", label: "Is Active?" },
]

// Filters
const filters = ref([])
</script>
