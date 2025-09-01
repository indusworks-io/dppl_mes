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


# Machine Card Development Work:
We are now working on the Machine Card Component that loads/renders on the Dashboard Component i.e. DashboardComponent.vue using MachineCard.vue

## Requirements
1. Make the Machine Name slightly Larger
2. Show The Following Job Progress Metrics:
  - Job Name
  - Job Number
  - Target Quantity
  - Completed Quantity
3. if the is_active in machine is 0 then make the card color gray
4. if the run_rate_indicator is 1 then make the card color green else red
5. Stick with the image functionality & hyperlinking the card to machine details page
6. Similar to how we are updating tha map using socket in FactoryFloorMap.vue we need to update the cards using the realtime events.
7. If required move the socketlistner to a seperate js file... create a new folder called 'store' and put it there. Think a lot before doing it.

## Instructions:
  - Some of the functionality is already done
  - Read code in the file & make a to do list
  - Take confirmation on plan/to do list and then execute changes

## Files To Use/Modify
  - Home.vue -- Path: dppl_mes/frontend/src/pages/Home.vue
  - DashboardComponent.vue Path: dppl_mes/frontend/src/components/DashboardComponent.vue
  - MachineCard.vue Path: dppl_mes/frontend/src/components/MachineCard.vue
  - FactoryFloorMap.vue Path: dppl_mes/frontend/src/components/FactoryFloorMap.vue

## Bugs:
When the page loads from the first time and the socket is not triggered an update the card shows 'No Active Job'.
This is true for DashboardComponent.vue & FactoryFloorMap.vue.
Can we add a functionality that when the page/section loads first we update map & cards by calling get_job_metrics_internal_function and then let socket take care of the realtime updates.

In Machine Card, machines that are inactive i.e. is_ative == 0 we see Job Metrics as No Job Running. Ideally if the machine is inactive the user should just see it as Inactive

In FactoryFloorMap.vue also we need to add logic/functionality similar to Machine Card. If a Machine is Inactive then the Overlay should show Inactive to the user and not show Job Metrics.