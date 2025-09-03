<template>
  <nav class="bg-white shadow-sm border-b border-gray-200 px-4 py-3 md:px-6 md:py-4 flex items-center justify-between">
    <div class="flex items-center">
      <img 
        src="/soundseal-logo.png" 
        alt="SoundSeal Logo" 
        class="h-10 cursor-pointer hover:opacity-80 transition-opacity duration-200"
        @click="navigateToHome"
      />
    </div>
    <div class="flex items-center gap-4">
      <button 
        @click="handleLogout" 
        class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 font-medium text-sm hover:bg-gray-50 hover:border-gray-400 active:bg-gray-100 transition-all duration-200 shadow-sm hover:shadow-md"
        title="Logout"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
        <span class="hidden sm:inline">Logout</span>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router"
import { session } from "../data/session"

const router = useRouter()

const navigateToHome = () => {
	router.push("/")
}

const handleLogout = async () => {
	try {
		await session.logout.submit()
		// Redirect to login page with redirect parameter
		window.location.href = "/login?redirect-to=/frontend"
	} catch (error) {
		console.error("Logout failed:", error)
		// Still redirect to login page even if logout fails
		window.location.href = "/login?redirect-to=/frontend"
	}
}
</script>