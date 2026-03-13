import { useFormik } from 'formik'; 
import * as yup from 'yup'; // Validation

function TaskForm({ fetchTasks, users }) {
  // Formik setup
  const formik = useFormik({
    initialValues: { title: '', description: '', priority: 'Medium', user_id: '' },
    // Validation here.
    validationSchema: yup.object({
      title: yup.string()
        .required('Required') 
        .min(3, 'Too short')  
        .max(50, 'Too long'), 
      user_id: yup.string().required('Select a user')
    }),
    // Submit form
    onSubmit: (values, { resetForm }) => {
      fetch('/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      }).then(() => {
        fetchTasks(); 
        resetForm(); 
      });
    }
  });

  // note to self, ream more on the below.
  return (
    <div>
      <h2>New Task</h2>
      <form onSubmit={formik.handleSubmit}>
        {/* Title field */}
        <div>
          <input name="title" placeholder="Title" onChange={formik.handleChange} value={formik.values.title} />
          {formik.errors.title && <div className="error">{formik.errors.title}</div>}
        </div>
        
        {/* Description field */}
        <div>
          <textarea name="description" placeholder="Description" onChange={formik.handleChange} value={formik.values.description} />
        </div>
        
        {/* Priority dropdown */}
        <div>
          <select name="priority" onChange={formik.handleChange} value={formik.values.priority}>
            <option>Low</option><option>Medium</option><option>High</option>
          </select>
        </div>
        
        {/* User dropdown */}
        <div>
          <select name="user_id" onChange={formik.handleChange} value={formik.values.user_id}>
            <option value="">Select User</option>
            {users.map(u => <option key={u.id} value={u.id}>{u.username}</option>)}
          </select>
          {formik.errors.user_id && <div className="error">{formik.errors.user_id}</div>}
        </div>
        
        <button type="submit">Create Task</button>
      </form>
    </div>
  );
}

export default TaskForm;