import { useEffect, useState } from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'

const projectSchema = Yup.object().shape({
  title: Yup.string().required('Title required').min(3, 'Min 3 chars'),
  description: Yup.string().optional(),
})

export default function Projects() {
  const [projects, setProjects] = useState([])
  const [message, setMessage] = useState(null)

  const loadProjects = () => {
    fetch('http://localhost:5000/projects')
      .then((res) => res.json())
      .then(setProjects)
      .catch((err) => {
        console.error(err)
        setMessage('Unable to load projects')
      })
  }

  useEffect(() => {
    loadProjects()
  }, [])

  return (
    <div>
      <h1 className="page-title">Projects</h1>
      <div className="form-container">
        {message && <p style={{ marginBottom: '0.75rem', color: message.startsWith('Unable') ? '#c53030' : '#027a48' }}>{message}</p>}
        <Formik
          initialValues={{ title: '', description: '' }}
          validationSchema={projectSchema}
          onSubmit={(values, actions) => {
            fetch('http://localhost:5000/projects', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(values),
            })
              .then((r) => r.json())
              .then(() => {
                loadProjects()
                actions.resetForm()
                setMessage('Project created successfully')
              })
              .catch((err) => {
                console.error(err)
                setMessage('Unable to create project')
              })
              .finally(() => actions.setSubmitting(false))
          }}
        >
          {({ isSubmitting }) => (
            <Form>
              <label>Title</label>
              <Field name="title" />
              <ErrorMessage name="title" component="div" style={{ color: 'red' }} />
              <label>Description</label>
              <Field name="description" />
              <ErrorMessage name="description" component="div" style={{ color: 'red' }} />
              <button type="submit" disabled={isSubmitting}>Create Project</button>
            </Form>
          )}
        </Formik>
      </div>

      <div className="card">
        <h2>All Projects</h2>
        <ul>
          {projects.map((p) => (
            <li className="project-item" key={p.id}>
              <span>{p.title}</span>
              <span className="small-muted">{p.description || 'No description'}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
