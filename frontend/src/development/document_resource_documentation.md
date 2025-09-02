Options API 
You can also define resources if you are using Options API. You need to register the resourcesPlugin first.

main.js

js
import { resourcesPlugin } from 'frappe-ui'
app.use(resourcesPlugin)
In your .vue file, you can declare all your resources under the resources key as functions. The resource object will be available on this.$resources.[name]. In the following example, this.$resources.todo is the resource object.

Component.vue
<script>
export default {
  resources: {
    todo() {
      return {
        type: 'document',
        doctype: 'ToDo',
        name: '1',
      }
    },
  },
}
</script>

List of Options and API 
Here is the list of all options and APIs that are available on a list resource.

Options
let todo = createDocumentResource({
  // name of the doctype
  doctype: 'ToDo',

  // name of the record
  name: '',

  // define doc methods to use as resources
  whitelistedMethods: {
    sendEmail: 'send_email',
  },
  // the above configuration enables the following API
  // todo.sendEmail.submit()

  // events
  // error can occur from failed request
  onError(error) {},
  // on successful response
  onSuccess(data) {},
  // transform data before setting it
  transform(doc) {
    doc.open = false
    return doc
  },
  // other events
  delete: {
    onSuccess() {},
    onError() {},
  },
  setValue: {
    onSuccess() {},
    onError() {},
  },
})

API 
A document resource is made up of multiple individual resources. In our running example, the resource object that fetches the document is at todos.get. So all the  are available on this object. Similarly, there are resources for setValue, and delete.

let todo = createDocumentResource({...})

todo.doc // doc returned from request
todo.reload() // reload the doc

// update options
todo.update({
  doctype: '',
  name: ''
})

todo.get // doc resource
todos.get.loading // true when data is being fetched
todos.get.error // error that occurred from making the request
todos.get.promise // promise object of the request, can be awaited

// resource to set value(s) on the document
todos.setValue
todos.setValue.submit({
    // field value pairs to set
    status: 'Closed',
    description: 'Updated description'
})

// same as setValue but debounced
todos.setValueDebounced
// will run once after 500ms
todos.setValueDebounced.submit({
    description: 'Updated description'
})

// resource to delete the document
todos.delete
todos.delete.submit()

// if whitelistedMethods is defined
// you get a resource for each whitelisted method
todos.sendEmail
todos.sendEmail.submit
todos.sendEmail.loading

