<template>
  <div class="job-card-page p-6">
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
              @click="goBack"
              class="inline-flex items-center text-gray-600 hover:text-gray-900 transition-colors"
              title="Back to Job Cards"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ docname ? doc.doc.name : 'New Job Card' }}
            </h1>
          </div>

          <div class="flex items-center gap-2">
            <!-- Save Button (Create Mode Only) -->
            <button
              v-if="!docname"
              @click="handleSave"
              :disabled="doc.setValue.loading"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 focus:outline-none disabled:opacity-50"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              {{ doc.setValue.loading ? 'Saving...' : 'Save' }}
            </button>

            <!-- Edit Button (View Mode Only) -->
            <button
              v-if="docname"
              @click="openUpdateModal"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 focus:outline-none"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
              Edit
            </button>

          </div>
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
              @click="activeTab = 'outputlogs'"
              :class="[
                'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
                activeTab === 'outputlogs'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Output Logs
            </button>
            <button
              v-if="docname"
              @click="activeTab = 'downtimelogs'"
              :class="[
                'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
                activeTab === 'downtimelogs'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Downtime Logs
            </button>
          </nav>
        </div>

        <!-- Tab Content -->
        <div class="p-6">
          <!-- Overview Tab -->
          <div v-if="activeTab === 'overview'">
            <!-- Progress Bar (for existing documents) -->
            <div v-if="docname && doc.doc.target_quantity" class="progress-section mb-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Production Progress</h3>
              <div class="progress-bar-container">
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{ width: getProgressPercentage() + '%' }"
                  ></div>
                </div>
                <div class="progress-text">
                  {{ doc.doc.completed_quantity || 0 }} / {{ doc.doc.target_quantity }} completed ({{ getProgressPercentage() }}%)
                </div>
              </div>
            </div>

            <!-- Form Fields -->
            <div class="grid grid-cols-1 gap-6 mb-6">
              <!-- Create Mode Fields -->
              <template v-if="!docname">
                <!-- Machine -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Machine <span class="text-red-500">*</span>
                  </label>
                  <Autocomplete
                    v-model="doc.doc.machine"
                    :options="machineOptions"
                    placeholder="Select Machine"
                    :loading="machinesResource.loading"
                    :compareFn="(a, b) => a?.value === b?.value"
                  />
                </div>

                <!-- Date -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Date <span class="text-red-500">*</span>
                  </label>
                  <DatePicker
                    v-model="doc.doc.date"
                    placeholder="Select Date"
                    variant="outline"
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
                    :compareFn="(a, b) => a?.value === b?.value"
                  />
                </div>

                <!-- Operator -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Operator <span class="text-red-500">*</span>
                  </label>
                  <Autocomplete
                    v-model="doc.doc.operator"
                    :options="operatorOptions"
                    placeholder="Select Operator"
                    :loading="operatorsResource.loading"
                    :compareFn="(a, b) => a?.value === b?.value"
                  />
                </div>

                <!-- Job Name -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Job Name <span class="text-red-500">*</span>
                  </label>
                  <Autocomplete
                    v-model="doc.doc.job_name"
                    :options="jobOptions"
                    placeholder="Select Job"
                    :loading="jobsResource.loading"
                    :compareFn="(a, b) => a?.value === b?.value"
                  />
                </div>

                <!-- Target Quantity -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Target Quantity <span class="text-red-500">*</span>
                  </label>
                  <Input
                    v-model="doc.doc.target_quantity"
                    type="number"
                    placeholder="Enter target quantity"
                  />
                </div>

                <!-- Job Sequence Number -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Job Sequence Number <span class="text-red-500">*</span>
                  </label>
                  <Input
                    v-model="doc.doc.job_sequence_number"
                    type="number"
                    placeholder="Enter sequence number"
                  />
                </div>

                <!-- Planned Start Date Time -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Planned Start Date Time <span class="text-red-500">*</span>
                  </label>
                  <DateTimePicker
                    v-model="doc.doc.planned_start_date_time"
                    placeholder="Select start date time"
                    variant="outline"
                  />
                </div>

                <!-- Planned End Date Time -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Planned End Date Time <span class="text-red-500">*</span>
                  </label>
                  <DateTimePicker
                    v-model="doc.doc.planned_end_date_time"
                    placeholder="Select end date time"
                    variant="outline"
                  />
                </div>
              </template>
            </div>

            <!-- Job Card Details Grid (Read-only display, only for existing documents) -->
            <div v-if="docname" class="job-card-details-grid">
              <!-- Basic Information Card -->
              <div class="details-card">
                <div class="card-header">
                  <h3>Basic Information</h3>
                </div>
                <div class="card-content">
                  <div class="detail-item">
                    <span class="detail-label">Machine:</span>
                    <span class="detail-value">{{ getFieldValue(doc.doc.machine) || 'N/A' }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Date:</span>
                    <span class="detail-value">{{ formatDate(doc.doc.date) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Shift:</span>
                    <span class="detail-value">{{ getFieldValue(doc.doc.shift) || 'N/A' }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Operator:</span>
                    <span class="detail-value">{{ getFieldValue(doc.doc.operator) || 'N/A' }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Job Sequence:</span>
                    <span class="detail-value">{{ doc.doc.job_sequence_number || 'N/A' }}</span>
                  </div>
                </div>
              </div>

              <!-- Production Metrics Card -->
              <div class="details-card">
                <div class="card-header">
                  <h3>Production Metrics</h3>
                </div>
                <div class="card-content">
                  <div class="detail-item">
                    <span class="detail-label">Status:</span>
                    <span class="detail-value">
                      <span class="status-badge-inline" :class="getJobStatusClass(doc.doc.status)">
                        {{ doc.doc.status || 'Unknown' }}
                      </span>
                    </span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Target Quantity:</span>
                    <span class="detail-value">{{ doc.doc.target_quantity || 0 }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Completed Quantity:</span>
                    <span class="detail-value">{{ doc.doc.completed_quantity || 0 }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Balance Quantity:</span>
                    <span class="detail-value">{{ (doc.doc.target_quantity || 0) - (doc.doc.completed_quantity || 0) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Progress:</span>
                    <span class="detail-value">{{ getProgressPercentage() }}%</span>
                  </div>
                </div>
              </div>

              <!-- Performance Metrics Card -->
              <div class="details-card">
                <div class="card-header">
                  <h3>Performance Metrics</h3>
                </div>
                <div class="card-content">
                  <div class="detail-item">
                    <span class="detail-label">Planned Run Rate:</span>
                    <span class="detail-value">{{ doc.doc.planned_run_rate || 'N/A' }} per minute</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Actual Run Rate:</span>
                    <span class="detail-value">{{ doc.doc.actual_run_rate || 'N/A' }} per minute</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Planned Duration:</span>
                    <span class="detail-value">{{ formatDuration(doc.doc.planned_duration) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Actual Duration:</span>
                    <span class="detail-value">{{ formatDuration(doc.doc.actual_duration) }}</span>
                  </div>
                </div>
              </div>

              <!-- Timing Information Card -->
              <div class="details-card">
                <div class="card-header">
                  <h3>Timing Information</h3>
                </div>
                <div class="card-content">
                  <div class="detail-item">
                    <span class="detail-label">Planned Start:</span>
                    <span class="detail-value">{{ formatDateTime(doc.doc.planned_start_date_time) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Planned End:</span>
                    <span class="detail-value">{{ formatDateTime(doc.doc.planned_end_date_time) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Actual Start:</span>
                    <span class="detail-value">{{ formatDateTime(doc.doc.actual_start_date_time) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Actual End:</span>
                    <span class="detail-value">{{ formatDateTime(doc.doc.actual_end_date_time) }}</span>
                  </div>
                </div>
              </div>

              <!-- Wastage Information Card -->
              <div class="details-card">
                <div class="card-header">
                  <h3>Wastage Information</h3>
                </div>
                <div class="card-content">
                  <div class="detail-item">
                    <span class="detail-label">Machine Wastage:</span>
                    <span class="detail-value">{{ formatWastage(doc.doc.machine_wastage) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Job Setting Wastage:</span>
                    <span class="detail-value">{{ formatWastage(doc.doc.job_setting_wastage) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Roll Wastage:</span>
                    <span class="detail-value">{{ formatWastage(doc.doc.roll_wastage) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Printing Wastage:</span>
                    <span class="detail-value">{{ formatWastage(doc.doc.printing_wastage) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Barcode Wastage:</span>
                    <span class="detail-value">{{ formatWastage(doc.doc.barcode_wastage) }}</span>
                  </div>
                  <div class="detail-item total-wastage">
                    <span class="detail-label">Total Wastage:</span>
                    <span class="detail-value">{{ formatWastage(doc.doc.total_wastage) }}</span>
                  </div>
                </div>
              </div>

              <!-- Downtime Information Card (for existing docs) -->
              <div v-if="docname" class="details-card">
                <div class="card-header">
                  <h3>Downtime Information</h3>
                </div>
                <div class="card-content">
                  <div class="detail-item">
                    <span class="detail-label">Total Downtime Duration:</span>
                    <span class="detail-value">{{ formatDowntimeDuration(totalDowntimeDuration) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Number of Downtime Events:</span>
                    <span class="detail-value">{{ downtimeLogsCount }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Output Logs Tab -->
          <div v-if="activeTab === 'outputlogs' && docname">
            <ListView
              doctype="Output Log"
              title="Output Logs"
              :columns="outputLogColumns"
              :fields="['name', 'timestamp', 'output', 'run_rate', 'machine']"
              :filters="outputLogFilters"
              :hideHeader="true"
              :hideSubheader="true"
              orderBy="timestamp desc"
              :pageLength="50"
              :enableRouting="true"
              routePrefix="/production/output-logs"
            >
              <!-- Custom Timestamp Cell -->
              <template #cell-timestamp="{ value }">
                {{ formatDateTime(value) }}
              </template>

              <!-- Custom Run Rate Cell -->
              <template #cell-run_rate="{ value }">
                {{ value ? Number.parseFloat(value).toFixed(2) : 'N/A' }}
              </template>
            </ListView>
          </div>

          <!-- Downtime Logs Tab -->
          <div v-if="activeTab === 'downtimelogs' && docname">
            <ListView
              doctype="Downtime Log"
              title="Downtime Logs"
              :columns="downtimeLogColumns"
              :fields="['name', 'status', 'start_date_time', 'end_date_time', 'duration', 'reason', 'category', 'machine']"
              :filters="downtimeLogFilters"
              :hideHeader="true"
              :hideSubheader="true"
              orderBy="start_date_time desc"
              :pageLength="50"
              :enableRouting="true"
              routePrefix="/production/downtime-logs"
            >
              <!-- Custom Status Cell -->
              <template #cell-status="{ value }">
                <span :class="getDowntimeStatusClass(value)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                  {{ value || 'Unknown' }}
                </span>
              </template>

              <!-- Custom Start Date Time Cell -->
              <template #cell-start_date_time="{ value }">
                {{ formatDateTime(value) }}
              </template>

              <!-- Custom End Date Time Cell -->
              <template #cell-end_date_time="{ value }">
                {{ formatDateTime(value) }}
              </template>

              <!-- Custom Duration Cell -->
              <template #cell-duration="{ value }">
                {{ formatDowntimeDuration(value) }}
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
          </div>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="fixed top-4 right-4 z-50">
        <div class="bg-green-50 border border-green-200 rounded-lg p-4 shadow-lg flex items-center gap-3 animate-fade-in">
          <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <span class="text-green-800 font-medium">{{ successMessage }}</span>
        </div>
      </div>

      <!-- Update Modal -->
      <JobCardUpdateModal
        :is-visible="isUpdateModalVisible"
        :job-card-data="doc.doc"
        @close="closeUpdateModal"
        @updated="handleJobCardUpdated"
      />

      <!-- Update Reason Dialog -->
      <UpdateReasonDialog
        :visible="isReasonDialogVisible"
        :downtimeId="selectedDowntimeId"
        @update="handleReasonUpdated"
        @cancel="closeReasonDialog"
      />
    </div>
  </div>
</template>

<script setup>
import { createDocumentResource, createListResource, createResource, Autocomplete, DatePicker, DateTimePicker, Input, toast } from 'frappe-ui'
import { computed, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ListView from '../../components/ListView.vue'
import JobCardUpdateModal from '../../components/JobCardUpdateModal.vue'
import UpdateReasonDialog from '../../components/UpdateReasonDialog.vue'

const route = useRoute()
const router = useRouter()

// State
const activeTab = ref('overview')
const isUpdateModalVisible = ref(false)
const successMessage = ref('')
const isReasonDialogVisible = ref(false)
const selectedDowntimeId = ref(null)

// Compute docname from route
const docname = computed(() => {
  const id = route.params.id
  return (id === 'new' || !id) ? undefined : id
})

// Document resource - initialize reactively based on docname
const docResource = ref(null)

// Computed property to access doc without .value in template
const doc = computed(() => docResource.value)

// Function to initialize/reinitialize document resource
const initializeDoc = () => {
  const id = docname.value
  if (id && id !== 'new') {
    // Existing document - use createDocumentResource
    docResource.value = createDocumentResource({
      doctype: 'Job Card',
      name: id,
      auto: true,
      setValue: {
        onSuccess: () => {
          toast.success('Job Card updated successfully')
        },
        onError: (err) => {
          toast.error(err.messages?.join(', ') || 'Failed to update')
        }
      }
    })
  } else {
    // New document - create a reactive document structure
    docResource.value = reactive({
      doc: {
        doctype: 'Job Card',
        machine: null,
        date: new Date().toISOString().split('T')[0],
        shift: null,
        operator: null,
        job_name: null,
        target_quantity: null,
        job_sequence_number: 1,
        planned_start_date_time: null,
        planned_end_date_time: null,
        status: 'Not Started'
      },
      loading: false,
      setValue: {
        loading: false,
        submit: () => Promise.resolve()
      },
      reload: () => Promise.resolve(),
      save: async () => {
        // This will be implemented in handleSave
        return Promise.resolve()
      }
    })
  }
}

// Initialize document on mount
initializeDoc()

// Watch for route param changes and reinitialize document resource
watch(docname, () => {
  initializeDoc()
  activeTab.value = 'overview' // Reset to overview tab
})

// List resources for link fields
const machinesResource = createListResource({
  doctype: 'Machine',
  fields: ['name', 'machine_name'],
  filters: { is_active: 1 },
  auto: true,
  pageLength: '*',
})

const shiftsResource = createListResource({
  doctype: 'Shift Type',
  fields: ['name', 'shift_type'],
  auto: true,
  pageLength: '*',
})

const operatorsResource = createListResource({
  doctype: 'Operator',
  fields: ['name', 'operator_name'],
  filters: { is_active: 1 },
  auto: true,
  pageLength: '*',
})

const jobsResource = createListResource({
  doctype: 'Job',
  fields: ['name', 'job_name', 'job_number'],
  auto: true,
  pageLength: '*',
})

// List resources for related records (only for existing documents)
const outputLogsResource = computed(() => {
  if (!docname.value) return null
  return createListResource({
    doctype: 'Output Log',
    fields: ['name', 'timestamp', 'output', 'run_rate', 'machine'],
    filters: {
      job_card: docname.value
    },
    auto: true,
  })
})

const downtimeLogsResource = computed(() => {
  if (!docname.value) return null
  return createListResource({
    doctype: 'Downtime Log',
    fields: ['name', 'status', 'start_date_time', 'end_date_time', 'duration', 'reason', 'category', 'machine'],
    filters: {
      job_card: docname.value
    },
    auto: true,
  })
})

// Convert list resources to Autocomplete options format
const machineOptions = computed(() => {
  if (!machinesResource.data) return []
  return machinesResource.data.map(machine => ({
    label: machine.machine_name || machine.name,
    value: machine.name
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

// Helper function to extract value from Autocomplete option objects
const getFieldValue = (value) => {
  if (!value) return null
  return typeof value === 'object' && value.value !== undefined ? value.value : value
}

// Filters for related records tabs
const outputLogFilters = computed(() => {
  return [['job_card', '=', docname.value]]
})

const downtimeLogFilters = computed(() => {
  return [['job_card', '=', docname.value]]
})

// Column definitions for list views
const outputLogColumns = [
  { fieldname: 'name', label: 'ID' },
  { fieldname: 'timestamp', label: 'Timestamp' },
  { fieldname: 'machine', label: 'Machine' },
  { fieldname: 'output', label: 'Output' },
  { fieldname: 'run_rate', label: 'Run Rate' }
]

const downtimeLogColumns = [
  { fieldname: 'name', label: 'ID' },
  { fieldname: 'status', label: 'Status' },
  { fieldname: 'machine', label: 'Machine' },
  { fieldname: 'start_date_time', label: 'Start' },
  { fieldname: 'end_date_time', label: 'End' },
  { fieldname: 'duration', label: 'Duration' },
  { fieldname: 'reason', label: 'Reason' },
  { fieldname: 'category', label: 'Category' },
  { fieldname: 'actions', label: 'Actions' }
]

// Computed properties for downtime summary
const totalDowntimeDuration = computed(() => {
  if (!downtimeLogsResource.value?.data || downtimeLogsResource.value.data.length === 0) {
    return 0
  }
  return downtimeLogsResource.value.data.reduce((total, log) => {
    return total + (log.duration || 0)
  }, 0)
})

const downtimeLogsCount = computed(() => {
  return downtimeLogsResource.value?.data ? downtimeLogsResource.value.data.length : 0
})

// Validation
const validateForm = () => {
  if (!docname.value) {
    // Create mode validation
    if (!doc.value.doc.machine) {
      toast.error('Machine is required')
      return false
    }
    if (!doc.value.doc.date) {
      toast.error('Date is required')
      return false
    }
    if (!doc.value.doc.shift) {
      toast.error('Shift is required')
      return false
    }
    if (!doc.value.doc.operator) {
      toast.error('Operator is required')
      return false
    }
    if (!doc.value.doc.job_name) {
      toast.error('Job Name is required')
      return false
    }
    if (!doc.value.doc.target_quantity) {
      toast.error('Target Quantity is required')
      return false
    }
    if (!doc.value.doc.planned_start_date_time) {
      toast.error('Planned Start Date Time is required')
      return false
    }
    if (!doc.value.doc.planned_end_date_time) {
      toast.error('Planned End Date Time is required')
      return false
    }
  }
  return true
}

// Handle Save
const handleSave = async () => {
  if (!validateForm()) {
    return
  }

  try {
    if (docname.value) {
      // Update existing document
      const dataToSave = {}

      // Only include editable fields for update mode
      if (doc.value.doc.status !== undefined) {
        dataToSave.status = doc.value.doc.status
      }
      if (doc.value.doc.completed_quantity !== undefined) {
        dataToSave.completed_quantity = doc.value.doc.completed_quantity
      }
      if (doc.value.doc.machine_wastage !== undefined) {
        dataToSave.machine_wastage = doc.value.doc.machine_wastage
      }
      if (doc.value.doc.job_setting_wastage !== undefined) {
        dataToSave.job_setting_wastage = doc.value.doc.job_setting_wastage
      }
      if (doc.value.doc.roll_wastage !== undefined) {
        dataToSave.roll_wastage = doc.value.doc.roll_wastage
      }
      if (doc.value.doc.printing_wastage !== undefined) {
        dataToSave.printing_wastage = doc.value.doc.printing_wastage
      }
      if (doc.value.doc.barcode_wastage !== undefined) {
        dataToSave.barcode_wastage = doc.value.doc.barcode_wastage
      }

      await doc.value.setValue.submit(dataToSave)
      await doc.value.reload()
    } else {
      // Create new document
      const dataToSave = {
        doctype: 'Job Card',
        machine: getFieldValue(doc.value.doc.machine),
        date: doc.value.doc.date,
        shift: getFieldValue(doc.value.doc.shift),
        operator: getFieldValue(doc.value.doc.operator),
        job_name: getFieldValue(doc.value.doc.job_name),
        target_quantity: doc.value.doc.target_quantity,
        job_sequence_number: doc.value.doc.job_sequence_number,
        planned_start_date_time: doc.value.doc.planned_start_date_time,
        planned_end_date_time: doc.value.doc.planned_end_date_time,
        status: doc.value.doc.status || 'Not Started'
      }

      const insertResource = createResource({
        url: 'frappe.client.insert',
        makeParams: () => ({
          doc: dataToSave
        })
      })

      const result = await insertResource.fetch()

      if (result) {
        toast.success('Job Card created successfully')
        // Navigate to the new document
        router.push(`/production/job-cards/${result.name}`)
      }
    }
  } catch (err) {
    toast.error(err.messages?.join(', ') || err.message || 'Failed to save')
    console.error(err)
  }
}

// Navigation
const goBack = () => {
  router.push('/production/job-cards')
}

// Utility functions
const formatDate = (dateString) => {
  if (!dateString) return "N/A"
  try {
    return new Date(dateString).toLocaleDateString("en-GB")
  } catch {
    return "Invalid Date"
  }
}

const formatDateTime = (dateTimeString) => {
  if (!dateTimeString) return "N/A"
  try {
    const date = new Date(dateTimeString)

    // Format date as DD/MM/YYYY
    const day = date.getDate().toString().padStart(2, "0")
    const month = (date.getMonth() + 1).toString().padStart(2, "0")
    const year = date.getFullYear()

    // Format time in 12-hour AM/PM format
    let hours = date.getHours()
    const minutes = date.getMinutes().toString().padStart(2, "0")
    const ampm = hours >= 12 ? "PM" : "AM"
    hours = hours % 12
    hours = hours ? hours : 12 // Convert 0 to 12
    const formattedHours = hours.toString().padStart(2, "0")

    return `${day}/${month}/${year} ${formattedHours}:${minutes} ${ampm}`
  } catch {
    return "Invalid DateTime"
  }
}

const formatDuration = (seconds) => {
  if (!seconds || seconds === 0) return "N/A"

  const totalSeconds = Math.floor(seconds)
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)

  if (hours > 0 && minutes > 0) {
    return `${hours}h ${minutes}m`
  } else if (hours > 0) {
    return `${hours}h`
  } else if (minutes > 0) {
    return `${minutes}m`
  } else {
    return "< 1m"
  }
}

const formatDowntimeDuration = (seconds) => {
  if (!seconds || seconds === 0) return "0h 0m 0s"

  const totalSeconds = Math.floor(seconds)
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const secs = totalSeconds % 60

  const parts = []
  if (hours > 0) parts.push(`${hours}h`)
  if (minutes > 0) parts.push(`${minutes}m`)
  if (secs > 0 || parts.length === 0) parts.push(`${secs}s`)

  return parts.join(" ")
}

const formatWastage = (wastage) => {
  if (!wastage || wastage === 0) return "0.00 kg"
  return `${Number.parseFloat(wastage).toFixed(2)} kg`
}

const getJobStatusClass = (status) => {
  if (!status) return "status-unknown"
  const statusLower = status.toLowerCase()
  if (statusLower.includes("progress") || statusLower.includes("active")) {
    return "status-active"
  } else if (statusLower.includes("complete") || statusLower.includes("done")) {
    return "status-complete"
  } else if (
    statusLower.includes("cancelled") ||
    statusLower.includes("failed")
  ) {
    return "status-error"
  }
  return "status-pending"
}

const getDowntimeStatusClass = (status) => {
  if (!status) return 'bg-gray-100 text-gray-800'
  const statusLower = status.toLowerCase()
  if (statusLower === 'open') {
    return 'bg-red-100 text-red-800'
  } else if (statusLower === 'closed') {
    return 'bg-green-100 text-green-800'
  }
  return 'bg-gray-100 text-gray-800'
}

const getProgressPercentage = () => {
  if (!doc.value || !doc.value.doc || !doc.value.doc.target_quantity) return 0
  const completed = doc.value.doc.completed_quantity || 0
  const target = doc.value.doc.target_quantity
  return Math.round((completed / target) * 100)
}

// Modal handling methods
const openUpdateModal = () => {
  isUpdateModalVisible.value = true
}

const closeUpdateModal = () => {
  isUpdateModalVisible.value = false
}

const handleJobCardUpdated = () => {
  // Refresh the job card data after successful update
  if (docResource.value && docResource.value.reload) {
    docResource.value.reload()
  }
  successMessage.value = 'Job card updated successfully!'

  // Clear success message after 3 seconds
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}

// Dialog handlers for Update Reason
const openUpdateReasonDialog = (downtimeId) => {
  selectedDowntimeId.value = downtimeId
  isReasonDialogVisible.value = true
}

const closeReasonDialog = () => {
  isReasonDialogVisible.value = false
  selectedDowntimeId.value = null
}

const handleReasonUpdated = () => {
  // Close the dialog
  closeReasonDialog()
  // Reload downtime logs data
  if (downtimeLogsResource.value) {
    downtimeLogsResource.value.reload()
  }
  // Show success message
  successMessage.value = 'Downtime reason updated successfully!'
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}
</script>

<style scoped>
.job-card-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}


/* Animation for success message */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}

/* Status Badge */
.status-badge {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  flex-shrink: 0;
}

.status-badge-inline {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
}

.status-active {
  background-color: #d4edda;
  color: #155724;
}

.status-complete {
  background-color: #d4edda;
  color: #155724;
}

.status-pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-error {
  background-color: #f8d7da;
  color: #721c24;
}

.status-unknown {
  background-color: #e2e3e5;
  color: #6c757d;
}

/* Progress Section */
.progress-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.progress-bar-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.progress-bar {
  width: 100%;
  height: 20px;
  background-color: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #28a745, #20c997);
  border-radius: 10px;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  font-weight: 500;
  color: #495057;
}

/* Details Grid */
.job-card-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.details-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  background-color: #f8f9fa;
  padding: 16px 24px;
  border-bottom: 1px solid #e9ecef;
}

.card-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
}

.card-content {
  padding: 20px 24px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f8f9fa;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 600;
  color: #6c757d;
  font-size: 0.9rem;
}

.detail-value {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
  text-align: right;
}

/* Total Wastage Styling */
.total-wastage {
  border-top: 2px solid #e9ecef;
  margin-top: 8px;
  padding-top: 16px;
  font-weight: 600;
}

.total-wastage .detail-label {
  font-weight: 700;
  color: #495057;
}

.total-wastage .detail-value {
  font-weight: 700;
  color: #dc3545;
  font-size: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .job-card-details-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
    padding: 10px 0;
  }

  .detail-value {
    text-align: left;
    font-weight: 600;
  }
}
</style>
