function AssignmentList({ assignments, fetchAssignments, users, tasks }) {
  // Toggle completion status
  const handleToggleComplete = (assignment) => {
    fetch(`/assignments/${assignment.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed: !assignment.completed })
    }).then(() => fetchAssignments()); 
  };

  // GET operations.
  const getUserName = (userId) => {
    const user = users.find(u => u.id === userId);
    return user ? user.username : 'Unknown';
  };
  const getTaskTitle = (taskId) => {
    const task = tasks.find(t => t.id === taskId);
    return task ? task.title : 'Unknown';
  };

  return (
    <div>
      <h2>Assignments</h2>
      {assignments.map(a => (
        <div key={a.id} style={{ 
          border: '1px solid #ccc', 
          padding: '10px', 
          margin: '10px 0',
          background: a.completed ? '#e6ffe6' : 'white' 
        }}>
          <p><strong>User:</strong> {getUserName(a.user_id)}</p>
          <p><strong>Task:</strong> {getTaskTitle(a.task_id)}</p>
          <p><strong>Notes:</strong> {a.notes || 'None'}</p>
          <p><strong>Status:</strong> {a.completed ? 'Complete' : 'Pending'}</p>
          <button onClick={() => handleToggleComplete(a)}>
            Mark {a.completed ? 'Incomplete' : 'Complete'}
          </button>
        </div>
      ))}
    </div>
  );
}

export default AssignmentList;