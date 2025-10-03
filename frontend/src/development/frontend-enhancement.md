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
