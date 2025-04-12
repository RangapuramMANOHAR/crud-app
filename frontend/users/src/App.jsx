import { useEffect, useState } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ name: '', email: '' });
  const [editingId, setEditingId] = useState(null);

  const getUsers = async () => {
    const res = await fetch('/api/users');
    const data = await res.json();
    setUsers(data);
  };

  useEffect(() => {
    getUsers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const method = editingId ? 'PUT' : 'POST';
    const url = editingId ? `/api/users/${editingId}` : '/api/users';

    await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });

    setEditingId(null);
    setForm({ name: '', email: '' });
    getUsers();
  };

  const handleEdit = (user) => {
    setForm({ name: user.name, email: user.email });
    setEditingId(user.id);
  };

  const handleDelete = async (id) => {
    await fetch(`/api/users/${id}`, { method: 'DELETE' });
    getUsers();
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">CRUD Application(WEB DEVELOPMENT)</h2>

      <form className="mb-4" onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Name</label>
          <input
            className="form-control"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
          />
        </div>
        <div className="mb-3">
          <label>Email address</label>
          <input
            className="form-control"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          {editingId ? 'Update User' : 'Add User'}
        </button>
      </form>

      <table className="table table-striped table-bordered">
        <thead className="table-dark">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th style={{ width: '150px' }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.name}</td>
              <td>{u.email}</td>
              <td>
                <button
                  className="btn btn-sm btn-primary me-2"
                  onClick={() => handleEdit(u)}
                >
                  Edit
                </button>
                <button
                  className="btn btn-sm btn-danger"
                  onClick={() => handleDelete(u.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
