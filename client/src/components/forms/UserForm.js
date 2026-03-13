import { useFormik } from 'formik';
import * as yup from 'yup';

function UserForm({ fetchUsers }) {
  // usual Formik setup and validation
  const formik = useFormik({
    initialValues: { username: '', email: '', password: 'password' },
    validationSchema: yup.object({
      username: yup.string()
        .required('Required')
        .min(3, 'Too short')
        .max(20, 'Too long'),
      email: yup.string()
        .required('Required')
        .email('Invalid email') 
    }),
    // Submit
    onSubmit: (values, { resetForm }) => {
      fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      }).then(() => {
        fetchUsers(); 
        resetForm(); 
      });
    }
  });

  return (
    <div>
      <h2>New User</h2>
      <form onSubmit={formik.handleSubmit}>
        {/* Username field */}
        <div>
          <input name="username" placeholder="Username" onChange={formik.handleChange} value={formik.values.username} />
          {formik.errors.username && <div className="error">{formik.errors.username}</div>}
        </div>
        
        {/* Email field */}
        <div>
          <input name="email" placeholder="Email" onChange={formik.handleChange} value={formik.values.email} />
          {formik.errors.email && <div className="error">{formik.errors.email}</div>}
        </div>
        
        <button type="submit">Create User</button>
      </form>
    </div>
  );
}

export default UserForm;