<template>
  <div class="p-6">
    <!-- Header Section -->
    <div v-if="!hideHeader" class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">{{ title }}</h1>
      </div>
      <button
        v-if="!hideCreateButton"
        @click="handleCreate"
        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        Create
      </button>
    </div>

    <!-- Subheader Section -->
    <div v-if="!hideSubheader" class="mb-4 flex items-center justify-between flex-wrap gap-4">
      <div class="flex items-center gap-2">
        <!-- Filter Dropdown -->
        <div class="relative" v-if="filterOptions && filterOptions.length > 0">
          <button
            @click="showFilterDropdown = !showFilterDropdown"
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path>
            </svg>
            Filters
          </button>
          <div
            v-if="showFilterDropdown"
            class="absolute left-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 z-10"
          >
            <div class="py-2">
              <button
                v-for="(filter, index) in filterOptions"
                :key="index"
                @click="applyFilter(filter)"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                {{ filter.label }}
              </button>
            </div>
          </div>
        </div>

        <!-- Refresh Button -->
        <button
          @click="handleRefresh"
          @blur="removeButtonFocus"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
          :disabled="listResource.loading"
        >
          <svg
            class="w-4 h-4 mr-2"
            :class="{ 'animate-spin': listResource.loading }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          Refresh
        </button>
      </div>

      <!-- Sort Dropdown -->
      <div class="relative">
        <button
          @click="showSortDropdown = !showSortDropdown"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"></path>
          </svg>
          Sort
        </button>
        <div
          v-if="showSortDropdown"
          class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 z-10"
        >
          <div class="py-2">
            <button
              @click="toggleSortOrder('asc')"
              class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Ascending
            </button>
            <button
              @click="toggleSortOrder('desc')"
              class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Descending
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="listResource.loading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p class="text-gray-600">Loading...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="listResource.error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-800">Error loading data: {{ listResource.error }}</p>
    </div>

    <!-- Body Section - Data Table -->
    <div v-else>
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <!-- Empty State -->
        <div v-if="!listResource.data || listResource.data.length === 0" class="p-8 text-center">
          <svg class="mx-auto w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No records found</h3>
          <p class="mt-1 text-sm text-gray-500">Records will appear here once created.</p>
        </div>

        <!-- Table -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  v-for="column in columns"
                  :key="column.fieldname"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  :style="column.width ? { width: column.width } : {}"
                >
                  {{ column.label }}
                </th>
                <th
                  v-if="rowActions && rowActions.length > 0"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="row in listResource.data"
                :key="row.name"
                @click="handleRowClick(row)"
                class="hover:bg-gray-50 cursor-pointer transition-colors"
              >
                <td
                  v-for="column in columns"
                  :key="column.fieldname"
                  class="px-6 py-4 text-sm text-gray-900"
                  :class="column.cellClass || 'whitespace-nowrap'"
                >
                  <!-- Custom Slot for Cell -->
                  <slot
                    :name="`cell-${column.fieldname}`"
                    :row="row"
                    :value="row[column.fieldname]"
                  >
                    <!-- Default Rendering with Formatter -->
                    <span v-if="column.formatter">
                      {{ column.formatter(row[column.fieldname], row) }}
                    </span>
                    <span v-else>
                      {{ row[column.fieldname] || '-' }}
                    </span>
                  </slot>
                </td>

                <!-- Row Actions -->
                <td
                  v-if="rowActions && rowActions.length > 0"
                  class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                  @click.stop
                >
                  <div class="flex items-center gap-2">
                    <button
                      v-for="(action, index) in rowActions"
                      :key="index"
                      @click="handleRowAction(action, row)"
                      class="text-blue-600 hover:text-blue-900 transition-colors inline-flex items-center"
                      :title="action.label"
                    >
                      <svg v-if="action.icon === 'edit'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                      <svg v-else-if="action.icon === 'check'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                      </svg>
                      <svg v-else-if="action.icon === 'delete'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                      <svg v-else-if="action.icon === 'view'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                      </svg>
                      <span v-else>{{ action.label }}</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination Controls -->
        <div class="px-6 py-4 border-t border-gray-200 flex flex-col items-center justify-center gap-3">
          <div class="text-sm text-gray-700">
            <span v-if="listResource.data && listResource.data.length > 0">
              Showing {{ listResource.data.length }} records
            </span>
          </div>

          <button
            v-if="listResource.hasNextPage && listResource.data && listResource.data.length > 0"
            @click="handleLoadMore"
            :disabled="listResource.loading"
            class="inline-flex items-center px-6 py-2 border border-gray-300 rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 bg-white hover:bg-gray-50 focus:outline-none transition-colors"
          >
            <span v-if="!listResource.loading">Load More</span>
            <span v-else class="flex items-center">
              <svg class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              Loading...
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createListResource } from "frappe-ui"
import { computed, ref, watch } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

// Props
const props = defineProps({
	doctype: {
		type: String,
		required: true,
	},
	title: {
		type: String,
		required: true,
	},
	columns: {
		type: Array,
		required: true,
		validator: (columns) => {
			return columns.every((col) => col.fieldname && col.label)
		},
	},
	filters: {
		type: Array,
		default: () => [],
	},
	orderBy: {
		type: String,
		default: "modified desc",
	},
	pageLength: {
		type: Number,
		default: 20,
	},
	rowActions: {
		type: Array,
		default: () => [],
	},
	filterOptions: {
		type: Array,
		default: () => [],
	},
	enableRouting: {
		type: Boolean,
		default: true,
	},
	routePrefix: {
		type: String,
		default: null,
	},
	fields: {
		type: Array,
		default: null,
	},
	hideHeader: {
		type: Boolean,
		default: false,
	},
	hideSubheader: {
		type: Boolean,
		default: false,
	},
	hideCreateButton: {
		type: Boolean,
		default: false,
	},
})

// Emits
const emit = defineEmits([
	"row-click",
	"row-action",
	"filters-change",
	"page-change",
	"create",
])

// State
const showFilterDropdown = ref(false)
const showSortDropdown = ref(false)
const currentFilters = ref([...props.filters])
const currentOrderBy = ref(props.orderBy)

// Compute fields from columns if not provided
const computedFields = computed(() => {
	if (props.fields) {
		return props.fields
	}
	// Extract unique fieldnames from columns
	const fieldnames = [...new Set(props.columns.map((col) => col.fieldname))]
	// Always include 'name' field if not present
	if (!fieldnames.includes("name")) {
		fieldnames.unshift("name")
	}
	return fieldnames
})

// Create List Resource
const listResource = createListResource({
	doctype: props.doctype,
	fields: computedFields.value,
	filters: currentFilters.value,
	orderBy: currentOrderBy.value,
	pageLength: props.pageLength,
	auto: true,
})

// Watch for filter changes from parent
watch(
	() => props.filters,
	(newFilters) => {
		currentFilters.value = [...newFilters]
		listResource.update({
			filters: currentFilters.value,
		})
		listResource.reload()
	},
	{ deep: true },
)

// Methods
const handleCreate = () => {
	emit("create")
	// If routing is enabled, navigate to form page
	if (props.enableRouting) {
		const route = props.routePrefix
			? `${props.routePrefix}/new`
			: `/app/${props.doctype.toLowerCase().replace(" ", "-")}/new`
		router.push(route)
	}
}

const handleRefresh = (event) => {
	listResource.reload()
	// Remove focus from button after click
	if (event?.target) {
		event.target.blur()
	}
}

const removeButtonFocus = () => {
	// Helper method for blur event
}

const handleRowClick = (row) => {
	emit("row-click", row)

	// If routing is enabled, navigate to detail page
	if (props.enableRouting && row.name) {
		const route = props.routePrefix
			? `${props.routePrefix}/${row.name}`
			: `/${props.doctype.toLowerCase().replace(" ", "-")}/${row.name}`
		router.push(route)
	}
}

const handleRowAction = (action, row) => {
	emit("row-action", { action: action.label, row })
	if (action.action && typeof action.action === "function") {
		action.action(row)
	}
}

const applyFilter = (filter) => {
	if (filter.filters) {
		currentFilters.value = filter.filters
		listResource.update({
			filters: currentFilters.value,
		})
		listResource.reload()
		emit("filters-change", currentFilters.value)
	}
	showFilterDropdown.value = false
}

const toggleSortOrder = (order) => {
	// Extract the field name from current orderBy
	const currentField = currentOrderBy.value.split(" ")[0]
	currentOrderBy.value = `${currentField} ${order}`

	listResource.update({
		orderBy: currentOrderBy.value,
	})
	listResource.reload()
	showSortDropdown.value = false
}

const handleLoadMore = () => {
	if (listResource.next) {
		listResource.next()
		emit("page-change", "load-more")
	}
}

// Close dropdowns when clicking outside
const closeDropdowns = () => {
	showFilterDropdown.value = false
	showSortDropdown.value = false
}

// Add event listener for clicks outside
if (typeof window !== "undefined") {
	window.addEventListener("click", (e) => {
		if (!e.target.closest(".relative")) {
			closeDropdowns()
		}
	})
}
</script>
