
import { useEffect, useState } from 'react'
import API from '../services/api'

function ExecutionsPage() {
  const [executions, setExecutions] = useState([])
  const [tasks, setTasks] = useState([])
  const [taskId, setTaskId] = useState('')
  const [loading, setLoading] = useState(true)

  const fetchExecutions = () => {
    API.get('/executions/')
      .then((response) => setExecutions(response.data))
      .catch((error) => console.log('Executions fetch failed:', error))
      .finally(() => setLoading(false))
  }

  const fetchTasks = () => {
    API.get('/tasks/')
      .then((response) => setTasks(response.data))
      .catch((error) => console.log('Tasks fetch failed:', error))
  }

  useEffect(() => {
    fetchExecutions()
    fetchTasks()
  }, [])

  const handleStartExecution = async (e) => {
    e.preventDefault()

    if (!taskId) {
      alert('Please select a task')
      return
    }

    try {
      await API.post('/executions/', {
        task_id: Number(taskId)
      })

      alert('Execution started successfully!')
      fetchExecutions()
    } catch (error) {
      alert(error.response?.data?.detail || 'Execution start failed')
    }
  }

  const handleCompleteExecution = async (execution) => {
    const result = prompt('Enter execution result:')

    if (!result || !result.trim()) return

    try {
      await API.put(
        `/executions/${execution.id}/complete`,
        null,
        { params: { result: result.trim() } }
      )

      alert('Execution completed successfully!')
      fetchExecutions()
    } catch (error) {
      alert(error.response?.data?.detail || 'Execution completion failed')
    }
  }

  const handleFailExecution = async (execution) => {
    const errorMessage = prompt('Enter failure reason:')

    if (!errorMessage || !errorMessage.trim()) return

    try {
      await API.put(
        `/executions/${execution.id}/fail`,
        null,
        { params: { error_message: errorMessage.trim() } }
      )

      alert('Execution marked as failed!')
      fetchExecutions()
    } catch (error) {
      alert(error.response?.data?.detail || 'Execution update failed')
    }
  }

  return (
    <div className="page-content">
      <h1>Execution Management</h1>
      <p>Monitor and track your task executions.</p>

      <h2>Start New Execution</h2>

      {tasks.length === 0 ? (
        <p>Please create a task before starting an execution.</p>
      ) : (
        <form onSubmit={handleStartExecution}>
          <label>Select Task: </label>

          <select
            value={taskId}
            onChange={(e) => setTaskId(e.target.value)}
            required
          >
            <option value="">Select a task</option>

            {tasks.map((task) => (
              <option key={task.id} value={task.id}>
                {task.title}
              </option>
            ))}
          </select>

          <br /><br />

          <button type="submit">Start Execution</button>
        </form>
      )}

      <h2>Executions List</h2>

      {loading ? (
        <p>Loading executions...</p>
      ) : executions.length === 0 ? (
        <p>No executions found.</p>
      ) : (
        <table className="executions-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Task ID</th>
              <th>Status</th>
              <th>Result</th>
              <th>Error Message</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {executions.map((execution) => (
              <tr key={execution.id}>
                <td>{execution.id}</td>
                <td>{execution.task_id}</td>
                <td>{execution.status}</td>
                <td>{execution.result || '-'}</td>
                <td>{execution.error_message || '-'}</td>

                <td>
                  {execution.status === 'running' ? (
                    <>
                      <button
                        onClick={() => handleCompleteExecution(execution)}
                      >
                        Complete
                      </button>

                      {' '}

                      <button
                        onClick={() => handleFailExecution(execution)}
                      >
                        Fail
                      </button>
                    </>
                  ) : (
                    <span>-</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default ExecutionsPage
