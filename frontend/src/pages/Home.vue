<template>
  <div id="app">
    <NavBar />
    <HomePageControls
      :factory-options="factoryOptions"
      :selected-factory="selectedFactory"
      :is-floor-map-view="isFloorMapView"
      @toggle-view="toggleView"
      @filter-selected="handleFactorySelection"
    />

    <div id="HomePageView">
      <DashboardComponent
        v-if="!isFloorMapView"
        :areas="areas"
        :machines="machines"
      />
      <FactoryFloorMap
        v-else
        :selected-factory="selectedFactory"
        :factory-data="selectedFactoryData"
        :machines="machines"
      />
    </div>
  </div>
</template>

<script setup>
import { createListResource, createResource } from "frappe-ui"
import { computed, onMounted, onUnmounted, ref } from "vue"
import DashboardComponent from "../components/DashboardComponent.vue"
import FactoryFloorMap from "../components/FactoryFloorMap.vue"
import HomePageControls from "../components/HomePageControls.vue"
import NavBar from "../components/NavBar.vue"
import { initSocket } from "../socket.js"

const isFloorMapView = ref(false)
const factoryOptions = ref([])
const selectedFactory = ref("")
const selectedFactoryData = ref(null)
const areas = ref([])
const machines = ref([])
const socket = ref(null)

// Toggle between views
function toggleView() {
	isFloorMapView.value = !isFloorMapView.value
}

// Handle factory selection
function handleFactorySelection(factoryName) {
	selectedFactory.value = factoryName
	selectedFactoryData.value =
		factoryOptions.value.find((f) => f.value === factoryName) || null
}

// Fetch factories
const factoryResource = createListResource({
	doctype: "Factory",
	fields: ["name", "factory_name", "floor_plan"],
	filters: { is_active: 1 },
	auto: true,
	onSuccess(data) {
		factoryOptions.value = data.map((f) => ({
			value: f.name,
			text: f.factory_name,
			floor_plan: f.floor_plan,
		}))
		fetchDefaultFactory()
	},
})

// Fetch default factory
function fetchDefaultFactory() {
	createResource({
		url: "frappe.client.get",
		params: { doctype: "Organization Settings", name: "Organization Settings" },
		auto: true,
		onSuccess(res) {
			if (res && res.default_factory) {
				selectedFactory.value = res.default_factory
				selectedFactoryData.value =
					factoryOptions.value.find((f) => f.value === res.default_factory) ||
					null
			}
		},
	})
}

// Fetch areas
const areaResource = createListResource({
	doctype: "Area",
	fields: ["name", "area_name", "factory", "sequence_number"],
	auto: true,
	onSuccess(data) {
		areas.value = data
	},
})

// Fetch machines
const machineResource = createListResource({
	doctype: "Machine",
	fields: [
		"name",
		"machine_name",
		"is_active",
		"area",
		"sequence_number",
		"machine_image",
	],
	auto: true,
	pageLength: 2000,
	onSuccess(data) {
		machines.value = data
	},
})

const initializeView = () => {
	isFloorMapView.value = window.innerWidth > 1024
}

onMounted(() => {
	initializeView()
	window.addEventListener("resize", initializeView)

	// Initialize socket connection
	socket.value = initSocket()

	factoryResource.reload()
	areaResource.reload()
	machineResource.reload()
})

onUnmounted(() => {
	window.removeEventListener("resize", initializeView)

	// Clean up socket connection if needed
	if (socket.value) {
		socket.value.disconnect()
	}
})
</script>
