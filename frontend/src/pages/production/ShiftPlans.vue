<template>
  <ListView
    doctype="Shift Plan"
    title="Shift Plans"
    :columns="columns"
    :filters="filters"
    orderBy="creation desc"
    :pageLength="50"
    :enableRouting="true"
    routePrefix="/production/shift-plans"
  >
    <!-- Custom Status Cell -->
    <template #cell-status="{ value }">
      <span :class="getStatusClass(value)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
        {{ value || 'Draft' }}
      </span>
    </template>
  </ListView>
</template>

<script setup>
import { ref } from "vue"
import { createListResource } from "frappe-ui"
import ListView from "../../components/ListView.vue"

// Fetch shift plans for stats calculation
const shiftPlans = createListResource({
	doctype: "Shift Plan",
	fields: ["name", "status"],
	orderBy: "creation desc",
	pageLength: 1000,
	auto: true,
})

// Column definitions for ListView
const columns = [
	{ fieldname: "name", label: "Plan Name" },
	{
		fieldname: "date",
		label: "Date",
		formatter: (value) => {
			if (!value) return "N/A"
			try {
				return new Date(value).toLocaleDateString("en-GB")
			} catch {
				return "Invalid Date"
			}
		},
	},
	{ fieldname: "shift", label: "Shift" },
	{ fieldname: "factory", label: "Factory" },
	{ fieldname: "status", label: "Status" },
]

// Filters
const filters = ref([])

// Utility functions
const getStatusClass = (status) => {
	if (!status) return "bg-gray-100 text-gray-800"
	const statusLower = status.toLowerCase()

	if (statusLower.includes("active") || statusLower.includes("progress")) {
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
</script>