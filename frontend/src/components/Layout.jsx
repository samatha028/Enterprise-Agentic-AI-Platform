
import { NavLink, Outlet } from 'react-router-dom'

function Layout() {
  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>Enterprise AI</h2>

        <nav className="sidebar-nav">
          <NavLink to="/" end className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Dashboard
          </NavLink>

          <NavLink to="/agents" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Agents
          </NavLink>

          <NavLink to="/workflows" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Workflows
          </NavLink>

          <NavLink to="/tasks" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Tasks
          </NavLink>

          <NavLink to="/executions" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Executions
          </NavLink>

          <NavLink to="/settings" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Settings
          </NavLink>
        </nav>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
