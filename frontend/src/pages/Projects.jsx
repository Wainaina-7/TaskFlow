import { useEffect, useState } from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { Plus, Folder, AlertCircle } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

const projectSchema = Yup.object().shape({
  title: Yup.string().required('Title required').min(3, 'Min 3 chars'),
  description: Yup.string().optional(),
})

export default function Projects() {
  const [projects, setProjects] = useState([])
  const [message, setMessage] = useState(null)
  const [messageType, setMessageType] = useState(null)
  const [loading, setLoading] = useState(true)

  const loadProjects = () => {
    setLoading(true)
    fetch(`${API_BASE}/projects`)
      .then((res) => res.json())
      .then(setProjects)
      .catch((err) => {
        console.error(err)
        setMessage('Unable to load projects')
        setMessageType('error')
      })
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    loadProjects()
  }, [])

  return (
    <div>
      <div className="mb-8">
        <h1 className="page-title mb-2">Projects</h1>
        <p className="text-slate-600">Create and manage your projects</p>
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
              New Project
            </h3>
            <Formik
              initialValues={{ title: '', description: '' }}
              validationSchema={projectSchema}
              onSubmit={(values, actions) => {
                fetch(`${API_BASE}/projects`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(values),
                })
                  .then((r) => r.json())
                  .then(() => {
                    loadProjects()
                    actions.resetForm()
                    setMessage('Project created successfully')
                    setMessageType('success')
                    setTimeout(() => setMessage(null), 3000)
                  })
                  .catch((err) => {
                    console.error(err)
                    setMessage('Unable to create project')
                    setMessageType('error')
                  })
                  .finally(() => actions.setSubmitting(false))
              }}
            >
              {({ isSubmitting, errors, touched }) => (
                <Form className="space-y-4">
                  <div>
                    <label className="form-label">Project Title</label>
                    <Field
                      name="title"
                      placeholder="e.g., Website Redesign"
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
                      placeholder="Describe your project..."
                      className="form-input resize-none h-20"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="btn-primary w-full"
                  >
                    {isSubmitting ? 'Creating...' : 'Create Project'}
                  </button>
                </Form>
              )}
            </Formik>
          </div>
        </div>

        {/* Projects List */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
              <Folder className="text-primary-600" />
              All Projects {projects.length > 0 && `(${projects.length})`}
            </h2>

            {loading ? (
              <div className="py-8 text-center text-slate-500">Loading projects...</div>
            ) : projects.length === 0 ? (
              <div className="py-12 text-center">
                <Folder size={48} className="mx-auto mb-3 text-slate-300" />
                <p className="text-slate-500">No projects yet. Create your first project!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {projects.map((project) => (
                  <div
                    key={project.id}
                    className="p-4 border border-slate-200 rounded-lg hover:border-primary-300 hover:shadow-md transition-all"
                  >
                    <h3 className="font-semibold text-slate-900">{project.title}</h3>
                    {project.description && (
                      <p className="text-sm text-slate-600 mt-2">{project.description}</p>
                    )}
                    <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
                      <span className="badge-primary">Project #{project.id}</span>
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
