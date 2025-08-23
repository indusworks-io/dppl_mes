<!-- src/components/HomePageControls.vue -->
<template>
    <div class="controls-bar">
      <button @click="$emit('toggle-view')" class="toggle-button">
        Switch to {{ isFloorMapView ? 'Dashboard View' : 'Map View' }}
      </button>
    </div>
</template>

<script setup>

const props = defineProps({
  isFloorMapView: Boolean,
  isMachineDetailsView: Boolean,
});

const emit = defineEmits(['go-back', 'toggle-view', 'filter-selected']);

</script>

<style scoped>
/* Primary Bar */
.controls-bar {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  padding: 10px 20px;
  background: #f7f8fa;
  border-radius: 0px;
  box-shadow: 0 2px 16px rgba(60, 72, 88, 0.08);
  margin: 0px 0;
  position: relative;
  z-index: 10;
  gap: 10px;
}

/* Toggle Button Style */
.toggle-button {
  flex-shrink: 1;
}

.controls-bar button {
  padding: 10px 20px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.25px;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
  position: relative;
  overflow: hidden;
}

.controls-bar button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.4s;
}

.controls-bar button:hover::before {
  left: 100%;
}

.controls-bar button:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.controls-bar button:active {
  transform: translateY(0px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

/* Desktop: filters align to the right */
@media (min-width: 769px) {
  .filters {
    flex-grow: 1;
    justify-content: flex-end;
  }
}

/* Mobile: filters start from left when wrapped */
@media (max-width: 768px) {
  .controls-bar {
    flex-direction: column;
    align-items: stretch;
  }
}

</style>