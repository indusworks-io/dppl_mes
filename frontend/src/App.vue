<template>
  <div>
    <!-- Only render router-view after session is validated -->
    <router-view v-if="sessionReady" />
    <!-- Loading state while session is being checked -->
    <div v-else class="flex items-center justify-center h-screen">
      <div class="text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
        <p class="mt-2 text-gray-600">Authenticating...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { provide, ref, onMounted } from 'vue'
import { session } from './data/session'
import { userResource } from './data/user'

const sessionReady = ref(false)

// Provide session globally for components that want to use inject
provide('session', session)

onMounted(async () => {
  try {
    // Wait for user resource to load/validate
    await userResource.promise
    sessionReady.value = true
  } catch (error) {
    // Session invalid, let router guard handle the redirect
    console.log('Session validation failed, router will handle redirect')
    sessionReady.value = false
  }
})
</script>
