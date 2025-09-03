# Core Functionality
1. Job Card List View -- Done
2. Job Card Page View -- Done
3. Downtime Log List View -- Done
4. Downtime Log Page -- Done
5. Job Card Wastage Functionality -- Done
6. Job Card Update Functionality -- Done
7. Downtime Log Update Functionality -- Done
8. Include Job Card In Downtime Logs -- Done

# Frontend UI/UX Improvement
- Update App Name -- Done
- Update App Icon -- Done
- Update App Favicon -- Done
- Update Page Title -- Done
- Login Page Logo -- Done
- Update Navbar with SoundSeal Logo & Hyperlink -- Done
- Add Logout Functionality -- Done
- Remove Title From Factory Floor Plan Component -- Done
- In FactoryFloorMap.vue, Map overlay, if there is no job running then performance value should be N/A -- Done
- In Machine.vue, Active Job Section, if there is no job running then performance value should be N/A -- Done
- Include Percentage Completed On Map Overlay. -- Done
- Consistent Date Time Format -- Done
- Consitent Duration Format -- Done
- Functionality to load more job cards & more downtime logs
- Sorting logic of job cards & downtime logs -- Done
- Make All Fonts, Borders, Spacing, Radius etc. consistent as per Google Material Design -- Done


# Backend Development
1. Update Desk Navbar Logo -- Done
2. Update Desk Favicon -- Done
3. Update Job Card Report To Incorporate Wastage

## Job Card List View Development
Now we are working on the Job Card Tab in the Machine Page.
Currently we are showing Job Cards as Tiles but we need to show them as list with following data points:
1. Machine 
2. Date
3. Shift
4. Job Name
5. Target Quantity
6. Completed Quantity
7. Status
The List needs to be responsive.
If the user clicks on any list item then it shoul take them to Job Card Page.

## Job Card Page Development
Now we are working on the Job Card Page.
We need to show all the fields available in Job Card DocType except 'Completed Quantity Checker'
You can get the fields from job_card.json path: dppl_mes/dppl_mes/manufacturing/doctype/job_card/job_card.json
The page needs to be responsive.

In the Job Card Page i.e. JobCard.vue we need to make following updates:
1. In The Job Card Title we need to show the ID of the Job Card
2. Remove Job Card Sub Title
3. Reduce the height of Job Card Page Header
4. After the Job Card Page Header show Progress Section
5. Then Basic Information Section, Production Metrics, Performance Metrics & Then Timing Information


## Downtime Log List View Development
Similar to Job Card List View we now need to work on the Downtime Log Tab in the Machine Page.
Currently we are showing Downtime Logs as Tiles but we need to show them as list with following data points:
1. Downtime Log Name
2. Start Date Time -- DD/MM/YYYY and Time should be in AM/PM Format
3. End Date Time -- DD/MM/YYYY and Time should be in AM/PM Format
4. Duration -- From Backend We Will Get Duration In Seconds we need to convert in hours, minutes and seconds
5. Reason
6. Status
The List needs to be responsive.
If the user clicks on any list item then it should take them to Downtime Log Page.


## Downtime Log Page Development
Now we are working on the Downtime Log Page.
We need to show all the fields available in Downtime Log DocType except
You can get the fields from downtime_log.json path: dppl_mes/dppl_mes/manufacturing/doctype/downtime_log/downtime_log.json
The page needs to be responsive.

## Job Card Wastage Functionality
Now we are going to add Job Card Wastage Functionality In The Backend
I have added following float fields in Job Card DocType:
1. Machine Wastage
2. Job Setting Wastage
3. Roll Wastage
4. Printing Wastage
5. Barcode Wastage
6. Total Wastage
Whenever the user updates any of the wastage the backend should sum all of them and put it in Total Wastage field.
You can refer to job_card.json path: dppl_mes/dppl_mes/manufacturing/doctype/job_card/job_card.json for getting information about the fields
The function needs to be added in job_card.py path: dppl_mes/dppl_mes/manufacturing/doctype/job_card/job_card.py

Now we need to show the wastage related fields in Job Card Page.
Add the following:
1. Machine Wastage
2. Job Setting Wastage
3. Roll Wastage
4. Printing Wastage
5. Barcode Wastage
6. Total Wastage
In the Job Card Page i.e. JobCard.vue


## Job Card Update Functionality
Now we are going to add Job Card Update Functionality In The Frontend
We need to allow user to update the following fields of the Job Card:
1. Target Quantity
2. Completed Quantity
3. Status
4. Machine Wastage
5. Job Setting Wastage
6. Roll Wastage
7. Printing Wastage
8. Barcode Wastage
When the user updates any of the field we need to update the same in backend.
You can find the fields & backend logic in following fields:
- job_card.json path: dppl_mes/dppl_mes/manufacturing/doctype/job_card/job_card.json
- job_card.py path: dppl_mes/dppl_mes/manufacturing/doctype/job_card/job_card.py

The Job card also gets updated parellely from external systems using
- create_telemetry() in api.py path: dppl_mes/dppl_mes/api.py
- before_save() in telmetery.py path: dppl_mes/dppl_mes/organization/doctype/telemetry/telemetry.py

Please Note:
1. The project uses Frappe UI that has extra features for talking to frappe based backend.
2. You can find the docuemntation and example of it using document_resource_documentation.md path: dppl_mes/frontend/src/development/document_resource_documentation.md

Think a lot weather we should enable the user to edit the fields directly and provide a save option or provide an update option that opens up a overlay.

Create a To Do Plan before starting development & code change

## Bug Fixes:
Getting following Errors:
Failed to refresh data: TypeError: can't access property "reload", jobCardResource is undefined
    refreshData JobCardUpdateModal.vue:317
    setup JobCardUpdateModal.vue:293

Analyze the code base before making changes

## Downtime Log Update Functionality:
Now we are going to add Downtime Log Update Functionality In The Frontend
We need to allow user to update the following fields of the Downtime Log:
1. Reason

The functionality needs to similar to job card update functionality.


## Include Job Card In Downtime Logs
Now we need to work on updating job card doctype where.
In downtime log we have added link to Job Card. You can check downtime_log.json path: dppl_mes/dppl_mes/manufacturing/doctype/downtime_log/downtime_log.json
We have adde before_save() in downtime_log.py path: dppl_mes/dppl_mes/manufacturing/doctype/downtime_log/downtime_log.py
In the before_save() function we need add code that does following:
- if the Job Card field is empty then:
    - Fetch Job Card for the Machine where Job Card Status is 'In Progress'
    - Update that Job Card in Job Card Field

## Include Downtime Duration Card in Job Card Page:
Now we need to work on updating Job Card Page in frontend i.e. JobCard.vue path: dppl_mes/frontend/src/pages/JobCard.vue
Add a card called Downtime Information where we show total duration of all the downtimes associated with that Job Card in Hours, Minutes and Seconds.


## Update App Icons in PWA 
I have generated PWA Icons and put them as following:
- icons.json path: dppl_mes/frontend/public/icons.json
- android images folder path: dppl_mes/frontend/public/android
- iOs images folder path: dppl_mes/frontend/public/ios
Please update icons section in the PWA part in vite.config.json path: dppl_mes/frontend/vite.config.js
Note: remove the old icons


## Update Navbar
In the Navar Component path: dppl_mes/frontend/src/components/NavBar.vue I want to show only brand image on the left side path: dppl_mes/frontend/public/soundseal-logo.png
Also, remove the Title Property from it and all the places it is being passsed around.
On clicking the image we should come to the main page of the app


## Add Logout Functionality
Currently there is no way for the user to logout from the application.
In the Navbar add a logout Icon on the right side.
If the user clicks on it then log him out and take them to /login or /login?redirect-to=/frontend

## Map Overlay Update
We need to make data pattern same/similar across the app:
In the Map overlay functionality in the FactoryFloorMap.vue path: dppl_mes/frontend/src/components/FactoryFloorMap.vue we need to make following changes:
1. If No Job Running then show in Performance section show 'N/A'
2. If Job is 'In Progress' and run_rate_indicator is 0 then show 'Behind Schedule' In Red Color
3. If Job is 'In Progress' and run_rate_indicator is 1 then show 'On Schedule' In Green Color
4. Show a Balance Quantity
5. Show Completion %

Similarly add the following in MachineCard.vue path: dppl_mes/frontend/src/components/MachineCard.vue
1. Balance Quantity
2. Completion %

Similarly add the following in Machine.vue Active Job Section path: dppl_mes/frontend/src/pages/Machine.vue:
1. Completion %
2. If Job is 'In Progress' and run_rate_indicator is 0 then show 'Behind Schedule' In Red Color
3. If Job is 'In Progress' and run_rate_indicator is 1 then show 'On Schedule' In Green Color

## Load More Job Cards & Downtime Logs
Currently we are getting 50 records from the backend for Job Cards & Downtime Logs.
But there is no option to load more records.
Ideally at the end of the list there should be some option to load more records.
Please functionality that allows a user to load more Job Cards & Downtime Logs if they exisit else show him text 'No More Records found'
Create a Plan Before Changing the Code

## UI Improvement
Currently some components look like they belong to same design system and some belog to different design system.
This makes the app little less polished.
I have created a simple design guide called design.md path: dppl_mes/frontend/src/development/design.md
do the following:
1. Go through the design guide and understand it.
2. Make necessary additions/subtractions from the guide based on our components.
3. Modify/Update the components & Pages as per the design guide.
The objective is to make the app look and feel like a super polished & professional looking.
Think a lot before doing anything.
Create a to do plan before executing.

## Update Job Card Report To Incorporate Wastage
We have added following fields in Job Card DocType:
- Machine Wastage
- Job Setting Wastage
- Roll Wastage
- Printing Wastage
- Barcode Wastage
- Total Wastage
You can find the fields in job_card.json path: dppl_mes/dppl_mes/manufacturing/doctype/job_card/job_card.json

Now we need to incorporate the fields in the Job Report path: dppl_mes/dppl_mes/manufacturing/report/job_report/job_report.py
Go through the exisiting report structure and incorporate changes
The columns that I would like to see are as following:
{'fieldname': 'machine', 'label': 'Machine', 'fieldtype': 'Link', 'options': 'Machine', 'width': 150},
{'fieldname': 'date', 'label': 'Date', 'fieldtype': 'Date', 'width': 120},
{'fieldname': 'shift', 'label': 'Shift', 'fieldtype': 'Data', 'width': 120},
{'fieldname': 'operator', 'label': 'Operator', 'fieldtype': 'Data', 'width': 150},
{'fieldname': 'job_name_one', 'label': 'Job Name', 'fieldtype': 'Link', 'options': 'Job', 'width': 200},
{'fieldname': 'job_number_one', 'label': 'Job No.', 'fieldtype': 'Data', 'width': 150},
{'fieldname': 'target_quantity_one', 'label': 'Target Quantity', 'fieldtype': 'Int', 'width': 150},
{'fieldname': 'completed_quantity_one', 'label': 'Completed Quantity', 'fieldtype': 'Int', 'width': 150},
{'fieldname': 'efficiency_one_percent', 'label': 'Efficiency (%)', 'fieldtype': 'Percent', 'width': 150},
{'fieldname': 'machine_wastage_one', 'label': 'Machine Wastage', 'fieldtype': 'float', 'width': 150},
{'fieldname': 'job_setting_wastage_one', 'label': 'Job Setting Wastage', 'fieldtype': 'float', 'width': 150},
{'fieldname': 'printing_wastage_one', 'label': 'Printing Wastage', 'fieldtype': 'float', 'width': 150},
{'fieldname': 'barcode_wastage_one', 'label': 'Barcode Wastage', 'fieldtype': 'float', 'width': 150},
{'fieldname': 'total_wastage_one', 'label': 'Total Wastage', 'fieldtype': 'float', 'width': 150},
{'fieldname': 'job_name_two', 'label': 'Job Name', 'fieldtype': 'Link', 'options': 'Job', 'width': 200},
{'fieldname': 'job_number_two', 'label': 'Job No.', 'fieldtype': 'Data', 'width': 150},
{'fieldname': 'target_quantity_two', 'label': 'Target Quantity', 'fieldtype': 'Int', 'width': 150},
{'fieldname': 'completed_quantity_two', 'label': 'Completed Quantity', 'fieldtype': 'Int', 'width': 150},
{'fieldname': 'efficiency_two_percent', 'label': 'Efficiency (%)', 'fieldtype': 'Percent', 'width': 150},
{'fieldname': 'machine_wastage_two', 'label': 'Machine Wastage', 'fieldtype': 'float', 'width': 150},
{'fieldname': 'job_setting_wastage_two', 'label': 'Job Setting Wastage', 'fieldtype': 'float', 'width': 150},
{'fieldname': 'printing_wastage_two', 'label': 'Printing Wastage', 'fieldtype': 'float', 'width': 150},
{'fieldname': 'barcode_wastage_two', 'label': 'Barcode Wastage', 'fieldtype': 'float', 'width': 150},
{'fieldname': 'total_wastage_two', 'label': 'Total Wastage', 'fieldtype': 'float', 'width': 150},


## Socket Error: ✅ RESOLVED
~~In the socket2.js frappe.boot.socketio_port command fails as frappe does not exisit in the vue JS application.~~

**FINAL SOLUTION IMPLEMENTED:**
After analyzing Frappe CRM's working implementation, simplified our approach:

**Backend Changes (`dppl_mes/api.py`):**
- Simplified `get_boot()` to match Frappe CRM's minimal approach
- Removed complex Docker detection and custom port configuration 
- Uses only essential fields: `frappe_version`, `default_route`, `site_name`, `csrf_token`

**Frontend Changes:**
- **`socket.js`**: Created simple socket implementation following Frappe CRM pattern
  - Uses default port 9000, standard hostname detection
  - Handles `refetch_resource` events for frappe-ui integration
  - Exports both `initSocket()` and `useSocket()` for component usage
- **`main.js`**: Simplified context loading to match Frappe CRM exactly
  - Clean context loading without complex error handling
  - Uses local socket.js instead of frappe-ui utils

**Key Insight:** 
The issue was over-engineering. Frappe CRM works perfectly with simple, standard patterns. Our custom complex configuration was causing more problems than it solved.

**Files Modified:**
- ✅ `dppl_mes/api.py` - Simplified to Frappe CRM pattern
- ✅ `frontend/src/socket.js` - New simple implementation  
- ✅ `frontend/src/main.js` - Simplified context loading
- ✅ Removed obsolete `socket2.js`