function UserList({ users, fetchUsers }) {
  // READ action diplaying the usrs.
  return (
    <div>
      <h2>Users</h2>
      {users.map(user => (
        <div key={user.id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
          <h3>{user.username}</h3>
          <p>Email: {user.email}</p>
        </div>
      ))}
    </div>
  );
}

export default UserList;