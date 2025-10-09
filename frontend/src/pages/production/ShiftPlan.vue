<template>
  <div class="shift-plan-page p-6">
    <!-- Loading State -->
    <div v-if="doc.loading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p class="text-gray-600">Loading...</p>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else-if="doc.doc">
      <!-- Header Section -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-4">
        <div class="flex items-center justify-between flex-wrap gap-4">
          <div class="flex items-center gap-3">
            <button
              @click="router.push('/production/shift-plans')"
              class="inline-flex items-center text-gray-600 hover:text-gray-900 transition-colors"
              title="Back to Shift Plans"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ docname ? doc.doc.name : 'New Shift Plan' }}
            </h1>
          </div>

          <div class="flex items-center gap-2">
            <!-- View Mode Actions -->
            <template v-if="docname">
              <!-- <button
                @click="handleRefresh"
                :disabled="doc.loading"
                class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none disabled:opacity-50"
              >
                <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': refreshing }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                Refresh
              </button> -->

              <!-- Save Button (Draft only) -->
              <button
                v-if="doc.doc.status === 'Draft'"
                @click="handleSave"
                :disabled="doc.setValue.loading"
                class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 focus:outline-none disabled:opacity-50"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                {{ doc.setValue.loading ? 'Saving...' : 'Save' }}
              </button>

              <!-- Confirm Shift Plan Button (Draft only) -->
              <button
                v-if="doc.doc.status === 'Draft'"
                @click="handleConfirm"
                :disabled="confirming"
                class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 focus:outline-none disabled:opacity-50"
              >
                {{ confirming ? 'Confirming...' : 'Confirm Plan' }}
              </button>

              <!-- Cancel Shift Plan Button (Draft only) -->
              <button
                v-if="doc.doc.status === 'Draft'"
                @click="handleCancelPlan"
                :disabled="cancelling"
                class="inline-flex items-center px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 focus:outline-none disabled:opacity-50"
              >
                Cancel Plan
              </button>
            </template>

            <!-- New/Edit Mode Actions -->
            <template v-else>
              <button
                @click="handleCancel"
                class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
              >
                Cancel
              </button>
              <button
                @click="handleSave"
                :disabled="doc.setValue.loading"
                class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 focus:outline-none disabled:opacity-50"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                {{ doc.setValue.loading ? 'Saving...' : 'Save' }}
              </button>
            </template>
          </div>
        </div>
      </div>

      <!-- Error Message Display -->
      <div v-if="confirmError" class="bg-white rounded-lg shadow-sm border border-red-200 p-4 mb-6">
        <div class="flex items-start">
          <svg class="w-5 h-5 text-red-600 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <div class="flex-1">
            <h3 class="text-sm font-medium text-red-800 mb-1">Error</h3>
            <ErrorMessage :message="confirmError" />
          </div>
          <button @click="confirmError = null" class="text-red-600 hover:text-red-800">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Tab Navigation -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
        <div class="border-b border-gray-200">
          <nav class="flex -mb-px">
            <button
              @click="activeTab = 'overview'"
              :class="[
                'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
                activeTab === 'overview'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Overview
            </button>
            <button
              v-if="docname"
              @click="activeTab = 'jobcards'"
              :class="[
                'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
                activeTab === 'jobcards'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Job Cards
            </button>
          </nav>
        </div>

        <!-- Tab Content -->
        <div class="p-6">
          <!-- Overview Tab -->
          <div v-if="activeTab === 'overview'">
            <!-- Form Fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <!-- Date -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Date <span class="text-red-500">*</span>
                </label>
                <DatePicker
                  v-model="doc.doc.date"
                  :disabled="docname && doc.doc.status !== 'Draft'"
                  placeholder="Select Date"
                  variant="outline"
                />
              </div>

              <!-- Factory -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Factory <span class="text-red-500">*</span>
                </label>
                <Autocomplete
                  v-model="doc.doc.factory"
                  :options="factoryOptions"
                  placeholder="Select Factory"
                  :loading="factoriesResource.loading"
                  :disabled="docname && doc.doc.status !== 'Draft'"
                  :compareFn="(a, b) => a?.value === b?.value"
                  @update:modelValue="handleFactoryChange"
                />
              </div>

              <!-- Shift -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Shift <span class="text-red-500">*</span>
                </label>
                <Autocomplete
                  v-model="doc.doc.shift"
                  :options="shiftOptions"
                  placeholder="Select Shift"
                  :loading="shiftsResource.loading"
                  :disabled="docname && doc.doc.status !== 'Draft'"
                  :compareFn="(a, b) => a?.value === b?.value"
                />
              </div>

              <!-- Status -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Status
                </label>
                <Select
                  :model-value="doc.doc.status || 'Draft'"
                  :options="['Draft', 'Confirmed', 'Cancelled']"
                  disabled
                  variant="outline"
                  size="md"
                />
              </div>
            </div>

            <!-- Job Plan Details Table -->
            <div class="mt-6">
              <div class="mb-4">
                <h3 class="text-lg font-semibold text-gray-900">Job Plan Details</h3>
              </div>

              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-lg">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">No Job</th>
                      <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Machine</th>
                      <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Operator</th>
                      <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job 1</th>
                      <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job 1 Qty</th>
                      <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job 1 Duration</th>
                      <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job 2</th>
                      <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job 2 Qty</th>
                      <th v-if="!docname || doc.doc.status === 'Draft'" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-16">Action</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="(row, index) in doc.doc.job_plan_details" :key="row.id || `row-${index}`">
                      <!-- No Job Checkbox -->
                      <td class="px-3 py-2 text-center">
                        <Checkbox
                          v-model="row.no_job"
                          :disabled="docname && doc.doc.status !== 'Draft'"
                          size="md"
                        />
                      </td>

                      <!-- Machine -->
                      <td class="px-3 py-2">
                        <Autocomplete
                          v-if="!docname || doc.doc.status === 'Draft'"
                          v-model="row.machine_name"
                          :options="machineOptions"
                          placeholder="Select Machine"
                          :loading="machinesResource.loading"
                          :compareFn="(a, b) => a?.value === b?.value"
                          class="min-w-[150px]"
                        />
                        <span v-else class="text-sm text-gray-900">{{ getFieldValue(row.machine_name) || '-' }}</span>
                      </td>

                      <!-- Operator -->
                      <td class="px-3 py-2">
                        <Autocomplete
                          v-if="!docname || doc.doc.status === 'Draft'"
                          v-model="row.operator_name"
                          :options="operatorOptions"
                          placeholder="Select Operator"
                          :loading="operatorsResource.loading"
                          :disabled="!!row.no_job"
                          :compareFn="(a, b) => a?.value === b?.value"
                          class="min-w-[150px]"
                        />
                        <span v-else class="text-sm text-gray-900">{{ getFieldValue(row.operator_name) || '-' }}</span>
                      </td>

                      <!-- Job 1 Name -->
                      <td class="px-3 py-2">
                        <Autocomplete
                          v-if="!docname || doc.doc.status === 'Draft'"
                          v-model="row.job_one_name"
                          :options="jobOptions"
                          placeholder="Select Job"
                          :loading="jobsResource.loading"
                          :disabled="!!row.no_job"
                          :compareFn="(a, b) => a?.value === b?.value"
                          class="min-w-[150px]"
                        />
                        <span v-else class="text-sm text-gray-900">{{ getFieldValue(row.job_one_name) || '-' }}</span>
                      </td>

                      <!-- Job 1 Quantity -->
                      <td class="px-3 py-2 w-32">
                        <input
                          v-if="!docname || doc.doc.status === 'Draft'"
                          v-model.number="row.job_one_quantity"
                          type="number"
                          min="0"
                          :disabled="!!row.no_job"
                          class="min-w-[150px] w-full px-2 py-1 border border-gray-300 rounded text-sm focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50"
                        />
                        <span v-else class="text-sm text-gray-900">{{ row.job_one_quantity || '-' }}</span>
                      </td>

                      <!-- Job 1 Duration (input in hours, stored as seconds) -->
                      <td class="px-3 py-2 w-32">
                        <input
                          v-if="!docname || doc.doc.status === 'Draft'"
                          :value="getDurationHours(row.job_one_duration)"
                          @input="setDurationHours(row, $event.target.value)"
                          type="number"
                          min="0"
                          step="0.5"
                          placeholder="Hours"
                          :disabled="!!row.no_job"
                          class="min-w-[150px] w-full px-2 py-1 border border-gray-300 rounded text-sm focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50"
                        />
                        <span v-else class="text-sm text-gray-900">{{ formatDuration(row.job_one_duration) }}</span>
                      </td>

                      <!-- Job 2 Name -->
                      <td class="px-3 py-2">
                        <Autocomplete
                          v-if="!docname || doc.doc.status === 'Draft'"
                          v-model="row.job_two_name"
                          :options="jobOptions"
                          placeholder="Select Job"
                          :loading="jobsResource.loading"
                          :disabled="!!row.no_job"
                          :compareFn="(a, b) => a?.value === b?.value"
                          class="min-w-[150px]"
                        />
                        <span v-else class="text-sm text-gray-900">{{ getFieldValue(row.job_two_name) || '-' }}</span>
                      </td>

                      <!-- Job 2 Quantity -->
                      <td class="px-3 py-2 w-32">
                        <input
                          v-if="!docname || doc.doc.status === 'Draft'"
                          v-model.number="row.job_two_quantity"
                          type="number"
                          min="0"
                          :disabled="!!row.no_job"
                          class="min-w-[150px] w-full px-2 py-1 border border-gray-300 rounded text-sm focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50"
                        />
                        <span v-else class="text-sm text-gray-900">{{ row.job_two_quantity || '-' }}</span>
                      </td>

                      <!-- Remove Row Button -->
                      <td v-if="!docname || doc.doc.status === 'Draft'" class="px-3 py-2 text-center">
                        <button
                          @click="removeRow(index)"
                          class="text-red-600 hover:text-red-800"
                        >
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
                        </button>
                      </td>
                    </tr>

                    <!-- Empty State -->
                    <tr v-if="!doc.doc.job_plan_details || doc.doc.job_plan_details.length === 0">
                      <td :colspan="docname && doc.doc.status !== 'Draft' ? 8 : 9" class="px-6 py-8 text-center text-gray-500">
                        No machines added. {{ !docname || doc.doc.status === 'Draft' ? 'Select a factory or click "Add Row" to add machines.' : '' }}
                      </td>
                    </tr>
                  </tbody>
                </table>

                <!-- Add Row Button at Bottom -->
                <div v-if="!docname || doc.doc.status === 'Draft'" class="mt-4 flex justify-center">
                  <button
                    @click="addRow"
                    class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
                  >
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                    </svg>
                    Add Row
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Job Cards Tab -->
          <div v-if="activeTab === 'jobcards' && docname && doc.doc.name">
            <ListView
              doctype="Job Card"
              title="Job Cards"
              :columns="jobCardColumns"
              :fields="['name', 'machine', 'date', 'shift', 'job_name', 'completed_quantity', 'target_quantity', 'status']"
              :filters="jobCardFilters"
              :hideHeader="true"
              :hideSubheader="true"
              orderBy="creation desc"
              :pageLength="50"
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
                  <span class="text-xs text-gray-500 min-w-0">{{ getProgressPercentage(row) }}%</span>
                </div>
              </template>

              <!-- Custom Status Cell -->
              <template #cell-status="{ value }">
                <span :class="getJobCardStatusClass(value)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                  {{ value || 'Draft' }}
                </span>
              </template>

              <!-- Custom Date Cell -->
              <template #cell-date="{ value }">
                {{ formatDate(value) }}
              </template>
            </ListView>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createDocumentResource, createResource, createListResource, Autocomplete, Checkbox, DatePicker, ErrorMessage, Select, toast } from 'frappe-ui'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ListView from '../../components/ListView.vue'

const route = useRoute()
const router = useRouter()

// State
const activeTab = ref('overview')
const confirming = ref(false)
const cancelling = ref(false)
const refreshing = ref(false)
const confirmError = ref(null)

// Compute docname from route
const docname = computed(() => {
  const name = route.params.name
  return (name === 'new' || !name) ? undefined : name
})

// Document resource - initialize reactively based on docname
const docResource = ref(null)

// Computed property to access doc without .value in template
const doc = computed(() => docResource.value)

// Function to initialize/reinitialize document resource
const initializeDoc = () => {
  const name = docname.value
  if (name && name !== 'new') {
    // Existing document - use createDocumentResource
    docResource.value = createDocumentResource({
      doctype: 'Shift Plan',
      name: name,
      auto: true,
      setValue: {
        onSuccess: () => {
          toast.success('Shift Plan updated successfully')
        },
        onError: (err) => {
          toast.error(err.messages?.join(', ') || 'Failed to update')
        }
      },
      onSuccess: (data) => {
        // Convert no_job to boolean for display
        if (data.job_plan_details && data.job_plan_details.length > 0) {
          data.job_plan_details = data.job_plan_details.map((row, index) => ({
            ...row,
            id: row.name || `existing-${index}-${Date.now()}`,
            no_job: Boolean(row.no_job)
          }))
        }
      }
    })
  } else {
    // New document - create a reactive document structure
    docResource.value = reactive({
      doc: {
        doctype: 'Shift Plan',
        date: new Date().toISOString().split('T')[0],
        factory: null,
        shift: null,
        status: 'Draft',
        job_plan_details: []
      },
      loading: false,
      setValue: {
        loading: false,
        submit: () => Promise.resolve()
      },
      reload: () => Promise.resolve(),
      createJobCards: {
        submit: () => Promise.resolve()
      }
    })
  }
}

// Initialize document on mount
initializeDoc()

// Watch for route param changes and reinitialize document resource
watch(docname, () => {
  initializeDoc()
})

// Preload list resources for better UX
const factoriesResource = createListResource({
  doctype: 'Factory',
  fields: ['name', 'factory_name'],
  filters: { is_active: 1 },
  auto: true,
})

const shiftsResource = createListResource({
  doctype: 'Shift Type',
  fields: ['name', 'shift_type'],
  auto: true,
})

const operatorsResource = createListResource({
  doctype: 'Operator',
  fields: ['name', 'operator_name'],
  filters: { is_active: 1 },
  auto: true,
})

const jobsResource = createListResource({
  doctype: 'Job',
  fields: ['name', 'job_name'],
  auto: true,
})

// Load ALL machines upfront
const machinesResource = createListResource({
  doctype: 'Machine',
  fields: ['name', 'machine_name', 'factory', 'sequence_number'],
  filters: { is_active: 1 },
  order_by: 'sequence_number asc',
  auto: true,
})

// Convert list resources to Autocomplete options format
const factoryOptions = computed(() => {
  if (!factoriesResource.data) return []
  return factoriesResource.data.map(factory => ({
    label: factory.factory_name || factory.name,
    value: factory.name
  }))
})

const shiftOptions = computed(() => {
  if (!shiftsResource.data) return []
  return shiftsResource.data.map(shift => ({
    label: shift.name,
    value: shift.name
  }))
})

const operatorOptions = computed(() => {
  if (!operatorsResource.data) return []
  return operatorsResource.data.map(operator => ({
    label: operator.operator_name || operator.name,
    value: operator.name
  }))
})

const jobOptions = computed(() => {
  if (!jobsResource.data) return []
  return jobsResource.data.map(job => ({
    label: job.job_name || job.name,
    value: job.name
  }))
})

const machineOptions = computed(() => {
  if (!machinesResource.data) return []
  // Filter by selected factory if available
  const factory = doc.value?.doc?.factory
  const machines = factory
    ? machinesResource.data.filter(m => m.factory === getFieldValue(factory))
    : machinesResource.data

  // Sort by sequence_number in ascending order
  const sortedMachines = machines.sort((a, b) => {
    const seqA = a.sequence_number ?? Infinity
    const seqB = b.sequence_number ?? Infinity
    return seqA - seqB
  })

  return sortedMachines.map(machine => ({
    label: machine.machine_name || machine.name,
    value: machine.machine_name
  }))
})

// Helper function to extract value from Autocomplete option objects
const getFieldValue = (value) => {
  if (!value) return null
  return typeof value === 'object' && value.value !== undefined ? value.value : value
}

// Initialize new form with default values
const initializeNewForm = async () => {
  // Wait for all resources to load
  await Promise.all([
    factoriesResource.list?.loading ? factoriesResource.list.promise : Promise.resolve(),
    machinesResource.list?.loading ? machinesResource.list.promise : Promise.resolve(),
  ])

  // Fetch default factory from Organization Settings
  try {
    const settingsResource = createResource({
      url: 'frappe.client.get_value',
      params: {
        doctype: 'Organization Settings',
        filters: {},
        fieldname: 'default_factory'
      }
    })

    await settingsResource.fetch()

    if (settingsResource.data && settingsResource.data.default_factory) {
      doc.value.doc.factory = settingsResource.data.default_factory
      // Populate machines table for default factory
      populateMachinesTable(settingsResource.data.default_factory)
    }
  } catch (err) {
    console.error('Failed to load organization settings:', err)
  }
}

// Populate table with machines for selected factory (using already-loaded data)
const populateMachinesTable = (factory) => {
  if (!factory || !machinesResource.data) {
    doc.value.doc.job_plan_details = []
    return
  }

  // Filter machines by selected factory and sort by sequence_number
  const factoryMachines = machinesResource.data
    .filter(machine => machine.factory === factory)
    .sort((a, b) => {
      const seqA = a.sequence_number ?? Infinity
      const seqB = b.sequence_number ?? Infinity
      return seqA - seqB
    })

  // Clear existing rows
  doc.value.doc.job_plan_details = []

  // Add machines to table
  factoryMachines.forEach((machine, index) => {
    doc.value.doc.job_plan_details.push({
      id: `${machine.name}-${Date.now()}-${index}`, // Unique ID for Vue key
      machine_name: machine.machine_name,
      no_job: false,
      operator_name: null,
      job_one_name: null,
      job_one_number: null,
      job_one_quantity: null,
      job_one_duration: null,
      job_two_name: null,
      job_two_number: null,
      job_two_quantity: null
    })
  })
}

// Handle factory change - simplified to just filter local data
const handleFactoryChange = (newValue) => {
  const factoryValue = getFieldValue(newValue)
  if (factoryValue) {
    populateMachinesTable(factoryValue)
  }
}

// Table operations
const addRow = () => {
  doc.value.doc.job_plan_details.push({
    id: `manual-${Date.now()}-${Math.random()}`, // Unique ID for manually added rows
    machine_name: null,
    no_job: false,
    operator_name: null,
    job_one_name: null,
    job_one_number: null,
    job_one_quantity: null,
    job_one_duration: null,
    job_two_name: null,
    job_two_number: null,
    job_two_quantity: null
  })
}

const removeRow = (index) => {
  doc.value.doc.job_plan_details.splice(index, 1)
}

// Validation
const validateForm = () => {
  if (!doc.value.doc.date) {
    toast.error('Date is required')
    return false
  }
  if (!doc.value.doc.factory) {
    toast.error('Factory is required')
    return false
  }
  if (!doc.value.doc.shift) {
    toast.error('Shift is required')
    return false
  }
  return true
}

// Handle Save
const handleSave = async () => {
  if (!validateForm()) {
    return
  }

  try {
    // Prepare data for save - extract values from Autocomplete objects
    const dataToSave = {
      date: doc.value.doc.date,
      factory: getFieldValue(doc.value.doc.factory),
      shift: getFieldValue(doc.value.doc.shift),
      status: doc.value.doc.status,
      job_plan_details: (doc.value.doc.job_plan_details || []).map(row => ({
        ...row,
        no_job: row.no_job ? 1 : 0,
        machine_name: getFieldValue(row.machine_name),
        operator_name: getFieldValue(row.operator_name),
        job_one_name: getFieldValue(row.job_one_name),
        job_two_name: getFieldValue(row.job_two_name)
      }))
    }

    if (docname.value) {
      // Update existing document
      await doc.value.setValue.submit(dataToSave)
      await doc.value.reload()
    } else {
      // Create new document
      const insertResource = createResource({
        url: 'frappe.client.insert',
        makeParams: () => ({
          doc: {
            doctype: 'Shift Plan',
            ...dataToSave
          }
        })
      })

      const result = await insertResource.fetch()

      if (result) {
        toast.success('Shift Plan created successfully')
        // Navigate to the new document - use push to trigger route change and component reload
        router.push(`/production/shift-plans/${result.name}`)
      }
    }
  } catch (err) {
    toast.error(err.messages?.join(', ') || err.message || 'Failed to save')
    console.error(err)
  }
}

// Handle Confirm Shift Plan
const handleConfirm = async () => {
  if (!confirm('Job Cards will be created. Continue?')) {
    return
  }

  // Clear any previous errors
  confirmError.value = null
  confirming.value = true

  try {
    // Call the whitelisted method with full path
    const confirmResource = createResource({
      url: 'dppl_mes.manufacturing.doctype.shift_plan.shift_plan.create_job_cards',
      makeParams: () => ({
        docname: doc.value.doc.name
      })
    })

    const result = await confirmResource.fetch()

    if (result) {
      toast.success(`Job Cards created successfully. ${result.created} cards created.`)
      await doc.value.reload()
    }
  } catch (err) {
    // Store error for display in UI
    confirmError.value = err.messages?.join(', ') || err.message || 'Failed to confirm shift plan'
    // Also show toast for immediate feedback
    toast.error(confirmError.value)
  } finally {
    confirming.value = false
  }
}

// Handle Cancel Shift Plan
const handleCancelPlan = async () => {
  if (!confirm('Are you sure you want to cancel this shift plan?')) {
    return
  }

  // Clear any previous errors
  confirmError.value = null
  cancelling.value = true

  try {
    await doc.value.setValue.submit({ status: 'Cancelled' })
    await doc.value.reload()
    toast.success('Shift Plan cancelled successfully')
  } catch (err) {
    // Store error for display in UI
    confirmError.value = err.messages?.join(', ') || err.message || 'Failed to cancel shift plan'
    // Also show toast for immediate feedback
    toast.error(confirmError.value)
  } finally {
    cancelling.value = false
  }
}

// Handle Refresh
const handleRefresh = async () => {
  refreshing.value = true
  try {
    await doc.value.reload()
    toast.success('Shift Plan refreshed')
  } catch (err) {
    toast.error('Failed to refresh')
  } finally {
    refreshing.value = false
  }
}

// Handle Cancel (Edit mode)
const handleCancel = () => {
  if (!docname.value) {
    router.push('/production/shift-plans')
  } else {
    doc.value.reload()
  }
}

// Job Cards Tab Configuration
const jobCardFilters = computed(() => {
  return [['shift_plan', '=', doc.value?.doc?.name]]
})

const jobCardColumns = [
  { fieldname: 'name', label: 'Job Card ID' },
  { fieldname: 'machine', label: 'Machine' },
  { fieldname: 'date', label: 'Date' },
  { fieldname: 'shift', label: 'Shift' },
  { fieldname: 'job_name', label: 'Job Name' },
  { fieldname: 'completed_quantity', label: 'Completed' },
  { fieldname: 'target_quantity', label: 'Target' },
  { fieldname: 'progress', label: 'Progress' },
  { fieldname: 'status', label: 'Status' }
]

// Utility functions
const getStatusClass = (status) => {
  if (!status) return 'bg-gray-100 text-gray-800'
  const statusLower = status.toLowerCase()

  if (statusLower === 'confirmed') {
    return 'bg-green-100 text-green-800'
  } else if (statusLower === 'cancelled') {
    return 'bg-red-100 text-red-800'
  } else if (statusLower === 'draft') {
    return 'bg-yellow-100 text-yellow-800'
  }
  return 'bg-gray-100 text-gray-800'
}

const getJobCardStatusClass = (status) => {
  if (!status) return 'bg-gray-100 text-gray-800'
  const statusLower = status.toLowerCase()

  if (statusLower.includes('active') || statusLower.includes('progress') || statusLower.includes('running')) {
    return 'bg-green-100 text-green-800'
  } else if (statusLower.includes('complete') || statusLower.includes('done')) {
    return 'bg-blue-100 text-blue-800'
  } else if (statusLower.includes('cancelled') || statusLower.includes('failed')) {
    return 'bg-red-100 text-red-800'
  }
  return 'bg-yellow-100 text-yellow-800'
}

const getProgressPercentage = (job) => {
  if (!job.target_quantity || job.target_quantity === 0) return 0
  const completed = job.completed_quantity || 0
  const target = job.target_quantity
  return Math.min(Math.round((completed / target) * 100), 100)
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    return new Date(dateString).toLocaleDateString('en-GB')
  } catch {
    return 'Invalid Date'
  }
}

const formatDuration = (seconds) => {
  if (!seconds || seconds === 0) return '-'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${hours}h ${minutes}m`
}

// Convert seconds to hours for display in input
const getDurationHours = (seconds) => {
  if (!seconds || seconds === 0) return ''
  return (seconds / 3600).toFixed(2)
}

// Convert hours to seconds for storage
const setDurationHours = (row, hoursValue) => {
  const hours = parseFloat(hoursValue)
  row.job_one_duration = hours ? Math.round(hours * 3600) : 0
}

// Initialize
onMounted(() => {
  if (!docname.value) {
    initializeNewForm()
  }
})
</script>

<style scoped>
/* Custom styles for table inputs */
table input[type="number"],
table input[type="text"] {
  min-height: 32px;
}

/* Ensure autocomplete fits in table cells */
:deep(.autocomplete-container) {
  width: 100%;
}
</style>
