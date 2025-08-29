<template>
  <div class="factory-filter">
    <label :for="filterId">{{ label }}</label>
    <div class="select-wrapper">
      <select :id="filterId" :name="filterId" v-model="selectedValue" @change="handleChange">
        <option v-if="placeholder" value="">{{ placeholder }}</option>
        <option v-for="option in options" :key="option.value" :value="option.value">
          {{ option.text }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps, ref, watch } from "vue"

const props = defineProps({
	id: { type: String, default: "factory-filter" },
	label: { type: String, default: "Factory" },
	options: { type: Array, required: true },
	placeholder: { type: String, default: "Select Factory" },
	modelValue: { type: String, default: "" },
})

const emit = defineEmits(["update:modelValue", "factory-selected"])

const filterId = ref(props.id)
const selectedValue = ref(props.modelValue)

watch(
	() => props.modelValue,
	(newValue) => {
		selectedValue.value = newValue
	},
)

const handleChange = () => {
	emit("update:modelValue", selectedValue.value)
	emit("factory-selected", selectedValue.value)
}
</script>

<style scoped>
.factory-filter {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.factory-filter label {
  font-weight: 600;
  font-size: 1rem;
  color: #343a40;
  white-space: nowrap;
}

.select-wrapper {
  position: relative;
  display: inline-block;
  min-width: 200px;
}

.select-wrapper select {
  width: 100%;
  padding: 10px 36px 10px 14px;
  border-radius: 6px;
  border: 1px solid #ced4da;
  background-color: #fff;
  font-size: 1rem;
  font-weight: 500;
  color: #212529;
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  appearance: none;
}

.select-wrapper::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 12px;
  width: 12px;
  height: 12px;
  pointer-events: none;
  background: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' viewBox='0 0 16 16'%3e%3cpath d='M2 5l6 6 6-6'/%3e%3c/svg%3e")
    no-repeat center;
  transform: translateY(-50%);
}

.select-wrapper select:hover {
  border-color: #adb5bd;
}

.select-wrapper select:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>