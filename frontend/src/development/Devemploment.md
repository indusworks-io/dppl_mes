# Core Functionality
1. Job Card List View -- Done
2. Job Card Page View -- Done
3. Downtime Log List View -- Done
4. Downtime Log Page -- Done
5. Job Card Wastage Functionality -- Done
6. Job Card Update Functionality -- Done
7. Downtime Log Update Functionality -- Done


# UI/UX Improvement
1. Update App Name
2. Update App Icon
3. Update App Favicon
4. Update Page Title
5. Update Navbar with SoundSeal Logo & Hyperlink
6. Add Logout Functionality
7. Make All Fonts, Borders, Spacing, Radius etc. consistent as per Google Material Design
8. Login Page Logo
9. Remove Title From Factory Floor Plan Component
10. In FactoryFloorMap.vue, Map overlay, if there is no job running then performance value should be N/A
11. In Machine.vue, Active Job Section, if there is no job running then performance value should be N/A

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