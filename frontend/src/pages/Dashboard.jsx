import { useEffect, useState } from 'react'

export default function Dashboard() {
  const [tasks, setTasks] = useState([])

  useEffect(() => {
    fetch('http://localhost:5000/tasks')
      .then((res) => res.json())
      .then((data) => setTasks(data))
      .catch(console.error)
  }, [])

  const totals = tasks.reduce(
    (acc, task) => {
      acc.total++
      if (task.completed) acc.completed++
      return acc
    },
    { total: 0, completed: 0 }
  )

  return (
    <div>
      <h1 className="page-title">Dashboard</h1>
      <div className="card-grid">
        <div className="card">
          <h3>Total Tasks</h3>
          <p className="small-muted">{totals.total}</p>
        </div>
        <div className="card">
          <h3>Completed</h3>
          <p className="small-muted">{totals.completed}</p>
        </div>
        <div className="card">
          <h3>Pending</h3>
          <p className="small-muted">{totals.total - totals.completed}</p>
        </div>
      </div>
      <div className="card">
        <h2>Latest Tasks</h2>
        <ul>
          {tasks.slice(0, 5).map((t) => (
            <li className="task-item" key={t.id}>
              <span>{t.title}</span>
              <span className="small-muted">{t.status}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
