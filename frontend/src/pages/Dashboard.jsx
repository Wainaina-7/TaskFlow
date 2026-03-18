import { useEffect, useState } from 'react'
import { TrendingUp, CheckCircle2, Clock, AlertCircle } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

export default function Dashboard() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE}/tasks`)
      .then((res) => res.json())
      .then((data) => {
        setTasks(data)
        setError(null)
      })
      .catch((err) => {
        console.error(err)
        setError('Failed to load tasks')
      })
      .finally(() => setLoading(false))
  }, [])

  const totals = tasks.reduce(
    (acc, task) => {
      acc.total++
      if (task.completed) acc.completed++
      return acc
    },
    { total: 0, completed: 0 }
  )

  const stats = [
    {
      label: 'Total Tasks',
      value: totals.total,
      icon: TrendingUp,
      color: 'from-blue-500 to-blue-600',
      bg: 'bg-blue-50',
    },
    {
      label: 'Completed',
      value: totals.completed,
      icon: CheckCircle2,
      color: 'from-green-500 to-green-600',
      bg: 'bg-green-50',
    },
    {
      label: 'Pending',
      value: totals.total - totals.completed,
      icon: Clock,
      color: 'from-orange-500 to-orange-600',
      bg: 'bg-orange-50',
    },
  ]

  return (
    <div>
      <div className="mb-8">
        <h1 className="page-title mb-2">Welcome Back!</h1>
        <p className="text-slate-600">Here's your task overview for today</p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
          <AlertCircle size={20} className="text-red-600" />
          <span className="text-red-800">{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.label} className={`card ${stat.bg} border-l-4 border-l-primary-600`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 mb-1">{stat.label}</p>
                  <p className="text-3xl font-bold text-slate-900">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-lg bg-gradient-to-br ${stat.color}`}>
                  <Icon size={24} className="text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-slate-900">Latest Tasks</h2>
          {tasks.length > 5 && (
            <span className="badge-primary">+{tasks.length - 5} more</span>
          )}
        </div>
        {loading ? (
          <div className="py-8 text-center text-slate-500">Loading tasks...</div>
        ) : tasks.length === 0 ? (
          <div className="py-8 text-center text-slate-500">No tasks yet. Create one to get started!</div>
        ) : (
          <div className="space-y-3">
            {tasks.slice(0, 5).map((task) => (
              <div
                key={task.id}
                className="flex items-center justify-between p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors"
              >
                <span className="font-medium text-slate-900">{task.title || 'Untitled'}</span>
                <span className="badge badge-primary text-xs">
                  {task.status || 'Pending'}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
