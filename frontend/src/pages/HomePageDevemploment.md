# Homepage Development

## Instructions:
    - Following is the expected outcome for the realtime map update Functionality.
    - Some of the functionality is already done
    - Read code in the file & make a to do list
    - Take confirmation on plan/to do list and then execute changes

## Files To Use/Modify
    - Home.vue -- Path: dppl_mes/frontend/src/pages/Home.vue
    - HomePageControls.vue -- Path: dppl_mes/frontend/src/components/HomePageControls.vue
    - FactoryFloorMap.vue -- Path: dppl_mes/frontend/src/components/FactoryFloorMap.vue
    - FactoryFilter.vue -- Path: dppl_mes/frontend/src/components/FactoryFilter.vue
    - api.py -- Path: dppl_mes/dppl_mes/api.py

## Expected Outcomes:
  Build/Update Factory Floor Map:
    - The backend will publish realtime events to the frontend using frappe.publish_realtime() functionality in create_telemetry() in api.py
    - Update the corrosponding machine path based on following logic:
      - if run_rate_indicator == 1 then green else red
    - If a user clicks on the machine path open a overlay/popup to show:
        - Job Name
        - Job Number
        - Target Quantity
        - Completed Quantity
        - Button That Will Take Them To Machine Details Page (Machine.vue)
    - if a user clicks anywhere else then close the overlay/popup