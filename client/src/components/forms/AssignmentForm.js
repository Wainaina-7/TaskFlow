import { useFormik } from 'formik';
import * as yup from 'yup';

function AssignmentForm({ fetchAssignments, users, tasks }) {
  // Formik setup and validation AGAIN
  const formik = useFormik({
    initialValues: { user_id: '', task_id: '', notes: '' },
    validationSchema: yup.object({
      user_id: yup.string().required('Select user'),
      task_id: yup.string().required('Select task')
    }),
    // Submit
    onSubmit: (values, { resetForm }) => {
      fetch('/assignments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      }).then(() => {
        fetchAssignments(); 
        resetForm(); 
      });
    }
  });

  return (
    <div>
      <h2>Assign Task to User</h2>
      <form onSubmit={formik.handleSubmit}>
        {/* User dropdown */}
        <div>
          <select name="user_id" onChange={formik.handleChange} value={formik.values.user_id}>
            <option value="">Select User</option>
            {users.map(u => <option key={u.id} value={u.id}>{u.username}</option>)}
          </select>
          {formik.errors.user_id && <div className="error">{formik.errors.user_id}</div>}
        </div>
        
        {/* Task dropdown */}
        <div>
          <select name="task_id" onChange={formik.handleChange} value={formik.values.task_id}>
            <option value="">Select Task</option>
            {tasks.map(t => <option key={t.id} value={t.id}>{t.title}</option>)}
          </select>
          {formik.errors.task_id && <div className="error">{formik.errors.task_id}</div>}
        </div>
        
        {/* Notes field */}
        <div>
          <textarea name="notes" placeholder="Notes (optional)" onChange={formik.handleChange} value={formik.values.notes} />
        </div>
        
        <button type="submit">Create Assignment</button>
      </form>
    </div>
  );
}

export default AssignmentForm;