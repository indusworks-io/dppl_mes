import { createRouter, createWebHistory } from 'vue-router';
// import { session, userResource } from 'frappe-ui';
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


// router.beforeEach(async (to, from, next) => {
//   let isLoggedIn = session.isLoggedIn
//   try {
//     await userResource.promise
//   } catch (error) {
//     isLoggedIn = false;
//   }
//   if (!isLoggedIn) {
//     window.location.href = '/login?redirect-to=/Dashboard';
//   } else {
//     next();
//   }
// })


export default router;
