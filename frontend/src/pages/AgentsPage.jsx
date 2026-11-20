
import { useEffect, useState } from 'react'
import API from '../services/api'

function AgentsPage() {
  const [agents, setAgents] = useState([])
  const [loading, setLoading] = useState(true)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [agentType, setAgentType] = useState('support')

  const fetchAgents = () => {
    API.get('/agents/')
      .then((response) => setAgents(response.data))
      .catch((error) => console.log('Agents fetch failed:', error))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchAgents()
  }, [])

  const handleCreateAgent = async (e) => {
    e.preventDefault()

    try {
      await API.post('/agents/', {
        name,
        description,
        agent_type: agentType
      })

      alert('Agent created successfully!')
      setName('')
      setDescription('')
      setAgentType('support')
      fetchAgents()
    } catch (error) {
      alert(error.response?.data?.detail || 'Agent creation failed')
    }
  }

  const handleUpdateAgent = async (agent) => {
    const newName = prompt('Enter new agent name:', agent.name)

    if (!newName || !newName.trim()) return

    try {
      await API.put(`/agents/${agent.id}`, {
        name: newName.trim(),
        description: agent.description,
        agent_type: agent.agent_type
      })

      alert('Agent updated successfully!')
      fetchAgents()
    } catch (error) {
      alert(error.response?.data?.detail || 'Agent update failed')
    }
  }

  const handleDeleteAgent = async (agent) => {
    const confirmDelete = window.confirm(
      `Are you sure you want to delete ${agent.name}?`
    )

    if (!confirmDelete) return

    try {
      await API.delete(`/agents/${agent.id}`)
      alert('Agent deleted successfully!')
      fetchAgents()
    } catch (error) {
      alert(error.response?.data?.detail || 'Agent deletion failed')
    }
  }

  return (
    <div className="page-content">
      <h1>Agent Management</h1>
      <p>Create, manage and monitor your AI agents.</p>

      <h2>Create New Agent</h2>

      <form onSubmit={handleCreateAgent}>
        <input
          type="text"
          placeholder="Agent Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <br /><br />

        <textarea
          placeholder="Agent Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />

        <br /><br />

        <select
          value={agentType}
          onChange={(e) => setAgentType(e.target.value)}
        >
          <option value="support">Support</option>
          <option value="automation">Automation</option>
          <option value="assistant">Assistant</option>
        </select>

        <br /><br />

        <button type="submit">Create Agent</button>
      </form>

      <h2>Agents List</h2>

      {loading ? (
        <p>Loading agents...</p>
      ) : agents.length === 0 ? (
        <p>No agents found.</p>
      ) : (
        <table className="agents-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Type</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {agents.map((agent) => (
              <tr key={agent.id}>
                <td>{agent.id}</td>
                <td>{agent.name}</td>
                <td>{agent.description}</td>
                <td>{agent.agent_type}</td>
                <td>{agent.status}</td>
                <td>
                  <button onClick={() => handleUpdateAgent(agent)}>
                    Edit
                  </button>

                  {' '}

                  <button onClick={() => handleDeleteAgent(agent)}>
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

export default AgentsPage
