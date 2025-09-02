<template>
  <nav class="top-bar">
    <div class="navbar-left">
      <img 
        src="/soundseal-logo.png" 
        alt="SoundSeal Logo" 
        class="brand-logo"
        @click="navigateToHome"
      />
    </div>
    <div class="navbar-right">
      <button @click="handleLogout" class="logout-button" title="Logout">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
        <span class="logout-text">Logout</span>
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

<style scoped>
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 32px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.navbar-left {
  display: flex;
  align-items: center;
}

.navbar-right {
  display: flex;
  align-items: center;
}

.brand-logo {
  height: 40px;
  width: auto;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
  object-fit: contain;
}

.brand-logo:hover {
  transform: scale(1.05);
  opacity: 0.9;
}

.logout-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  color: #475569;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.logout-button:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  color: #334155;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logout-button:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.logout-text {
  font-size: 14px;
}

@media (max-width: 640px) {
  .logout-text {
    display: none;
  }
  
  .logout-button {
    padding: 8px 12px;
  }
}
</style>