# Dashboard Component Development Work
We are now working on the Dashboard Component that loads/renders on the Home Page i.e. Home.vue

## Expected Outcomes:
1. Fetch areas from backend using areaResource
2. Based on the selectedFactory variable Create a list of FactoryAreas that are in that Factory & Order Them based on sequence_number that we get from areaResource
3. Render them as individual sections in ascending order of sequence_number
4. In Each Area that we are rendering/showing on the page we need to append/insert a machine card for each machine in that area
5. We will get machine information from machineResource resource
6. The machine needs to be in ascending order based on sequence_number in machineResource
7. The Page & all components need to be responsive

## Instructions:
  - Some of the functionality is already done
  - Read code in the file & make a to do list
  - Take confirmation on plan/to do list and then execute changes

## Files To Use/Modify
  - Home.vue -- Path: dppl_mes/frontend/src/pages/Home.vue
  - DashboardComponent.vue Path: dppl_mes/frontend/src/components/DashboardComponent.vue
  - MachineCard.vue Path: dppl_mes/frontend/src/components/MachineCard.vue

Use playwright MCP view page, evaluate HTML, CSS & Javascript. Use URL: http://dppl.localhost:8080/frontend/