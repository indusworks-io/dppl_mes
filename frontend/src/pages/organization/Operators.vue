<template>
  <ListView
    doctype="Operator"
    title="Operators"
    :columns="columns"
    :filters="filters"
    orderBy="creation desc"
    :pageLength="100"
    :enableRouting="true"
    routePrefix="/organization/operators"
  >
    <!-- Custom Operator Name Cell -->
    <template #cell-operator_name="{ value, row }">
      {{ value || row.name }}
    </template>
  </ListView>
</template>

<script setup>
import { ref } from "vue"
import ListView from "../../components/ListView.vue"

// Column definitions for ListView
const columns = [
  { fieldname: "operator_name", label: "Operator Name" },
  { fieldname: "employee_code", label: "Employee Code" },
]

// Filters
const filters = ref([])
</script>
