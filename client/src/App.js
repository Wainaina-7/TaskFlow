// imports here
import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import TaskList from "./components/TaskList";
import UserList from "./components/UserList";
import AssignmentList from "./components/AssignmentList";
import TaskForm from "./components/forms/TaskForm";
import UserForm from "./components/forms/UserForm";
import AssignmentForm from "./components/forms/AssignmentForm";
import "./index.css";

function App() {
  // State for storing data from backend
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [assignments, setAssignments] = useState([]);

  // Fetch all data when app starts
  useEffect(() => {
    fetchTasks();
    fetchUsers();
    fetchAssignments();
  }, []);

  // Fetching from API functions
  const fetchTasks = () => {
    fetch("/tasks")
      .then(res => res.json())
      .then(data => setTasks(data));
  };
  const fetchUsers = () => {
    fetch("/users")
      .then(res => res.json())
      .then(data => setUsers(data));
  };
  const fetchAssignments = () => {
    fetch("/assignments")
      .then(res => res.json())
      .then(data => setAssignments(data));
  };

  return (
    <BrowserRouter>
      {/* nav bar */}
      <nav style={{ padding: "10px", background: "#333", display: "flex", gap: "15px" }}>
        <NavLink to="/" style={{ color: "white" }}>Tasks</NavLink>
        <NavLink to="/users" style={{ color: "white" }}>Users</NavLink>
        <NavLink to="/assignments" style={{ color: "white" }}>Assignments</NavLink>
        <NavLink to="/tasks/new" style={{ color: "white" }}>+ Task</NavLink>
        <NavLink to="/users/new" style={{ color: "white" }}>+ User</NavLink>
        <NavLink to="/assignments/new" style={{ color: "white" }}>+ Assignment</NavLink>
      </nav>

      {/* routes */}
      <div style={{ padding: "20px" }}>
        <Routes>
          <Route path="/" element={<TaskList tasks={tasks} fetchTasks={fetchTasks} />} />
          <Route path="/users" element={<UserList users={users} fetchUsers={fetchUsers} />} />
          <Route path="/assignments" element={
            <AssignmentList 
              assignments={assignments} 
              fetchAssignments={fetchAssignments}
              users={users}
              tasks={tasks}
            />
          } />
          <Route path="/tasks/new" element={<TaskForm fetchTasks={fetchTasks} users={users} />} />
          <Route path="/users/new" element={<UserForm fetchUsers={fetchUsers} />} />
          <Route path="/assignments/new" element={
            <AssignmentForm 
              fetchAssignments={fetchAssignments}
              users={users}
              tasks={tasks}
            />
          } />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;