import { createRouter, createWebHistory } from 'vue-router';
import DashboardComponent from '../components/DashboardComponent.vue';
import FactoryFloorMap from '../components/FactoryFloorMap.vue';
import MachineDetails from '../components/MachineDetails.vue';

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardComponent
  },
  {
    path: '/map',
    name: 'FactoryFloorMap',
    component: FactoryFloorMap
  },
  {
    path: '/machines/:id',
    name: 'MachineDetails',
    component: MachineDetails,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
