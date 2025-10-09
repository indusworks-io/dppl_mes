<template>
  <div class="job-page p-6">
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
              title="Back to Jobs"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ docname ? doc.doc.job_name || doc.doc.name : 'New Job' }}
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
          <!-- Job Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Job Name <span class="text-red-500">*</span>
            </label>
            <Input
              v-model="doc.doc.job_name"
              type="text"
              placeholder="Enter job name"
              :disabled="!!docname"
            />
            <p v-if="docname" class="mt-1 text-xs text-gray-500">Job name cannot be changed after creation</p>
          </div>

          <!-- Job Number -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Job Number <span class="text-red-500">*</span>
            </label>
            <Input
              v-model="doc.doc.job_number"
              type="text"
              placeholder="Enter job number"
            />
          </div>

          <!-- Complexity Level -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Complexity Level <span class="text-red-500">*</span>
            </label>
            <Select
              v-model="doc.doc.complexity_level"
              :options="['1', '2', '3', '4', '5']"
              placeholder="Select complexity level"
            />
            <p class="mt-1 text-xs text-gray-500">1 = Lowest complexity, 5 = Highest complexity</p>
          </div>

          <!-- Ideal Run Rate -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Ideal Run Rate <span class="text-red-500">*</span>
            </label>
            <Input
              v-model="doc.doc.ideal_run_rate"
              type="number"
              placeholder="Enter ideal run rate"
              min="0"
            />
            <p class="mt-1 text-xs text-gray-500">Output per minute</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createDocumentResource, createResource, Input, Select, toast } from 'frappe-ui'
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
      doctype: 'Job',
      name: docname.value,
      auto: true,
      setValue: {
        onSuccess: () => {
          toast.success('Job updated successfully')
        },
        onError: (err) => {
          toast.error(err.messages?.join(', ') || 'Failed to update')
        }
      }
    })
  } else {
    // Create mode
    docResource.value = reactive({
      doc: {
        doctype: 'Job',
        job_name: '',
        job_number: '',
        complexity_level: '',
        ideal_run_rate: null
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
  if (!doc.value.doc.job_name || doc.value.doc.job_name.trim() === '') {
    toast.error('Job Name is required')
    return false
  }
  if (!doc.value.doc.job_number || doc.value.doc.job_number.trim() === '') {
    toast.error('Job Number is required')
    return false
  }
  if (!doc.value.doc.complexity_level) {
    toast.error('Complexity Level is required')
    return false
  }
  if (!doc.value.doc.ideal_run_rate || doc.value.doc.ideal_run_rate <= 0) {
    toast.error('Ideal Run Rate is required and must be greater than 0')
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
        job_number: doc.value.doc.job_number,
        complexity_level: doc.value.doc.complexity_level,
        ideal_run_rate: doc.value.doc.ideal_run_rate
      }
      await doc.value.setValue.submit(dataToSave)
      await doc.value.reload()
    } else {
      // Create new document
      const dataToSave = {
        doctype: 'Job',
        job_name: doc.value.doc.job_name.trim(),
        job_number: doc.value.doc.job_number.trim(),
        complexity_level: doc.value.doc.complexity_level,
        ideal_run_rate: Number.parseInt(doc.value.doc.ideal_run_rate)
      }

      const insertResource = createResource({
        url: 'frappe.client.insert',
        makeParams: () => ({ doc: dataToSave })
      })

      const result = await insertResource.fetch()

      if (result) {
        toast.success('Job created successfully')
        router.push(`/production/jobs/${result.name}`)
      }
    }
  } catch (err) {
    toast.error(err.messages?.join(', ') || err.message || 'Failed to save')
    console.error(err)
  }
}

// Navigation
const goBack = () => {
  router.push('/production/jobs')
}
</script>

<style scoped>
.job-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* Ensure consistent white background for all form inputs */

</style>
