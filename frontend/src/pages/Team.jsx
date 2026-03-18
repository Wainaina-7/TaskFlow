import { useEffect, useState } from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { Plus, Users, AlertCircle, Trash2 } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

const collaborationSchema = Yup.object().shape({
  user_id: Yup.number().required('User required').positive().integer(),
  project_id: Yup.number().required('Project required').positive().integer(),
  role: Yup.string().required('Role required').min(3),
})

const roleColors = {
  'Manager': 'bg-purple-100 text-purple-700',
  'Developer': 'bg-blue-100 text-blue-700',
  'Viewer': 'bg-slate-100 text-slate-700',
}

export default function Team() {
  const [collabs, setCollabs] = useState([])
  const [message, setMessage] = useState(null)
  const [messageType, setMessageType] = useState(null)
  const [loading, setLoading] = useState(true)

  const loadCollabs = () => {
    setLoading(true)
    fetch(`${API_BASE}/collaborations`)
      .then((res) => res.json())
      .then(setCollabs)
      .catch((err) => {
        console.error(err)
        setMessage('Unable to load collaborations')
        setMessageType('error')
      })
      .finally(() => setLoading(false))
  }

  const deleteCollab = (id) => {
    if (!confirm('Are you sure you want to remove this collaboration?')) return
    
    fetch(`${API_BASE}/collaborations/${id}`, { method: 'DELETE' })
      .then(() => {
        loadCollabs()
        setMessage('Collaboration removed')
        setMessageType('success')
        setTimeout(() => setMessage(null), 3000)
      })
      .catch((err) => {
        console.error(err)
        setMessage('Unable to delete collaboration')
        setMessageType('error')
      })
  }

  useEffect(() => {
    loadCollabs()
  }, [])

  return (
    <div>
      <div className="mb-8">
        <h1 className="page-title mb-2">Team & Collaboration</h1>
        <p className="text-slate-600">Manage collaborators and team members</p>
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
              Add Member
            </h3>
            <Formik
              initialValues={{ user_id: '', project_id: '', role: 'Developer' }}
              validationSchema={collaborationSchema}
              onSubmit={(values, actions) => {
                const payload = {
                  user_id: Number(values.user_id),
                  project_id: Number(values.project_id),
                  role: values.role,
                }

                fetch(`${API_BASE}/collaborations`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(payload),
                })
                  .then(() => {
                    loadCollabs()
                    actions.resetForm()
                    setMessage('Collaboration created successfully')
                    setMessageType('success')
                    setTimeout(() => setMessage(null), 3000)
                  })
                  .catch((err) => {
                    console.error(err)
                    setMessage('Unable to create collaboration')
                    setMessageType('error')
                  })
                  .finally(() => actions.setSubmitting(false))
              }}
            >
              {({ isSubmitting, errors, touched }) => (
                <Form className="space-y-4">
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
                    <label className="form-label">Role</label>
                    <Field name="role" as="select" className="form-input">
                      <option value="Developer">Developer</option>
                      <option value="Manager">Manager</option>
                      <option value="Viewer">Viewer</option>
                    </Field>
                    {errors.role && touched.role && (
                      <p className="mt-1 small-muted text-red-600">{errors.role}</p>
                    )}
                  </div>
                  <button type="submit" disabled={isSubmitting} className="btn-primary w-full">
                    {isSubmitting ? 'Adding...' : 'Add Member'}
                  </button>
                </Form>
              )}
            </Formik>
          </div>
        </div>

        {/* Collaborations List */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
              <Users className="text-primary-600" />
              Team Members {collabs.length > 0 && `(${collabs.length})`}
            </h2>

            {loading ? (
              <div className="py-8 text-center text-slate-500">Loading collaborations...</div>
            ) : collabs.length === 0 ? (
              <div className="py-12 text-center">
                <Users size={48} className="mx-auto mb-3 text-slate-300" />
                <p className="text-slate-500">No team members yet. Add your first collaborator!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {collabs.map((collab) => (
                  <div
                    key={collab.id}
                    className="p-4 border border-slate-200 rounded-lg hover:shadow-md transition-all"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <h3 className="font-semibold text-slate-900">
                          {collab.user || `User #${collab.user_id}`}
                        </h3>
                        <p className="text-sm text-slate-600 mt-1">
                          {collab.project || `Project #${collab.project_id}`}
                        </p>
                        <div className="mt-3 flex items-center gap-2">
                          <span
                            className={`badge ${roleColors[collab.role] || 'bg-slate-100 text-slate-700'}`}
                          >
                            {collab.role}
                          </span>
                          <span className="small-muted">ID: {collab.id}</span>
                        </div>
                      </div>
                      <button
                        onClick={() => deleteCollab(collab.id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="Remove member"
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
