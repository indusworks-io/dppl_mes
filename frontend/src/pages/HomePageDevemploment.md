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
        - Iterate through all the paths in the SVG and create a reactive object for each machine path
        - Create a function that can be used to update the color of the machine object path to #FF0000 or #00FF00 or #FFFFFF
        - If the Machine is_active is 0 then change color of the machine object path to #FFFFFF
        

    6. Build/Update Dashboard Component
        - In DashboardComponent.vue
        - Create Sections with Area as the name.
        - The Area Should be In increasing order based on sequence_number in the Area List
        - In each Area Render MachineCard.vue.
        - The Machine Card should In increasing order based on sequence_number in the Machine List
