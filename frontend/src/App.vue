<template>
  <div class="flex h-screen overflow-hidden bg-gray-50">
    <!-- Sidebar -->
    <Sidebar
      v-model:collapsed="sidebarCollapsed"
      :header="sidebarHeader"
      :sections="sidebarSections"
      class="flex-shrink-0"
    >
      <template #header-logo>
        <img
          :src="logoUrl"
          alt="Company Logo"
          class="h-8 w-auto object-contain"
          @error="handleLogoError"
        />
      </template>
    </Sidebar>

    <!-- Main Content Area -->
    <main class="flex-1 overflow-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { session } from "./data/session"
import { userDetailsResource, userResource } from "./data/user"

import LucideBarChart3 from "~icons/lucide/bar-chart-3"
import LucideBell from "~icons/lucide/bell"
import LucideBriefcase from "~icons/lucide/briefcase"
import LucideBuilding2 from "~icons/lucide/building-2"
import LucideCalendar from "~icons/lucide/calendar"
import LucideClipboardList from "~icons/lucide/clipboard-list"
import LucideClock from "~icons/lucide/clock"
import LucideHelpCircle from "~icons/lucide/help-circle"
// Import Lucide icons
import LucideHome from "~icons/lucide/home"
import LucideLogOut from "~icons/lucide/log-out"
import LucideMap from "~icons/lucide/map"
import LucidePackage from "~icons/lucide/package"
import LucideSettings from "~icons/lucide/settings"
import LucideUsers from "~icons/lucide/users"

const router = useRouter()
const sidebarCollapsed = ref(false)

// Sidebar header configuration
const sidebarHeader = computed(() => ({
	title: "Soundseal MES",
	subtitle: userDisplayName.value,
	menuItems: [
		{
			label: "Logout",
			icon: LucideLogOut,
			onClick: handleLogout,
		},
	],
}))

// User display name
const userDisplayName = computed(() => {
	if (userDetailsResource.data) {
		return (
			userDetailsResource.data.full_name ||
			`${userDetailsResource.data.first_name || ""} ${userDetailsResource.data.last_name || ""}`.trim() ||
			userDetailsResource.data.email
		)
	}
	return "User"
})

// Logo URL
const logoUrl = "/soundseal-favicon.png"

// Sidebar sections configuration
const sidebarSections = computed(() => [
	{
		label: "",
		items: [
			{
				label: "Home",
				icon: LucideHome,
				to: "/",
				isActive: router.currentRoute.value.path === "/",
			},
			{
				label: "Notifications",
				icon: LucideBell,
				to: "/notifications",
				isActive: router.currentRoute.value.path === "/notifications",
			},
			{
				label: "Reports",
				icon: LucideBarChart3,
				to: "/reports",
				isActive: router.currentRoute.value.path === "/reports",
			},
		],
	},
	{
		label: "Production",
		collapsible: true,
		items: [
			{
				label: "Shift Plans",
				icon: LucideCalendar,
				to: "/production/shift-plans",
				isActive: router.currentRoute.value.path === "/production/shift-plans",
			},
			{
				label: "Job Cards",
				icon: LucideClipboardList,
				to: "/production/job-cards",
				isActive: router.currentRoute.value.path === "/production/job-cards",
			},
			{
				label: "Output Logs",
				icon: LucidePackage,
				to: "/production/output-logs",
				isActive: router.currentRoute.value.path === "/production/output-logs",
			},
			{
				label: "Downtime Logs",
				icon: LucideClock,
				to: "/production/downtime-logs",
				isActive:
					router.currentRoute.value.path === "/production/downtime-logs",
			},
			{
				label: "Jobs",
				icon: LucideBriefcase,
				to: "/production/jobs",
				isActive: router.currentRoute.value.path === "/production/job-master",
			},
			{
				label: "Downtime Reasons",
				icon: LucideHelpCircle,
				to: "/production/downtime-reasons",
				isActive:
					router.currentRoute.value.path === "/production/downtime-reasons",
			},
		],
	},
	{
		label: "Organization",
		collapsible: true,
		items: [
			{
				label: "Factories",
				icon: LucideBuilding2,
				to: "/organization/factories",
				isActive: router.currentRoute.value.path === "/organization/factories",
			},
			{
				label: "Areas",
				icon: LucideMap,
				to: "/organization/areas",
				isActive: router.currentRoute.value.path === "/organization/areas",
			},
			{
				label: "Machines",
				icon: LucideSettings,
				to: "/organization/machines",
				isActive: router.currentRoute.value.path === "/organization/machines",
			},
			{
				label: "Operators",
				icon: LucideUsers,
				to: "/organization/operators",
				isActive: router.currentRoute.value.path === "/organization/operators",
			},
		],
	},
])

// Logout handler
const handleLogout = async () => {
	try {
		await session.logout.submit()
		window.location.href = "/login?redirect-to=/frontend"
	} catch (error) {
		console.error("Logout failed:", error)
		window.location.href = "/login?redirect-to=/frontend"
	}
}

// Handle logo error
const handleLogoError = () => {
	console.warn("Failed to load company logo, falling back to default")
}

// Initialize data on mount
onMounted(async () => {
	try {
		// Ensure user is loaded (should be from auto: true)
		if (!userResource.data) {
			await userResource.reload()
		}

		// Fetch user details if user is available
		if (userResource.data && userDetailsResource.reload) {
			await userDetailsResource.reload()
		}
	} catch (error) {
		console.error("Failed to initialize app data:", error)
	}
})
</script>
