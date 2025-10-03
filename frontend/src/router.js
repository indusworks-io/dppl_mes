import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("@/pages/Home.vue"),
	},

	// System pages
	{
		path: "/notifications",
		name: "Notifications",
		component: () => import("@/pages/Notifications.vue"),
	},
	{
		path: "/reports",
		name: "Reports",
		component: () => import("@/pages/Reports.vue"),
	},

	// Production pages
	{
		path: "/production/shift-plans",
		name: "ShiftPlans",
		component: () => import("@/pages/production/ShiftPlans.vue"),
	},
	{
		path: "/production/shift-plans/:name",
		name: "ShiftPlanDetail",
		component: () => import("@/pages/production/ShiftPlanDetail.vue"),
	},
	{
		path: "/production/job-cards",
		name: "JobCards",
		component: () => import("@/pages/production/JobCards.vue"),
	},
	{
		path: "/production/output-logs",
		name: "OutputLogs",
		component: () => import("@/pages/production/OutputLogs.vue"),
	},
	{
		path: "/production/downtime-logs",
		name: "DowntimeLogs",
		component: () => import("@/pages/production/DowntimeLogs.vue"),
	},
	{
		path: "/production/job-master",
		name: "JobMaster",
		component: () => import("@/pages/production/JobMaster.vue"),
	},
	{
		path: "/production/downtime-reasons",
		name: "DowntimeReasons",
		component: () => import("@/pages/production/DowntimeReasons.vue"),
	},

	// Organization pages
	{
		path: "/organization/factories",
		name: "Factories",
		component: () => import("@/pages/organization/Factories.vue"),
	},
	{
		path: "/organization/areas",
		name: "Areas",
		component: () => import("@/pages/organization/Areas.vue"),
	},
	{
		path: "/organization/machines",
		name: "Machines",
		component: () => import("@/pages/organization/Machines.vue"),
	},
	{
		path: "/organization/operators",
		name: "Operators",
		component: () => import("@/pages/organization/Operators.vue"),
	},

	// Detail pages (existing)
	{
		path: "/machine/:id",
		name: "Machine",
		component: () => import("@/pages/Machine.vue"),
	},
	{
		path: "/job-card/:id",
		name: "JobCard",
		component: () => import("@/pages/JobCard.vue"),
	},
	{
		path: "/downtime-log/:id",
		name: "DowntimeLog",
		component: () => import("@/pages/DowntimeLog.vue"),
	},
]

const router = createRouter({
	history: createWebHistory("/frontend"),
	routes,
})

router.beforeEach(async (to, from, next) => {
	let isLoggedIn = session.isLoggedIn
	console.log("isLoggedIn Init")
	try {
		await userResource.fetch()
	} catch (error) {
		isLoggedIn = false
	}
	console.log(isLoggedIn)

	if (to.name === "Login" && isLoggedIn) {
		next({ name: "Home" })
	} else if (to.name !== "Login" && !isLoggedIn) {
		window.location.href = "/login?redirect-to=/frontend"
	} else {
		next()
	}
})

export default router
