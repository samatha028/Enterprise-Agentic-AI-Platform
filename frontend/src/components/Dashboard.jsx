

function Dashboard({ agentCount, workflowCount, taskCount, executionCount }) {
  return (
    <>
      <h1>Enterprise Agentic AI Platform</h1>
      <p>Intelligent Automation Dashboard</p>

      <section className="dashboard-cards">
        <div className="card">
          <h3>Total Agents</h3>
          <h2>{agentCount}</h2>
        </div>

        <div className="card">
          <h3>Total Workflows</h3>
          <h2>{workflowCount}</h2>
        </div>

        <div className="card">
          <h3>Total Tasks</h3>
          <h2>{taskCount}</h2>
        </div>

        <div className="card">
          <h3>Total Executions</h3>
          <h2>{executionCount}</h2>
        </div>
      </section>

      <section className="recent-activity">
        <h2>Recent Activity</h2>
        <p>No recent activity available.</p>
      </section>
    </>
  )
}

export default Dashboard
