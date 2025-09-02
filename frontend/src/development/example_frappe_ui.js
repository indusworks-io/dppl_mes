const todos = createListResource({
	// name of the doctype
	doctype: "ToDo",

	// list of fields
	fields: ["name", "description", "status"],

	// object of filters to apply
	filters: {
		status: "Open",
	},

	// the order in which records must be sorted
	orderBy: "creation desc",

	// index from which records should be fetched
	// default value is 0
	start: 0,

	// number of records to fetch in a single request
	// default value is 20
	pageLength: 20,

	// parent doctype when you are fetching records of a child doctype
	parent: null,

	// set to 1 to enable debugging of list query
	debug: 0,

	// cache key to cache the resource
	// can be a string
	cache: "todos",
	// or an array that can be serialized
	cache: ["todos", "faris@frappe.io"],

	// default value for url is "frappe.client.get_list"
	// specify url if you want to use a custom API method
	url: "todo_app.api.get_todos",

	// make the first request automatically
	auto: true,

	// events
	// error can occur from failed request
	onError(error) {},
	// on successful response
	onSuccess(data) {},
	// transform data before setting it
	transform(data) {
		for (const d of data) {
			d.open = false
		}
		return data
	},
	// other events
	fetchOne: {
		onSuccess() {},
		onError() {},
	},
	insert: {
		onSuccess() {},
		onError() {},
	},
	delete: {
		onSuccess() {},
		onError() {},
	},
	setValue: {
		onSuccess() {},
		onError() {},
	},
	runDocMethod: {
		onSuccess() {},
		onError() {},
	},
})
