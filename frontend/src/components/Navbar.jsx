import { NavLink } from 'react-router-dom'

const activeStyle = { fontWeight: 'bold', textDecoration: 'underline' }

export default function Navbar() {
  return (
    <nav style={{ background: '#282c34', padding: '0.75rem' }}>
      <NavLink to="/" style={({ isActive }) => (isActive ? activeStyle : { color: '#ddd', marginRight: '1rem' })}>
        Dashboard
      </NavLink>
      <NavLink to="/projects" style={({ isActive }) => (isActive ? activeStyle : { color: '#ddd', marginRight: '1rem' })}>
        Projects
      </NavLink>
      <NavLink to="/tasks" style={({ isActive }) => (isActive ? activeStyle : { color: '#ddd', marginRight: '1rem' })}>
        Tasks
      </NavLink>
      <NavLink to="/team" style={({ isActive }) => (isActive ? activeStyle : { color: '#ddd', marginRight: '1rem' })}>
        Team
      </NavLink>
    </nav>
  )
}
