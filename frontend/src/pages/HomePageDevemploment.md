# Homepage Development

## Instructions:
    - Following is the expected outcome for the Homepage Functionality.
    - Some of the functionality is already done
    - Read code in the file before making changes

## Files To Use/Modify
    - Home.vue -- Path: dppl_mes/frontend/src/pages/Home.vue
    - NavBar.vue -- Path: dppl_mes/frontend/src/components/NavBar.vue
    - HomePageControls.vue -- Path: dppl_mes/frontend/src/components/HomePageControls.vue
    - FactoryFloorMap.vue -- Path: dppl_mes/frontend/src/components/FactoryFloorMap.vue
    - DashboardComponent.vue -- Path: dppl_mes/frontend/src/components/DashboardComponent.vue
    - MachineCard.vue -- Path: dppl_mes/frontend/src/components/MachineCard.vue
    - FactoryFilter.vue -- Path: dppl_mes/frontend/src/components/FactoryFilter.vue
    - Machine.vue -- Path: dppl_mes/frontend/src/pages/Machine.vue
    - router.js -- Path: dppl_mes/frontend/src/router.js
    - api.py -- Path: dppl_mes/dppl_mes/api.py

## Expected Outcomes:
    1. Have following components:
        - Navbar
        - Homepage
        - Homepage Controls Bar
            - Factory Filter
            - Dashboard Switcher
        - Homepage Section

    2. Fetch & Update Factory List:
        - Fetch Factory List From 'Factory' DocType from the backend with following params:
            - Filter: is_active == 1
            - Fields: name, factory_name, floor_plan
        - Append the name in Factory Filter
        - Fetch Default Factory from Organization Settings & Select/Update in the Factory List

    3. Fetch & Update Area List:
        - Fetch All Areas From Area DocType with following params:
            - Fields: name, area_name, factory, sequence_number

    4. Fetch & Update Machine List:
        - Fetch All Machines From Machine DocType For All Factories In The Factory List With Following Params
            - Fields: name, machine_name, is_active, area, sequence_number, machine_image

    5. Build/Update Factory Floor Map:
        - In FactoryFloorMap.vue file render machine_image SVG
        - Make The SVG take 100% of the View Port Width while having some padding on all sides
        - The SVG path of each machine where the id of the path is same as name of Machine. example:
            In SVG: <path id="XL-D" d="M29 21V79H11V21H29Z" fill="#808080" stroke="black" stroke-width="2"/>
            In Backend: Machine Name is XL-D
        - Connect the path in the SVG with the machine from backend
        - If for a path there is not machine found then fill that path with gray color
        - In api.py there is a realtime event called job_metrics_update under create_telemetry(). Use that event to update te SVG as following:
            - if run_rate_indicator == 1 then green else red
        - If a user clicks on the machine path open a overlay/popup to show:
            - Job Name
            - Job Number
            - Target Quantity
            - Completed Quantity
            - Button That Will Take Them To Machine Details Page (Machine.vue)
        - if a user clicks anywhere else then close the overlay/popup