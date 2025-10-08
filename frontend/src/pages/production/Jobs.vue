<template>
  <ListView
    doctype="Job"
    title="Jobs"
    :columns="columns"
    :filters="filters"
    orderBy="creation desc"
    :pageLength="50"
    :enableRouting="true"
    routePrefix="/production/jobs"
  >
  </ListView>
</template>

<script setup>
import { ref } from "vue"
import ListView from "../../components/ListView.vue"

// Column definitions for ListView
const columns = [
  { fieldname: "job_name", label: "Job Name" },
  { fieldname: "job_number", label: "Job Number" },
  { fieldname: "complexity_level", label: "Complexity Level" },
  { fieldname: "ideal_run_rate", label: "Ideal Run Rate" },
]

// Filters
const filters = ref([])
</script>
