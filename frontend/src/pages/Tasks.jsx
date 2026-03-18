import { useEffect, useState } from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { Plus, Trash2, CheckSquare, AlertCircle } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

const taskSchema = Yup.object().shape({
  title: Yup.string().required('Task title required'),
  user_id: Yup.number().required('User ID required').positive('Must be positive').integer('Must be integer'),
  project_id: Yup.number().required('Project ID required').positive('Must be positive').integer('Must be integer'),
  status: Yup.string().oneOf(['Pending', 'In Progress', 'Done']),
})

const statusColors = {
  'Pending': 'bg-yellow-100 text-yellow-700',
  'In Progress': 'bg-blue-100 text-blue-700',
  'Done': 'bg-green-100 text-green-700',
}

export default function Tasks() {
  const [tasks, setTasks] = useState([])
  const [message, setMessage] = useState(null)
  const [messageType, setMessageType] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchTasks = () => {
    setLoading(true)
    fetch(`${API_BASE}/tasks`)
      .then((res) => res.json())
      .then(setTasks)
      .catch((err) => {
        console.error(err)
        setMessage('Unable to load tasks')
        setMessageType('error')
      })
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  const deleteTask = (id) => {
    if (!confirm('Are you sure you want to delete this task?')) return
    
    fetch(`${API_BASE}/tasks/${id}`, { method: 'DELETE' })
      .then(() => {
        fetchTasks()
        setMessage('Task deleted successfully')
        setMessageType('success')
        setTimeout(() => setMessage(null), 3000)
      })
      .catch((err) => {
        console.error(err)
        setMessage('Unable to delete task')
        setMessageType('error')
      })
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="page-title mb-2">Tasks</h1>
        <p className="text-slate-600">Create and manage your tasks</p>
      </div>

      {message && (
        <div
          className={`mb-6 p-4 rounded-lg flex items-center gap-3 ${
            messageType === 'error'
              ? 'bg-red-50 border border-red-200'
              : 'bg-green-50 border border-green-200'
          }`}
        >
          <AlertCircle
            size={20}
            className={messageType === 'error' ? 'text-red-600' : 'text-green-600'}
          />
          <span className={messageType === 'error' ? 'text-red-800' : 'text-green-800'}>
            {message}
          </span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Form */}
        <div className="lg:col-span-1">
          <div className="card sticky top-24">
            <h3 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
              <Plus size={20} className="text-primary-600" />
              New Task
            </h3>
            <Formik
              initialValues={{
                title: '',
                description: '',
                user_id: '',
                project_id: '',
                status: 'Pending',
              }}
              validationSchema={taskSchema}
              onSubmit={(values, actions) => {
                const payload = {
                  ...values,
                  user_id: Number(values.user_id),
                  project_id: Number(values.project_id),
                }

                fetch(`${API_BASE}/tasks`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(payload),
                })
                  .then(() => {
                    fetchTasks()
                    actions.resetForm()
                    setMessage('Task created successfully')
                    setMessageType('success')
                    setTimeout(() => setMessage(null), 3000)
                  })
                  .catch((err) => {
                    console.error(err)
                    setMessage('Unable to create task')
                    setMessageType('error')
                  })
                  .finally(() => actions.setSubmitting(false))
              }}
            >
              {({ isSubmitting, errors, touched }) => (
                <Form className="space-y-4">
                  <div>
                    <label className="form-label">Title</label>
                    <Field
                      name="title"
                      placeholder="e.g., Fix login bug"
                      className="form-input"
                    />
                    {errors.title && touched.title && (
                      <p className="mt-1 small-muted text-red-600">{errors.title}</p>
                    )}
                  </div>
                  <div>
                    <label className="form-label">Description</label>
                    <Field
                      name="description"
                      as="textarea"
                      placeholder="Task details..."
                      className="form-input resize-none h-16"
                    />
                  </div>
                  <div>
                    <label className="form-label">User ID</label>
                    <Field
                      name="user_id"
                      type="number"
                      placeholder="1"
                      className="form-input"
                    />
                    {errors.user_id && touched.user_id && (
                      <p className="mt-1 small-muted text-red-600">{errors.user_id}</p>
                    )}
                  </div>
                  <div>
                    <label className="form-label">Project ID</label>
                    <Field
                      name="project_id"
                      type="number"
                      placeholder="1"
                      className="form-input"
                    />
                    {errors.project_id && touched.project_id && (
                      <p className="mt-1 small-muted text-red-600">{errors.project_id}</p>
                    )}
                  </div>
                  <div>
                    <label className="form-label">Status</label>
                    <Field name="status" as="select" className="form-input">
                      <option value="Pending">Pending</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Done">Done</option>
                    </Field>
                  </div>
                  <button type="submit" disabled={isSubmitting} className="btn-primary w-full">
                    {isSubmitting ? 'Creating...' : 'Create Task'}
                  </button>
                </Form>
              )}
            </Formik>
          </div>
        </div>

        {/* Tasks List */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
              <CheckSquare className="text-primary-600" />
              All Tasks {tasks.length > 0 && `(${tasks.length})`}
            </h2>

            {loading ? (
              <div className="py-8 text-center text-slate-500">Loading tasks...</div>
            ) : tasks.length === 0 ? (
              <div className="py-12 text-center">
                <CheckSquare size={48} className="mx-auto mb-3 text-slate-300" />
                <p className="text-slate-500">No tasks yet. Create your first task!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {tasks.map((task) => (
                  <div
                    key={task.id}
                    className="p-4 border border-slate-200 rounded-lg hover:shadow-md transition-all"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <h3 className="font-semibold text-slate-900">{task.title || 'Untitled'}</h3>
                        {task.description && (
                          <p className="text-sm text-slate-600 mt-2">{task.description}</p>
                        )}
                        <div className="mt-3 flex items-center gap-2 text-xs">
                          <span className={`badge ${statusColors[task.status] || 'bg-slate-100 text-slate-700'}`}>
                            {task.status || 'Pending'}
                          </span>
                          <span className="small-muted">Task #{task.id} • User #{task.user_id} • Project #{task.project_id}</span>
                        </div>
                      </div>
                      <button
                        onClick={() => deleteTask(task.id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="Delete task"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
