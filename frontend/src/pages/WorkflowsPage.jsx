
import { useEffect, useState } from 'react'
import API from '../services/api'

function WorkflowsPage() {
  const [workflows, setWorkflows] = useState([])
  const [loading, setLoading] = useState(true)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')

  const fetchWorkflows = () => {
    API.get('/workflows/')
      .then((response) => setWorkflows(response.data))
      .catch((error) => console.log('Workflows fetch failed:', error))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchWorkflows()
  }, [])

  const handleCreateWorkflow = async (e) => {
    e.preventDefault()

    try {
      await API.post('/workflows/', {
        name,
        description
      })

      alert('Workflow created successfully!')
      setName('')
      setDescription('')
      fetchWorkflows()
    } catch (error) {
      alert(error.response?.data?.detail || 'Workflow creation failed')
    }
  }

  const handleUpdateWorkflow = async (workflow) => {
    const newName = prompt('Enter new workflow name:', workflow.name)

    if (!newName || !newName.trim()) return

    try {
      await API.put(`/workflows/${workflow.id}`, {
        name: newName.trim()
      })

      alert('Workflow updated successfully!')
      fetchWorkflows()
    } catch (error) {
      alert(error.response?.data?.detail || 'Workflow update failed')
    }
  }

  const handleDeleteWorkflow = async (workflow) => {
    const confirmDelete = window.confirm(
      `Are you sure you want to delete ${workflow.name}?`
    )

    if (!confirmDelete) return

    try {
      await API.delete(`/workflows/${workflow.id}`)
      alert('Workflow deleted successfully!')
      fetchWorkflows()
    } catch (error) {
      alert(error.response?.data?.detail || 'Workflow deletion failed')
    }
  }

  return (
    <div className="page-content">
      <h1>Workflow Management</h1>
      <p>Create, manage and monitor your workflows.</p>

      <h2>Create New Workflow</h2>

      <form onSubmit={handleCreateWorkflow}>
        <input
          type="text"
          placeholder="Workflow Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          minLength={2}
          maxLength={100}
          required
        />

        <br /><br />

        <textarea
          placeholder="Workflow Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <br /><br />

        <button type="submit">Create Workflow</button>
      </form>

      <h2>Workflows List</h2>

      {loading ? (
        <p>Loading workflows...</p>
      ) : workflows.length === 0 ? (
        <p>No workflows found.</p>
      ) : (
        <table className="agents-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {workflows.map((workflow) => (
              <tr key={workflow.id}>
                <td>{workflow.id}</td>
                <td>{workflow.name}</td>
                <td>{workflow.description || '-'}</td>
                <td>{workflow.status}</td>
                <td>
                  <button onClick={() => handleUpdateWorkflow(workflow)}>
                    Edit
                  </button>

                  {' '}

                  <button onClick={() => handleDeleteWorkflow(workflow)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default WorkflowsPage
