
import { useEffect, useState } from 'react'
import API from '../services/api'

function TasksPage() {
  const [tasks, setTasks] = useState([])
  const [workflows, setWorkflows] = useState([])
  const [loading, setLoading] = useState(true)

  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState('medium')
  const [workflowId, setWorkflowId] = useState('')

  const fetchTasks = () => {
    API.get('/tasks/')
      .then((response) => setTasks(response.data))
      .catch((error) => console.log('Tasks fetch failed:', error))
      .finally(() => setLoading(false))
  }

  const fetchWorkflows = () => {
    API.get('/workflows/')
      .then((response) => {
        setWorkflows(response.data)

        if (response.data.length > 0) {
          setWorkflowId(String(response.data[0].id))
        }
      })
      .catch((error) => console.log('Workflows fetch failed:', error))
  }

  useEffect(() => {
    fetchTasks()
    fetchWorkflows()
  }, [])

  const handleCreateTask = async (e) => {
    e.preventDefault()

    if (!workflowId) {
      alert('Please create a workflow first!')
      return
    }

    try {
      await API.post('/tasks/', {
        title,
        description,
        priority,
        workflow_id: Number(workflowId)
      })

      alert('Task created successfully!')
      setTitle('')
      setDescription('')
      setPriority('medium')
      fetchTasks()
    } catch (error) {
      alert(error.response?.data?.detail || 'Task creation failed')
    }
  }

  const handleUpdateTask = async (task) => {
    const newTitle = prompt('Enter new task title:', task.title)

    if (!newTitle || !newTitle.trim()) return

    try {
      await API.put(`/tasks/${task.id}`, {
        title: newTitle.trim()
      })

      alert('Task updated successfully!')
      fetchTasks()
    } catch (error) {
      alert(error.response?.data?.detail || 'Task update failed')
    }
  }

  const handleDeleteTask = async (task) => {
    const confirmDelete = window.confirm(
      `Are you sure you want to delete ${task.title}?`
    )

    if (!confirmDelete) return

    try {
      await API.delete(`/tasks/${task.id}`)
      alert('Task deleted successfully!')
      fetchTasks()
    } catch (error) {
      alert(error.response?.data?.detail || 'Task deletion failed')
    }
  }

  return (
    <div className="page-content">
      <h1>Task Management</h1>
      <p>Create, manage and track your tasks.</p>

      <h2>Create New Task</h2>

      {workflows.length === 0 ? (
        <p>Please create a workflow before creating a task.</p>
      ) : (
        <form onSubmit={handleCreateTask}>
          <input
            type="text"
            placeholder="Task Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            minLength={2}
            maxLength={150}
            required
          />

          <br /><br />

          <textarea
            placeholder="Task Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          <br /><br />

          <label>Priority: </label>

          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>

          <br /><br />

          <label>Workflow: </label>

          <select
            value={workflowId}
            onChange={(e) => setWorkflowId(e.target.value)}
            required
          >
            {workflows.map((workflow) => (
              <option key={workflow.id} value={workflow.id}>
                {workflow.name}
              </option>
            ))}
          </select>

          <br /><br />

          <button type="submit">Create Task</button>
        </form>
      )}

      <h2>Tasks List</h2>

      {loading ? (
        <p>Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <table className="tasks-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Description</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Workflow ID</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {tasks.map((task) => (
              <tr key={task.id}>
                <td>{task.id}</td>
                <td>{task.title}</td>
                <td>{task.description || '-'}</td>
                <td>{task.priority}</td>
                <td>{task.status}</td>
                <td>{task.workflow_id}</td>
                <td>
                  <button onClick={() => handleUpdateTask(task)}>
                    Edit
                  </button>

                  {' '}

                  <button onClick={() => handleDeleteTask(task)}>
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

export default TasksPage
