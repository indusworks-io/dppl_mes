<template>
  <div class="detail-view p-6">
    <!-- Loading State -->
    <div v-if="isLoadingSchema || (props.name && isLoadingDoc)" class="flex items-center justify-center py-12">
      <div class="text-center">
        <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p class="text-gray-600">Loading...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
      <p class="text-red-800">{{ error }}</p>
    </div>

    <!-- Main Content -->
    <div v-else>
      <!-- Header Section -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div class="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ currentMode === 'create' ? `New ${props.doctype}` : formData.name || props.doctype }}
            </h1>
            <p class="text-sm text-gray-500 mt-1">{{ props.doctype }}</p>
          </div>

          <div class="flex items-center gap-2">
            <!-- View Mode Actions -->
            <template v-if="currentMode === 'view'">
              <Button @click="handleRefresh" :disabled="refreshing">
                <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': refreshing }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                Refresh
              </Button>
              <Button @click="handleEdit">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
                Edit
              </Button>
              <Button @click="handleDelete" :disabled="deleting">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
                Delete
              </Button>
            </template>

            <!-- Edit/Create Mode Actions -->
            <template v-else>
              <Button @click="handleCancel">
                Cancel
              </Button>
              <Button @click="handleSave" :disabled="saving">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                {{ saving ? 'Saving...' : 'Save' }}
              </Button>
            </template>
          </div>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
        <p class="text-green-800">{{ successMessage }}</p>
      </div>

      <!-- Form Section -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <template v-for="field in visibleFields" :key="field.fieldname">
            <!-- Full Width Fields -->
            <div v-if="isFullWidthField(field)" class="col-span-1 md:col-span-2">
              <div class="mb-2">
                <label class="block text-sm font-medium text-gray-700">
                  {{ field.label }}
                  <span v-if="field.reqd" class="text-red-500">*</span>
                </label>
              </div>
              <component
                :is="getFieldComponent(field)"
                v-bind="getFieldProps(field)"
                v-model="formData[field.fieldname]"
                :disabled="currentMode === 'view' || field.read_only"
              />
            </div>

            <!-- Regular Fields -->
            <div v-else>
              <div class="mb-2">
                <label class="block text-sm font-medium text-gray-700">
                  {{ field.label }}
                  <span v-if="field.reqd" class="text-red-500">*</span>
                </label>
              </div>

              <!-- View Mode - Display as text -->
              <template v-if="currentMode === 'view'">
                <p class="text-gray-900">{{ formatFieldValue(field, formData[field.fieldname]) }}</p>
              </template>

              <!-- Edit/Create Mode - Render input -->
              <template v-else>
                <!-- Select Field with Options -->
                <select
                  v-if="field.fieldtype === 'Select'"
                  v-model="formData[field.fieldname]"
                  :disabled="field.read_only"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Select...</option>
                  <option
                    v-for="option in getSelectOptions(field)"
                    :key="option"
                    :value="option"
                  >
                    {{ option }}
                  </option>
                </select>

                <!-- Link Field with Autocomplete -->
                <Autocomplete
                  v-else-if="field.fieldtype === 'Link'"
                  v-model="formData[field.fieldname]"
                  :doctype="field.options"
                  :disabled="field.read_only"
                />

                <!-- Checkbox -->
                <input
                  v-else-if="field.fieldtype === 'Check'"
                  type="checkbox"
                  v-model="formData[field.fieldname]"
                  :disabled="field.read_only"
                  class="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />

                <!-- Other Fields -->
                <component
                  v-else
                  :is="getFieldComponent(field)"
                  v-bind="getFieldProps(field)"
                  v-model="formData[field.fieldname]"
                  :disabled="field.read_only"
                />
              </template>
            </div>
          </template>
        </div>
      </div>

      <!-- Related Records Section -->
      <div v-if="props.related && props.related.length > 0 && currentMode === 'view' && formData.name">
        <div v-for="relatedDoctype in props.related" :key="relatedDoctype" class="mb-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">{{ relatedDoctype }}</h2>
            <ListView
              :doctype="relatedDoctype"
              :title="relatedDoctype"
              :filters="getRelatedFilters(relatedDoctype)"
              :columns="getRelatedColumns(relatedDoctype)"
              :enable-routing="false"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createDocumentResource, createResource } from 'frappe-ui'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import ListView from './ListView.vue'

// Props
const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    default: null,
  },
  related: {
    type: Array,
    default: () => [],
  },
})

// Emits
const emit = defineEmits(['saved', 'deleted', 'cancel', 'refreshed'])

// State
const currentMode = ref(props.name ? 'view' : 'create')
const formData = reactive({})
const schemaFields = ref([])
const isLoadingSchema = ref(true)
const isLoadingDoc = ref(false)
const error = ref('')
const successMessage = ref('')
const saving = ref(false)
const deleting = ref(false)
const refreshing = ref(false)
const originalData = ref({})

// Schema Resource
const schemaResource = createResource({
  url: 'frappe.desk.form.load.getdoctype',
  params: {
    doctype: props.doctype,
  },
  auto: true,
  onSuccess(data) {
    if (data && data.docs && data.docs.length > 0) {
      const doctypeMeta = data.docs[0]
      schemaFields.value = doctypeMeta.fields || []
      initializeFormData()
      isLoadingSchema.value = false
    }
  },
  onError(err) {
    error.value = `Failed to load schema: ${err.message}`
    isLoadingSchema.value = false
  },
})

// Document Resource (for existing records)
let documentResource = null

// Initialize document resource for existing records
const initDocumentResource = () => {
  if (!props.name) return

  documentResource = createDocumentResource({
    doctype: props.doctype,
    name: props.name,
    auto: true,
    onSuccess(data) {
      Object.keys(data).forEach(key => {
        formData[key] = data[key]
      })
      originalData.value = { ...data }
      isLoadingDoc.value = false
    },
    onError(err) {
      error.value = `Failed to load document: ${err.message}`
      isLoadingDoc.value = false
    },
  })
}

// Initialize form data with defaults
const initializeFormData = () => {
  if (props.name) {
    isLoadingDoc.value = true
    initDocumentResource()
  } else {
    // Initialize with default values from schema
    schemaFields.value.forEach(field => {
      if (field.default) {
        formData[field.fieldname] = field.default
      } else if (field.fieldtype === 'Check') {
        formData[field.fieldname] = 0
      } else {
        formData[field.fieldname] = null
      }
    })
  }
}

// Computed: Visible fields (exclude hidden and system fields)
const visibleFields = computed(() => {
  return schemaFields.value.filter(field => {
    return !field.hidden &&
           field.fieldtype !== 'Section Break' &&
           field.fieldtype !== 'Column Break' &&
           field.fieldtype !== 'Tab Break' &&
           field.fieldtype !== 'HTML' &&
           field.fieldtype !== 'Table'
  })
})

// Check if field should span full width
const isFullWidthField = (field) => {
  return ['Text', 'Text Editor', 'Long Text', 'Small Text'].includes(field.fieldtype)
}

// Get component for field type
const getFieldComponent = (field) => {
  if (currentMode.value === 'view') {
    return 'div'
  }

  const typeMap = {
    'Data': 'Input',
    'Small Text': 'Textarea',
    'Text': 'Textarea',
    'Long Text': 'Textarea',
    'Int': 'Input',
    'Float': 'Input',
    'Currency': 'Input',
    'Percent': 'Input',
    'Date': 'Input',
    'Datetime': 'Input',
    'Time': 'Input',
    'Select': 'select',
    'Link': 'Input',
    'Check': 'input',
    'Password': 'Input',
  }

  return typeMap[field.fieldtype] || 'Input'
}

// Get props for field component
const getFieldProps = (field) => {
  const props = {}

  if (field.fieldtype === 'Int' || field.fieldtype === 'Float' ||
      field.fieldtype === 'Currency' || field.fieldtype === 'Percent') {
    props.type = 'number'
    if (field.fieldtype === 'Float' || field.fieldtype === 'Currency' || field.fieldtype === 'Percent') {
      props.step = '0.01'
    }
  } else if (field.fieldtype === 'Date') {
    props.type = 'date'
  } else if (field.fieldtype === 'Datetime') {
    props.type = 'datetime-local'
  } else if (field.fieldtype === 'Time') {
    props.type = 'time'
  } else if (field.fieldtype === 'Check') {
    props.type = 'checkbox'
  } else if (field.fieldtype === 'Password') {
    props.type = 'password'
  } else {
    props.type = 'text'
  }

  if (field.placeholder) {
    props.placeholder = field.placeholder
  }

  return props
}

// Get select options from field
const getSelectOptions = (field) => {
  if (!field.options) return []

  // Options are stored as newline-separated string in Frappe
  return field.options.split('\n').filter(opt => opt.trim() !== '')
}

// Format field value for display
const formatFieldValue = (field, value) => {
  if (value === null || value === undefined || value === '') {
    return '-'
  }

  if (field.fieldtype === 'Check') {
    return value ? 'Yes' : 'No'
  }

  if (field.fieldtype === 'Date') {
    try {
      return new Date(value).toLocaleDateString('en-GB')
    } catch {
      return value
    }
  }

  if (field.fieldtype === 'Datetime') {
    try {
      const date = new Date(value)
      return date.toLocaleString('en-GB')
    } catch {
      return value
    }
  }

  return value
}

// Get filters for related doctype
const getRelatedFilters = (relatedDoctype) => {
  // Try to auto-detect link field
  const linkFieldName = props.doctype.toLowerCase().replace(' ', '_')
  return [[linkFieldName, '=', formData.name]]
}

// Get columns for related doctype
const getRelatedColumns = (relatedDoctype) => {
  // Return basic columns - this can be customized
  return [
    { fieldname: 'name', label: 'ID' },
    { fieldname: 'modified', label: 'Modified', formatter: (val) => new Date(val).toLocaleDateString('en-GB') },
  ]
}

// Validate required fields
const validateForm = () => {
  const requiredFields = visibleFields.value.filter(f => f.reqd)
  for (const field of requiredFields) {
    if (!formData[field.fieldname]) {
      error.value = `${field.label} is required`
      return false
    }
  }
  return true
}

// Handle Save
const handleSave = async () => {
  error.value = ''
  successMessage.value = ''

  if (!validateForm()) {
    return
  }

  saving.value = true

  try {
    if (currentMode.value === 'create') {
      // Create new document
      const insertResource = createResource({
        url: 'frappe.client.insert',
        makeParams() {
          return {
            doc: {
              doctype: props.doctype,
              ...formData,
            },
          }
        },
      })

      await insertResource.fetch()

      if (insertResource.data) {
        successMessage.value = 'Document created successfully!'
        Object.keys(insertResource.data).forEach(key => {
          formData[key] = insertResource.data[key]
        })
        currentMode.value = 'view'
        emit('saved', insertResource.data)
      }
    } else {
      // Update existing document
      if (documentResource) {
        await documentResource.setValue.submit(formData)
        successMessage.value = 'Document updated successfully!'
        originalData.value = { ...formData }
        currentMode.value = 'view'
        emit('saved', formData)
      }
    }

    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err) {
    error.value = `Failed to save: ${err.message || 'Unknown error'}`
  } finally {
    saving.value = false
  }
}

// Handle Delete
const handleDelete = async () => {
  if (!confirm(`Are you sure you want to delete this ${props.doctype}?`)) {
    return
  }

  deleting.value = true
  error.value = ''

  try {
    if (documentResource) {
      await documentResource.delete.submit()
      successMessage.value = 'Document deleted successfully!'
      emit('deleted', formData.name)

      setTimeout(() => {
        successMessage.value = ''
      }, 2000)
    }
  } catch (err) {
    error.value = `Failed to delete: ${err.message}`
  } finally {
    deleting.value = false
  }
}

// Handle Refresh
const handleRefresh = async () => {
  if (!documentResource) return

  refreshing.value = true
  error.value = ''

  try {
    await documentResource.reload()
    successMessage.value = 'Document refreshed successfully!'
    emit('refreshed', formData)

    setTimeout(() => {
      successMessage.value = ''
    }, 2000)
  } catch (err) {
    error.value = `Failed to refresh: ${err.message}`
  } finally {
    refreshing.value = false
  }
}

// Handle Edit
const handleEdit = () => {
  currentMode.value = 'edit'
}

// Handle Cancel
const handleCancel = () => {
  if (currentMode.value === 'create') {
    emit('cancel')
  } else {
    // Restore original data
    Object.keys(originalData.value).forEach(key => {
      formData[key] = originalData.value[key]
    })
    currentMode.value = 'view'
    emit('cancel')
  }
}

// Watch for name prop changes
watch(() => props.name, (newName) => {
  if (newName) {
    currentMode.value = 'view'
    isLoadingDoc.value = true
    initDocumentResource()
  } else {
    currentMode.value = 'create'
    initializeFormData()
  }
})
</script>

<style scoped>
/* Additional custom styles if needed */
select {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  color: #111827;
  background-color: white;
}

select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

select:disabled {
  background-color: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
}

textarea {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  color: #111827;
  min-height: 100px;
  resize: vertical;
}

textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

textarea:disabled {
  background-color: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
}

input[type="checkbox"] {
  width: 1.25rem;
  height: 1.25rem;
  border: 1px solid #d1d5db;
  border-radius: 0.25rem;
  cursor: pointer;
}

input[type="checkbox"]:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
