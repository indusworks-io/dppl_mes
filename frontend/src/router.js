import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("@/pages/Home.vue"),
	},
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
	let isLoggedIn = session.isLoggedIn;
	console.log('isLoggedIn Init')
	try {
		await userResource.fetch();
	} catch (error) {
		isLoggedIn = false;
	}
	console.log(isLoggedIn)

	if (to.name === "Login" && isLoggedIn) {
		next({ name: "Home" });
	} else if (to.name !== "Login" && !isLoggedIn) {
		window.location.href = "/login?redirect-to=/frontend"
	} else {
		next();
	}
});

export default router
