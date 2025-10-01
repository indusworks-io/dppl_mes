# Frontend Enhancements
The goal is that end users should be able to do all activities from frontend and they dont have to access Desk for anything.
To enable this we need to update the Frontend Application.

## Side Navigation Development
Use Frappe UI Sidebar Component For Navigation.
The Navigation structure should be as follows:
- Header
  - Logo: Use From banner_image Field of Website Settings DocType
  - Title: Soundseal MES
  - Subtitle: Logged In Users First Name & Last Name
  - Menu Items: Logout
- Home
- Notifications
- Production
  - Shift Plans
  - Job Cards
  - Output Logs
  - Downtime Logs
  - Job Master
  - Downtime Reasons
- Organization
  - Factories
  - Areas
  - Machines
  - Operators
- Reports (Collapsible Section)

Critical Instructions:
 - Do not use custom css, always try to use Tailwind CSS
 - UI should be responsive across phone, tablet & desktop

Review the current frontend code and first provide set of changes you would make to enable this functionality.