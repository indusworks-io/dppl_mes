<template>
  <div class="machine-card" @click="handleClick">
    <img :src="machineImage" alt="Machine Photo" class="machine-photo">
    <div class="machine-details">
      <p><strong>Machine:</strong> {{ machine.name }}</p>
      <p><strong>OEM Code:</strong> {{ machine.oem_code || 'N/A' }}</p>
      <p>
        <strong>Status:</strong> {{ machine.status }}
        <FeatherIcon 
          :name="machine.status === 'running' ? 'play-circle' : 'stop-circle'" 
          :size="16" 
          class="status-icon"
        />
      </p>
      <p v-if="machine.jobName"><strong>Job:</strong> {{ machine.jobName }}</p>
      <p v-if="machine.actualOutput !== undefined && machine.targetOutput !== undefined">
        <strong>Output:</strong> {{ machine.actualOutput }} / {{ machine.targetOutput }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import { FeatherIcon } from 'frappe-ui';
import machineImage from '../assets/image.png';

const props = defineProps({
  machine: {
    type: Object,
    required: true,
    validator: (machine) => {
      return (
        typeof machine.id === 'string' &&
        typeof machine.name === 'string' &&
        typeof machine.status === 'string' &&
        typeof machine.factory === 'string' &&
        typeof machine.area === 'string'
      );
    },
  },
});

const emit = defineEmits(['card-clicked']);

const handleClick = () => {
  emit('card-clicked', props.machine.id);
};
</script>

<style scoped>
.machine-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin: 8px;
  cursor: pointer;
  transition: transform 0.2s;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.machine-card:hover {
  transform: translateY(-5px);
}

.machine-photo {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 12px;
}

.machine-details p {
  margin: 4px 0;
  display: flex;
  align-items: center;
}

.status-icon {
  margin-left: 8px;
}
</style>