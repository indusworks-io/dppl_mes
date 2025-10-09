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

## List View Component Development

You are an expert Vue 3 + Tailwind + Frappe UI developer.
Write a reusable Vue 3 component called **`ListView.vue`** with the following requirements:

---

### Objective

Build a **common ListView component** that can be used across multiple Frappe Doctypes.

The component must handle:

1. **Data Fetching** → Use `createListResource` from `frappe-ui` to fetch records.
2. **Data Filtering** → Support passing filters from parent and applying them dynamically.
3. **Data Pagination** → Support next/previous pagination using the list resource.
4. **Heading Section** → Show the Doctype name and a "Create" button (navigates to new form page).
5. **Sub Heading Section** → Show buttons for:

   * Filter dropdown
   * Refresh list
   * Sorting options
6. **Body Section** → Render a table/grid of records with each row clickable → navigates to the record detail page.
7. **Custom Renderers** → Support chips, buttons, and custom formatting for specific fields via prop config.

---

### 🔹 Tech Stack Constraints

* Use **Vue 3 `<script setup>` style**
* Use **Tailwind CSS** for layout and responsiveness
* Use **Frappe UI components** for UI (List, Button, Dropdown, Avatar, Badge, etc.)
* Must work across **mobile, tablet, and desktop** (responsive table/grid).

---

### 🔹 Props

```js
props: {
  doctype: { type: String, required: true },   // e.g. "Job Card"
  title: { type: String, required: true },     // heading title
  columns: { type: Array, required: true },    // [{ fieldname, label, width?, formatter? }]
  filters: { type: Array, default: () => [] }, // [["status", "=", "Open"]]
  orderBy: { type: String, default: "modified desc" },
  pageLength: { type: Number, default: 20 },
  rowActions: { type: Array, default: () => [] }, // [{ label, icon, action }]
}
```

---

### 🔹 Events to Emit

* `row-click` (when a row is clicked)
* `row-action` (when a row action is triggered)
* `filters-change` (when filters are updated)
* `page-change` (when pagination changes)

---

### 🔹 UI Layout

1. **Header Section**

   * Show `title` (doctype name)
   * Show a `Create` button → emits `"create"` event or navigates to `Form` page

2. **Subheader Section**

   * Filter dropdown (from props / predefined filters)
   * Refresh button → reloads resource
   * Sort button → toggle order

3. **Body Section**

   * Table/grid responsive layout
   * For each column: render value or use `formatter` function
   * Support custom Vue slot for fully custom cell rendering

4. **Pagination Controls**

   * Next / Previous buttons
   * Show current page info

---

### 🔹 Example Usage

```vue
<ListView
  doctype="Job Card"
  title="Job Cards"
  :columns="[
    { fieldname: 'name', label: 'Job ID' },
    { fieldname: 'operator', label: 'Operator' },
    { fieldname: 'status', label: 'Status', formatter: (val) => val.toUpperCase() },
    { fieldname: 'start_time', label: 'Start Time', formatter: (val) => new Date(val).toLocaleString() },
  ]"
  :filters="[['status', '=', 'Open']]"
  orderBy="creation desc"
  :rowActions="[
    { label: 'Edit', icon: 'edit', action: (row) => editJob(row) },
    { label: 'Close', icon: 'check', action: (row) => closeJob(row) }
  ]"
  @row-click="openJobDetail"
  @filters-change="updateFilters"
/>
```

---

### 🔹 Deliverables

* Full `ListView.vue` component code in Vue 3 (`<script setup>`)
* Use Frappe UI’s `createListResource` for fetching data
* Use Frappe UI components for buttons/dropdowns
* Responsive design with Tailwind
* Support props/events as defined above
* Allow **custom renderers** (via `formatter` in `columns`, and via slots)




Awesome 👌 you’re basically asking me to give you the **“master prompt”** so Claude Code can build a **production-ready, schema-driven `DetailView.vue`** that works for all doctypes, with future-proofing in mind.

Here’s the **ultimate detailed prompt** (with all enhancements I’d recommend):

---

# 📌 Master Prompt for Claude Code: `DetailView.vue`

You are an expert **Vue 3 + Tailwind CSS + Frappe UI** developer.
Write a reusable Vue 3 component called **`DetailView.vue`** with the following requirements:

---

## 🔹 Objective

Build a **common DetailView component** that dynamically renders doctype forms based on the schema in Frappe.

The component must support:

1. **Auto-fetching Doctype Schema** → fetch field definitions via `frappe.desk.form.load.getdoctype`.
2. **Create New Record** → if no record name is passed, render empty form and allow saving.
3. **View Existing Record** → if record name is passed, fetch and display data.
4. **Update Record** → allow editing fields and saving back.
5. **Delete Record** → support deleting the current record.
6. **View Connected Records** → render related doctypes in sub-sections using `<ListView.vue>`.
7. **Responsive UI** → must work across mobile, tablet, and desktop.

---

## 🔹 Tech Stack Constraints

* Vue 3 `<script setup>` syntax.
* Tailwind CSS for layout + responsiveness.
* Use **Frappe UI** components (`Button`, `Input`, `Textarea`, `Select`, `Checkbox`, `Autocomplete`, `Badge`, etc.) wherever possible.
* Use **Frappe UI resources**:

  * `createDocumentResource` for CRUD (insert, save, delete).
  * `createResource` for fetching doctype schema.
* Form layout should be **2-column on desktop, 1-column on mobile**.

---

## 🔹 Props

```js
props: {
  doctype: { type: String, required: true },    // e.g. "Job Card"
  name: { type: String, default: null },        // record name, null = new
  related: { type: Array, default: () => [] },  // list of related doctypes
}
```

---

## 🔹 State & Behavior

1. **Mode Handling**

   * `view` mode → show read-only fields.
   * `edit` mode → show inputs for editing.
   * `create` mode → if no name, render form for new record.

2. **Lifecycle**

   * On mount → fetch schema & record (if `name` provided).
   * If new record → initialize blank doc using schema defaults.

3. **CRUD Actions**

   * Save → `doc.insert()` if new, `doc.save()` if existing.
   * Delete → `doc.delete()`.
   * Refresh → refetch record.
   * Cancel → revert to view mode.

4. **Connected Records**

   * Render `<ListView :doctype="rel" :filters="[[linkField, '=', doc.name]]" />` for each related doctype.
   * Auto-detect `linkField` if possible (e.g. `job_card` for “Output Log”).

---

## 🔹 Field Rendering Rules

For each field in schema, render appropriate Frappe UI component:

| Frappe Fieldtype | Vue/Frappe UI Component                           |
| ---------------- | ------------------------------------------------- |
| Data             | `<Input type="text" />`                           |
| Small Text       | `<Textarea />`                                    |
| Text             | `<Textarea />`                                    |
| Text Editor      | `<RichTextEditor />` (if available)               |
| Select           | `<Select :options="field.options.split('\n')" />` |
| Check            | `<Checkbox />`                                    |
| Date             | `<DatePicker />`                                  |
| Datetime         | `<DateTimePicker />`                              |
| Int              | `<Input type="number" />`                         |
| Float            | `<Input type="number" step="0.01" />`             |
| Currency         | `<Input type="number" step="0.01" />`             |
| Percent          | `<Input type="number" step="0.01" />`             |
| Link             | `<Autocomplete :doctype="field.options" />`       |
| Table            | Render child table using `<ListView>` or sub-grid |
| Attach           | `<FileUploader />`                                |
| Image            | `<ImageUploader />`                               |
| Rating           | `<Rating />` (if available or custom)             |

* Required fields (`reqd=1`) → mark with `*` and validate before save.
* Read-only fields → display as plain text in view mode.

---

## 🔹 UI Layout

1. **Header Section**

   * Show doctype name + record title (`doc.name`).
   * Buttons: **Edit / Save / Cancel / Delete / Refresh**.

2. **Form Section**

   * Responsive grid (2 columns desktop, 1 column mobile).
   * Render fields dynamically from schema.
   * In `view` mode → show read-only values.
   * In `edit` or `create` mode → render appropriate inputs.

3. **Related Records Section**

   * For each entry in `related` prop, render a titled section:

     ```vue
     <ListView :doctype="rel" :filters="[[linkField, '=', doc.name]]" />
     ```

---

## 🔹 Events

* `saved` → after record is created/updated.
* `deleted` → after record deleted.
* `cancel` → when user cancels editing.
* `refreshed` → when record is reloaded.

---

## 🔹 Example Usage

```vue
<DetailView
  doctype="Job Card"
  :name="route.params.name || null"
  :related="['Output Log', 'Downtime Log']"
  @saved="refreshList"
  @deleted="goBack"
  @cancel="goBack"
/>
```

---

## 🔹 Deliverables

Produce a **fully working `DetailView.vue`**:

* Uses `createDocumentResource` + schema API.
* Dynamically renders form fields based on fieldtype.
* Supports create, view, update, delete.
* Supports related doctypes via `<ListView>`.
* Responsive Tailwind layout.
* Emits the defined events.
* Clean, modular Vue 3 `<script setup>` code.

---


In JobCards.vue, We need following columns in the List View:
fieldname - label
1. name - Job Card ID
2. machine - Machine
3. date - Date
4. shift - Shift
5. job_name - Job Name
6. completed_quantity - Completed Quantity
7. target_quantity - Target Quantity
8. Progress - Computed Field Based on completed_quantity & target_quantity
9. status - Status


In OutputLogs.vue, We need following columns in the List View:
fieldname - label
1. name - Output Log ID
2. timestamp - Timestamp
3. job_card - Job Card
4. machine - Machine
5. output - Output

In DowntimeLogs.vue, We need following columns in the List View:
fieldname - label
1. name - Downtime Log ID
2. machine - Machine
3. start_date_time - Start Date Time
4. end_date_time - End Date Time
5. duration - Duration
6. reason - Reason
7. status - Status

In Jobs.vue, We need following columns in the List View:
fieldname - label
1. job_name - Job Name
2. job_number - Job Number
3. complexity_level - Complexity Level
4. ideal_run_rate - Ideal Run Rate

In DowntimeReasons.vue, We need following columns in the List View:
fieldname - label
1. downtime_reason - Downtime Reason
2. category - Category
3. is_active - Is Active?

In Factories.vue, We need following columns in the List View:
fieldname - label
1. factory_name - Factory Name
2. is_active - Is Active?

In Areas.vue, We need following columns in the List View:
fieldname - label
1. area_name - Area Name
2. factory - Factory
3. is_active - Is Active?

In Machines.vue, We need following columns in the List View:
fieldname - label
1. machine_name - Machine Name
2. area - Area
3. factory - Factory
4. is_active - Is Active?

In Operators.vue, We need following columns in the List View:
fieldname - label
1. operator_name - Operator Name
2. employee_code - Employee Code


Details Page:
1. ShiftPlan.vue
2. JobCard.vue
3. OutputLog.vue
4. DowntimeLog.vue
5. Job.vue
6. DowntimeReason.vue
7. Factory.vue
8. Area.vue
9. Machine.vue
10. Operator.vue

We need to update ShiftPlan.vue page to handle following:
1. Create New Shift Plan
2. Update Existing Shift Plan
Check the following files from backend:
- shift_plan.json: dppl_mes/dppl_mes/manufacturing/doctype/shift_plan/shift_plan.json
- shift_plan.js: dppl_mes/dppl_mes/manufacturing/doctype/shift_plan/shift_plan.js
and implement same functionality in the frontend vue application

Also, show 2 tabs: Overview & Job Cards
In Overview tab show the fields & tables
In Job Cards tab show list of connected job cards.

Keep in mind:
1. Use Frappe UI components as much as possible
2. Use Create List Resource & Create Document Resource

Make following updates to JobCard.vue:
0. Add a Back Icon before the Shift Plan Name in Header Section. Clicking on back should take the user back to list view
1. Fetch Factories from backend using create list resource and update Factory Field
2. Fetch Shifts from backend using create list resource and update Shift Field
3. Fetch Operators from backend using create list resource and update Operator Field
4. Fetch Jobs from backend using create list resource and Update Job 1 & Job 2 Field
5. Increase Job 1 qty & Job 2 qty Field With to match Job 1 & Job 2 Field
6. The use should update the Job 1 Duration in hours and when we update the backend we convert to seconds
7. Place add Row button at the bottom of the table 
8. In Job Cards Tab remove the following:
   - Header Section & Sub Header Section
9. Job Cards are not showing in Job Cards Tab


In ShiftPlan.vue: On saving the document the name of the shift plan did not get updated + I got following warning in console: [Vue warn]: Property "refreshing" was accessed during render but is not 
defined on instance. 
  at <ShiftPlan onVnodeUnmounted=fn<onVnodeUnmounted> ref=Ref< 
Proxy { <target>: Proxy, <handler>: {…} }
 > > 
  at <RouterView> 
  at <App> runtime-core.esm-bundler.js:51:13

Check why this is happening & plan to fix it... remember stick with standard frappe UI functionality...

I have installed Frappe CRM app that uses vue js & Frappe UI... Please check how they are handling this... lets do similar functionality... 
the app is in /home/navneetjain89/frappe-bench/apps/crm you can access files in it always.


We need to update JobCard.vue page to handle:
- Create New Job Card
- Update Existing Job Card
Check the following files from backend to understand fields & layout:
- job_card.json: dppl_mes/dppl_mes/manufacturing/doctype/job_card/job_card.json
We need to do the following:
- Use Frappe UI Components Only. Currently all fields are just text input within a span. It should be a frappe UI Component.
- Use CreateDocumentResource for creating new document and updating existing document. Let CreateDocumentResource handle state & functions.
- Use CreateListResource for fetching Related Records
- Keep the current progress section & Job Card layout details grid as it is
- Instead of edit button that opens a modal/popup the user should be able to update the fields directly from the page/form
- While Creating a new document for the first time the user should only be able to edit/update following fields:
    - machine
    - date
    - shift
    - operator
    - job_name
    - target_quantity
    - job_sequence_number
    - planned_start_date_time
    - planned_end_date_time
- While updating a existing document the user should be able to edit/update the following:
   - status
   - completed_quantity
   - machine_wastage
   - job_setting_wastage
   - roll_wastage
   - printing_wastage
   - barcode_wastage
- Add following tabs:
   - Output logs: Show list of output logs that are linked to this job card.
   - Downtime Logs: Show list of Downtime logs that are linked to this job card.
- Before implementing review how you created ShiftPlan.vue page. we need something similar to that.
Understand all the requirements and create a to do on how to implement this.

Lets have all the fields in single column with following sequence:
- machine
- date
- shift
- operator
- job_name
- target_quantity
- job_sequence_number
- planned_start_date_time
- planned_end_date_time

We need to update OutputLog.vue page to handle viewing of a Output log Document.
Check the following files from backend to understand fields & layout:
- output_log.json: dppl_mes/dppl_mes/manufacturing/doctype/output_log/output_log.json
We need to do the following:
- Use Frappe UI Components Only.
- Use CreateDocumentResource
- The user can only view the record. No fields are editable. The user cannot create a new output log.


We need to now handle creating & updating following documents:
1. Jobs
2. Downtime Reasons
3. Factories
4. Areas
5. Operators
Each document has a .json file inside the dppl folder.
Update the corrosponding page to handle create & Update.
Keep in mind:
1. Use Frappe UI Component
2. Use a simple Single Column Format
3. Use CreateDocumentResource to handle create & update
4. Use Save Button to handle create & update
5. Use CreateListResource to fetch related links.
This is a big task. Create a detailed to plan before executing.
You can refer to ShiftPlan.vue to see how you handled it earlier.

We need to update the MachineCard.vue to make the UI similar to other pages like JobCard.vue
- Update the page to make in consistent through out the app
- Update the Job Cards & Downtime Logs Table with the ListView.vue