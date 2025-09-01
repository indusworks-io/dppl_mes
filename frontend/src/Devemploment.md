# Core Functionality
1. Job Card List View -- Done
2. Job Card Page View -- Done
3. Downtime Log List View -- Done
4. Downtime Log Page -- Done
5. Job Card Update Functionality
6. Downtime Log Update Functionality


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