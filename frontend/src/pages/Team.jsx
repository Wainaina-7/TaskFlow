import { useEffect, useState } from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'

const collaborationSchema = Yup.object().shape({
  user_id: Yup.number().required('User required').positive().integer(),
  project_id: Yup.number().required('Project required').positive().integer(),
  role: Yup.string().required('Role required').min(3),
})

export default function Team() {
  const [collabs, setCollabs] = useState([])
  const [message, setMessage] = useState(null)

  const loadCollabs = () => {
    fetch('http://localhost:5000/collaborations')
      .then((res) => res.json())
      .then(setCollabs)
      .catch((err) => {
        console.error(err)
        setMessage('Unable to load collaborations')
      })
  }

  useEffect(() => {
    loadCollabs()
  }, [])

  return (
    <div>
      <h1 className="page-title">Team / Collaboration</h1>
      <div className="form-container">
        {message && <p style={{ marginBottom: '0.75rem', color: message.startsWith('Unable') ? '#c53030' : '#027a48' }}>{message}</p>}
      <Formik
        initialValues={{ user_id: '', project_id: '', role: 'Developer' }}
        validationSchema={collaborationSchema}
        onSubmit={(values, actions) => {
          const payload = {
            user_id: Number(values.user_id),
            project_id: Number(values.project_id),
            role: values.role,
          }

          fetch('http://localhost:5000/collaborations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          })
            .then(() => {
              loadCollabs()
              actions.resetForm()
              setMessage('Collaboration created successfully')
            })
            .catch((err) => {
              console.error(err)
              setMessage('Unable to create collaboration')
            })
            .finally(() => actions.setSubmitting(false))
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <div>
              <label>User ID</label>
              <Field name="user_id" type="number" />
              <ErrorMessage name="user_id" component="div" style={{ color: 'red' }} />
            </div>
            <div>
              <label>Project ID</label>
              <Field name="project_id" type="number" />
              <ErrorMessage name="project_id" component="div" style={{ color: 'red' }} />
            </div>
            <div>
              <label>Role</label>
              <Field name="role" />
              <ErrorMessage name="role" component="div" style={{ color: 'red' }} />
            </div>
            <button type="submit" disabled={isSubmitting}>Add Collaboration</button>
          </Form>
        )}
      </Formik>
      </div>

      <div className="card">
        <h2>Existing Collaborations</h2>
        <ul>
          {collabs.map((c) => (
            <li className="collab-item" key={c.id}>
              <div>
                <strong>{c.user || 'User ' + c.user_id}</strong>
                <p className="small-muted">{c.project || 'Project ' + c.project_id}</p>
              </div>
              <div className="small-muted">{c.role}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
