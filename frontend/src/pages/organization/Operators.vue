<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Operators</h1>
      <p class="text-gray-600">Manage production operators and their assignments</p>
    </div>

    <div v-if="operators.loading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p class="text-gray-600">Loading operators...</p>
      </div>
    </div>

    <div v-else-if="operators.error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-800">Error loading operators: {{ operators.error }}</p>
    </div>

    <div v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Operators</p>
              <p class="text-2xl font-semibold text-gray-900">{{ operators.data?.length || 0 }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Active</p>
              <p class="text-2xl font-semibold text-gray-900">{{ activeOperatorsCount }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V8a2 2 0 012-2V6"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Skill Levels</p>
              <p class="text-2xl font-semibold text-gray-900">{{ uniqueSkillLevels }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Departments</p>
              <p class="text-2xl font-semibold text-gray-900">{{ uniqueDepartments }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Operators Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div
          v-for="operator in operators.data"
          :key="operator.name"
          class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
        >
          <div class="p-6">
            <div class="flex items-center mb-4">
              <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <div class="ml-3 flex-1 min-w-0">
                <h3 class="text-sm font-semibold text-gray-900 truncate">
                  {{ operator.operator_name || operator.name }}
                </h3>
                <p class="text-xs text-gray-500 truncate">{{ operator.name }}</p>
              </div>
              <span :class="operator.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                    class="inline-flex px-2 py-1 text-xs font-semibold rounded-full flex-shrink-0">
                {{ operator.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>

            <div class="space-y-2 text-xs text-gray-600">
              <div class="flex items-center" v-if="operator.employee_id">
                <svg class="w-3 h-3 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                </svg>
                <span class="truncate">ID: {{ operator.employee_id }}</span>
              </div>

              <div class="flex items-center" v-if="operator.department">
                <svg class="w-3 h-3 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                </svg>
                <span class="truncate">{{ operator.department }}</span>
              </div>

              <div class="flex items-center" v-if="operator.skill_level">
                <svg class="w-3 h-3 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
                <span :class="getSkillLevelClass(operator.skill_level)"
                      class="inline-flex px-1 py-0.5 text-xs font-medium rounded">
                  {{ operator.skill_level }}
                </span>
              </div>

              <div class="flex items-center" v-if="operator.phone">
                <svg class="w-3 h-3 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                </svg>
                <span class="truncate">{{ operator.phone }}</span>
              </div>

              <div class="flex items-center" v-if="operator.email">
                <svg class="w-3 h-3 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
                <span class="truncate">{{ operator.email }}</span>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-gray-100">
              <div class="flex items-center justify-between text-xs text-gray-500">
                <span>Joined:</span>
                <span>{{ formatDate(operator.creation) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!operators.data || operators.data.length === 0" class="col-span-full">
          <div class="text-center py-12">
            <svg class="mx-auto w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No operators found</h3>
            <p class="mt-1 text-sm text-gray-500">Production operators will appear here when registered.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createListResource } from "frappe-ui"
import { computed } from "vue"

const operators = createListResource({
  doctype: "Operator",
  fields: [
    "name",
    "operator_name",
    "employee_id",
    "department",
    "skill_level",
    "phone",
    "email",
    "is_active",
    "creation"
  ],
  orderBy: "creation desc",
  pageLength: 100,
  auto: true,
})

const activeOperatorsCount = computed(() => {
  if (!operators.data) return 0
  return operators.data.filter(operator => operator.is_active).length
})

const uniqueSkillLevels = computed(() => {
  if (!operators.data) return 0
  const skillLevels = [...new Set(operators.data.filter(o => o.skill_level).map(o => o.skill_level))]
  return skillLevels.length
})

const uniqueDepartments = computed(() => {
  if (!operators.data) return 0
  const departments = [...new Set(operators.data.filter(o => o.department).map(o => o.department))]
  return departments.length
})

const formatDate = (dateString) => {
  if (!dateString) return "N/A"
  try {
    return new Date(dateString).toLocaleDateString("en-GB")
  } catch {
    return "Invalid Date"
  }
}

const getSkillLevelClass = (skillLevel) => {
  if (!skillLevel) return "bg-gray-100 text-gray-800"
  const level = skillLevel.toLowerCase()

  if (level.includes('expert') || level.includes('senior')) {
    return "bg-green-100 text-green-800"
  } else if (level.includes('intermediate') || level.includes('mid')) {
    return "bg-blue-100 text-blue-800"
  } else if (level.includes('junior') || level.includes('beginner')) {
    return "bg-yellow-100 text-yellow-800"
  }
  return "bg-gray-100 text-gray-800"
}
</script>