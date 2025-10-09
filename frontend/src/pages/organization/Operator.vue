<template>
  <div class="operator-page p-6">
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
              title="Back to Operators"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ docname ? doc.doc.operator_name || doc.doc.name : 'New Operator' }}
            </h1>
          </div>

          <div class="flex items-center gap-2">
            <button
              v-if="!docname"
              @click="goBack"
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
          </div>
        </div>
      </div>

      <!-- Form Fields -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="space-y-6 max-w-2xl">
          <!-- Operator Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Operator Name <span class="text-red-500">*</span>
            </label>
            <Input
              v-model="doc.doc.operator_name"
              type="text"
              placeholder="Enter operator name"
              :disabled="!!docname"
            />
            <p v-if="docname" class="mt-1 text-xs text-gray-500">Operator name cannot be changed after creation</p>
          </div>

          <!-- Employee Code -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Employee Code
            </label>
            <Input
              v-model="doc.doc.employee_code"
              type="text"
              placeholder="Enter employee code (optional)"
            />
          </div>

          <!-- Is Active -->
          <div>
            <Checkbox
              v-model="doc.doc.is_active"
              label="Is Active?"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createDocumentResource, createResource, Input, Checkbox, toast } from 'frappe-ui'
import { computed, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Compute docname from route
const docname = computed(() => {
  const name = route.params.name
  return (name === 'new' || !name) ? undefined : name
})

// Document resource
const docResource = ref(null)
const doc = computed(() => docResource.value)

// Initialize document
const initializeDoc = () => {
  if (docname.value) {
    // Update mode
    docResource.value = createDocumentResource({
      doctype: 'Operator',
      name: docname.value,
      auto: true,
      setValue: {
        onSuccess: () => {
          toast.success('Operator updated successfully')
        },
        onError: (err) => {
          toast.error(err.messages?.join(', ') || 'Failed to update')
        }
      },
      onSuccess: (data) => {
        // Convert is_active to boolean for display
        data.is_active = Boolean(data.is_active)
      }
    })
  } else {
    // Create mode
    docResource.value = reactive({
      doc: {
        doctype: 'Operator',
        operator_name: '',
        employee_code: '',
        is_active: true
      },
      loading: false,
      setValue: {
        loading: false,
        submit: () => Promise.resolve()
      },
      reload: () => Promise.resolve()
    })
  }
}

initializeDoc()

// Watch for route changes
watch(docname, () => {
  initializeDoc()
})

// Validation
const validateForm = () => {
  if (!doc.value.doc.operator_name || doc.value.doc.operator_name.trim() === '') {
    toast.error('Operator Name is required')
    return false
  }
  return true
}

// Save handler
const handleSave = async () => {
  if (!validateForm()) {
    return
  }

  try {
    if (docname.value) {
      // Update existing document
      const dataToSave = {
        employee_code: doc.value.doc.employee_code ? doc.value.doc.employee_code.trim() : null,
        is_active: doc.value.doc.is_active ? 1 : 0
      }
      await doc.value.setValue.submit(dataToSave)
      await doc.value.reload()
    } else {
      // Create new document
      const dataToSave = {
        doctype: 'Operator',
        operator_name: doc.value.doc.operator_name.trim(),
        employee_code: doc.value.doc.employee_code ? doc.value.doc.employee_code.trim() : null,
        is_active: doc.value.doc.is_active ? 1 : 0
      }

      const insertResource = createResource({
        url: 'frappe.client.insert',
        makeParams: () => ({ doc: dataToSave })
      })

      const result = await insertResource.fetch()

      if (result) {
        toast.success('Operator created successfully')
        router.push(`/organization/operators/${result.name}`)
      }
    }
  } catch (err) {
    toast.error(err.messages?.join(', ') || err.message || 'Failed to save')
    console.error(err)
  }
}

// Navigation
const goBack = () => {
  router.push('/organization/operators')
}
</script>

<style scoped>
.operator-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* Ensure consistent white background for all form inputs */

</style>
