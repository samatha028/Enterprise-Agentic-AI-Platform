import { useEffect, useState } from 'react'
import Dashboard from '../components/Dashboard'
import API from '../services/api'

function DashboardPage() {
  const [agentCount, setAgentCount] = useState(0)
  const [workflowCount, setWorkflowCount] = useState(0)
  const [taskCount, setTaskCount] = useState(0)
  const [executionCount, setExecutionCount] = useState(0)
  const [backendStatus, setBackendStatus] = useState('Checking...')

  useEffect(() => {
    API.get('/')
      .then((response) => setBackendStatus(response.data.status))
      .catch(() => setBackendStatus('Backend connection failed'))

    API.get('/agents/')
      .then((response) => setAgentCount(response.data.length))
      .catch((error) => console.log('Agents fetch failed:', error))

    API.get('/workflows/')
      .then((response) => setWorkflowCount(response.data.length))
      .catch((error) => console.log('Workflows fetch failed:', error))

    API.get('/tasks/')
      .then((response) => setTaskCount(response.data.length))
      .catch((error) => console.log('Tasks fetch failed:', error))

    API.get('/executions/')
      .then((response) => setExecutionCount(response.data.length))
      .catch((error) => console.log('Executions fetch failed:', error))
  }, [])

  return (
    <>
      <Dashboard
        agentCount={agentCount}
        workflowCount={workflowCount}
        taskCount={taskCount}
        executionCount={executionCount}
      />
      <p>Backend Status: {backendStatus}</p>
    </>
  )
}

export default DashboardPage