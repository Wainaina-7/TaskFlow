import { useEffect, useState } from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'

const taskSchema = Yup.object().shape({
  title: Yup.string().required('Task title required'),
  user_id: Yup.number().required('User ID required').positive('Must be positive').integer('Must be integer'),
  project_id: Yup.number().required('Project ID required').positive('Must be positive').integer('Must be integer'),
  status: Yup.string().oneOf(['Pending', 'In Progress', 'Done']),
})

export default function Tasks() {
  const [tasks, setTasks] = useState([])
  const [message, setMessage] = useState(null)

  const fetchTasks = () => {
    fetch('http://localhost:5000/tasks')
      .then((res) => res.json())
      .then(setTasks)
      .catch((err) => {
        console.error(err)
        setMessage('Unable to load tasks')
      })
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  const deleteTask = (id) => {
    fetch(`http://localhost:5000/tasks/${id}`, { method: 'DELETE' })
      .then((res) => res.json())
      .then(fetchTasks)
      .catch(console.error)
  }

  return (
    <div>
      <h1 className="page-title">Tasks</h1>
      <div className="form-container">
        {message && <p style={{ marginBottom: '0.75rem', color: message.startsWith('Unable') ? '#c53030' : '#027a48' }}>{message}</p>}
      <Formik
        initialValues={{ title: '', description: '', user_id: '', project_id: '', status: 'Pending' }}
        validationSchema={taskSchema}
        onSubmit={(values, actions) => {
          const payload = {
            ...values,
            user_id: Number(values.user_id),
            project_id: Number(values.project_id)
          }

          fetch('http://localhost:5000/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          })
            .then(() => {
              fetchTasks()
              actions.resetForm()
              setMessage('Task created successfully')
            })
            .catch((err) => {
              console.error(err)
              setMessage('Unable to create task')
            })
            .finally(() => actions.setSubmitting(false))
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <div>
              <label>Title</label>
              <Field name="title" />
              <ErrorMessage name="title" component="div" style={{ color: 'red' }} />
            </div>
            <div>
              <label>Description</label>
              <Field name="description" />
            </div>
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
              <label>Status</label>
              <Field name="status" as="select">
                <option value="Pending">Pending</option>
                <option value="In Progress">In Progress</option>
                <option value="Done">Done</option>
              </Field>
            </div>
            <button type="submit" disabled={isSubmitting}>Create Task</button>
          </Form>
        )}
      </Formik>
      </div>

      <div className="card">
        <h2>Task List</h2>
        <ul>
          {tasks.map((task) => (
            <li className="task-item" key={task.id}>
              <div>
                <strong>{task.title}</strong>
                <p className="small-muted">user {task.user_id} · project {task.project_id}</p>
              </div>
              <div>
                <span className="small-muted">{task.status}</span>
                <button onClick={() => deleteTask(task.id)} style={{ marginLeft: '0.75rem' }}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
