<template>
  <div class="shift-plan-detail">
    <DetailView
      doctype="Shift Plan"
      :name="shiftPlanName"
      :related="['Job Card']"
      @saved="handleSaved"
      @deleted="handleDeleted"
      @cancel="handleCancel"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DetailView from '../../components/DetailView.vue'

const route = useRoute()
const router = useRouter()

// Get shift plan name from route params (null for new records)
const shiftPlanName = computed(() => {
  return route.params.name === 'new' ? null : route.params.name
})

// Handle saved event
const handleSaved = (data) => {
  console.log('Shift Plan saved:', data)

  // If it was a new record, update the URL to the saved record
  if (!route.params.name || route.params.name === 'new') {
    router.replace(`/production/shift-plans/${data.name}`)
  }
}

// Handle deleted event
const handleDeleted = () => {
  console.log('Shift Plan deleted')

  // Navigate back to list
  router.push('/production/shift-plans')
}

// Handle cancel event
const handleCancel = () => {
  // Navigate back to list
  router.push('/production/shift-plans')
}
</script>

<style scoped>
.shift-plan-detail {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>
