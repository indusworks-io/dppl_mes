# Machine Details Page
We are now working on the Machine Page that is rendered on Machine.vue

## UI Related Requirements:
A High Level Mockup of the Machine Page is available on Machine_Page_UI.png, Path: dppl_mes/frontend/src/pages/Machine_Page_UI.png
Here is the breakdown of the UI:
1. Section 1: Navbar, same as current Implementation
2. Section 2: Machine Page Header. This Section has 2 components:
  - Back Icon Component: This will take the user to previous page
  - Machine Name Component: This will show the name of the Machine
3. Section 3: Machine Details Section. Here we will have the Tabs:
 - Overview: Selected by default
 - Job Cards: This Section will show all the Job Cards associated with this Machine.
 - Downtime Logs: This Section will show all the Downtime Logs associated with this Machine
4. Section 4: Overview Section
- Machine Card: This Component Shows Following:
  - Machine Image if Available else text: No Image Available
  - Factory: Factory Name
  - Area: Area Name
  - Status: Machine Status
- Active Job Card: This Component Shows The Current Active Job for the Machine. The Card Has following:
  - Active Job Text
  - Horizontal Line
  - Job Name Tile: This has tile will have text 'Job Name' and The Actual Job Name that we get from backend
  - Job Number Tile: This has tile will have text 'Job Number' and The Actual Job Number that we get from backend
  - Target Quantity Tile: This has tile will have text 'Target Quantity' and The Actual Target Quantity that we get from backend
  - Completed Quantity Tile: This has tile will have text 'Completed Quantity' and The Actual Completed Quantity that we get from backend
  - Balance Quantity Tile: This has tile will have text 'Balance Quantity' and The Actual Balance Quantity that we get from backend
  - Performance Tile: This has tile will have text 'Performance' and The Actual Performance that we get from backend Based on run_rate_indicator
  The Active Job Card Needs To Updated In Realtime Using The Exisiting Socket Functionality.

The Page Needs To Be Responsive Across Laptop, Tablet & Phone
  

## Additional Instructions:
  - Some of the functionality is already done
  - Read code in the file & make a to do list
  - Take confirmation on plan/to do list and then execute changes