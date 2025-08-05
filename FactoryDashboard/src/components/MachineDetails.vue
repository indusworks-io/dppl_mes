<template>
  <div class="machine-details-container">
    <h2 class="page-title">Machine Details</h2>

    <!-- Top Section -->
    <div class="top-section">
      <img :src="machineImage" alt="Machine Image" class="machine-image" />
      <div class="info-panel">
        <p><strong>ID:</strong> {{ machine?.id }}</p>
        <p><strong>Status:</strong> <span :class="['status', machine?.status]">{{ machine?.status }}</span></p>
        <p><strong>Job:</strong> {{ machine?.jobName }}</p>
        <p><strong>Actual Output:</strong> {{ machine?.actualOutput }}</p>
        <p><strong>Target Output:</strong> {{ machine?.targetOutput }}</p>
      </div>
    </div>

    <!-- Table Section -->
    <div class="table-section">
      <h3 class="table-title" >Downtime Reasons</h3>
      <table style="">
        <thead>
          <tr>
            <th>Date</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Duration</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(entry, index) in visibleTableData" :key="index">
            <td>{{ entry.date }}</td>
            <td>{{ entry.startTime }}</td>
            <td>{{ entry.endTime }}</td>
            <td>{{ entry.duration }}</td>
            <td>{{ entry.status }}</td>
            <td><button class="action-btn">Update Reason</button></td>
          </tr>
          <tr class="load-more" v-if="visibleCount < tableData.length">
            <td colspan="6">
              <button class="load-more-btn" @click="loadMore">Load More</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import machineImage from '../assets/image.png';

const route = useRoute();
const machine = ref(null);

const fetchMachineDetails = async (machineId) => {
  try {
    const dummyMachines = [
      { id: 1, name: 'Machine 1', area: 'Area1', status: 'running', jobName: 'Job A', actualOutput: 100, targetOutput: 120, photo: 'https://via.placeholder.com/150' },
      { id: 2, name: 'Machine 2', area: 'Area1', status: 'stopped', jobName: 'Job B', actualOutput: 80, targetOutput: 100, photo: 'https://via.placeholder.com/150' },
      { id: 3, name: 'Machine 3', area: 'Area2', status: 'running', jobName: 'Job C', actualOutput: 150, targetOutput: 150, photo: 'https://via.placeholder.com/150' },
      { id: 4, name: 'Machine 4', area: 'Area2', status: 'maintenance', jobName: 'Job D', actualOutput: 0, targetOutput: 100, photo: 'https://via.placeholder.com/150' },
      { id: 5, name: 'Machine 5', area: 'Area3', status: 'running', jobName: 'Job E', actualOutput: 200, targetOutput: 180, photo: 'https://via.placeholder.com/150' },
    ];
    machine.value = dummyMachines.find(m => m.id === parseInt(machineId));
  } catch (error) {
    console.error('Error fetching machine details:', error);
  }
};

onMounted(() => {
  const machineId = route.params.id;
  if (machineId) {
    fetchMachineDetails(machineId);
  }
});

const tableData = ref([
  { date: '2025-08-01', startTime: '08:00', endTime: '10:00', duration: '2h', status: 'Running' },
  { date: '2025-08-01', startTime: '10:30', endTime: '11:00', duration: '30m', status: 'Stopped' },
  { date: '2025-08-02', startTime: '09:00', endTime: '12:00', duration: '3h', status: 'Running' },
  { date: '2025-08-03', startTime: '07:45', endTime: '08:30', duration: '45m', status: 'Maintenance' },
  { date: '2025-08-04', startTime: '13:00', endTime: '15:30', duration: '2.5h', status: 'Running' },
  { date: '2025-08-01', startTime: '08:00', endTime: '10:00', duration: '2h', status: 'Running' },
  { date: '2025-08-01', startTime: '10:30', endTime: '11:00', duration: '30m', status: 'Stopped' },
  { date: '2025-08-02', startTime: '09:00', endTime: '12:00', duration: '3h', status: 'Running' },
  { date: '2025-08-03', startTime: '07:45', endTime: '08:30', duration: '45m', status: 'Maintenance' },
  { date: '2025-08-04', startTime: '13:00', endTime: '15:30', duration: '2.5h', status: 'Running' },
]);


const visibleCount = ref(4);

const visibleTableData = computed(() => {
  return tableData.value.slice(0, visibleCount.value);
});

function loadMore() {
  visibleCount.value += 4;
}

</script>

<style scoped>
.machine-details-container {
  padding: 24px;
  font-family: 'Segoe UI', sans-serif;

    max-height: 100vh;        /* Full viewport height */
  overflow-y: auto;         /* Enable vertical scroll */
  box-sizing: border-box;   /* Include padding in height */
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #2c3e50;
}

.top-section {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.machine-image {
  width: 300px;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.info-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  flex-grow: 1;
}

.status {
  padding: 4px 10px;
  border-radius: 8px;
  font-weight: bold;
  text-transform: capitalize;
}

.status.running {
  background-color: #e0ffe5;
  color: #2ecc71;
}
.status.stopped {
  background-color: #ffe0e0;
  color: #e74c3c;
}
.status.maintenance {
  background-color: #fff6e0;
  color: #f39c12;
}

.table-section {
  margin-top: 30px;
    overflow-y: auto;

}

.table-title {
  margin-bottom: 12px;
  font-size: 18px;
  font-weight: 500;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

thead {
  background-color: #f0f0f0;
}

th, td {
  padding: 12px 16px;
  text-align: left;
}

tbody tr:not(.load-more):hover {
  background-color: #f9f9f9;
}

.load-more {
  text-align: center;
}

.load-more-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.load-more-btn:hover {
  background-color: #2980b9;
}

.action-btn {
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}

.action-btn:hover {
  background-color: #27ae60;
}
</style>
