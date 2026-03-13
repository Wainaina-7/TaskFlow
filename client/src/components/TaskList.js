import { useState } from 'react'; 

function TaskList({ tasks, fetchTasks }) {
  // tracking task being edited
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({ title: '', description: '', priority: 'Medium' });

  // DELETE task 
  const handleDelete = (id) => {
    fetch(`/tasks/${id}`, { method: 'DELETE' })
      .then(() => fetchTasks()); // Refresh list
  };

  // EDIT task
  const startEdit = (task) => {
    setEditingId(task.id);
    setEditForm({
      title: task.title,
      description: task.description || '',
      priority: task.priority || 'Medium'
    });
  };

  // Handle form field changes
  const handleEditChange = (e) => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  // UPDATE task 
  const handleEditSubmit = (id) => {
    fetch(`/tasks/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editForm)
    }).then(() => {
      setEditingId(null); 
      fetchTasks(); // Refresh
    });
  };

  return (
    <div>
      <h2>Tasks</h2>
      {tasks.map(task => (
        <div key={task.id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
          {editingId === task.id ? (
            // form here
            <>
              <input name="title" value={editForm.title} onChange={handleEditChange} />
              <textarea name="description" value={editForm.description} onChange={handleEditChange} />
              <select name="priority" value={editForm.priority} onChange={handleEditChange}>
                <option>Low</option><option>Medium</option><option>High</option>
              </select>
              <button onClick={() => handleEditSubmit(task.id)}>Save</button>
              <button onClick={() => setEditingId(null)}>Cancel</button>
            </>
          ) : (
            // for view mode
            <>
              <h3>{task.title}</h3>
              <p>{task.description}</p>
              <p>Priority: {task.priority} | Status: {task.completed ? '✅' : '⏳'}</p>
              <button onClick={() => startEdit(task)}>Edit</button>
              <button onClick={() => handleDelete(task.id)}>Delete</button>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

export default TaskList;