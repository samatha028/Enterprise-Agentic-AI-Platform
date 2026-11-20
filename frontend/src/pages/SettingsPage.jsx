
import { useEffect, useState } from 'react'
import API from '../services/api'

function SettingsPage() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState('')

  useEffect(() => {
    API.get('/users/profile')
      .then((response) => setProfile(response.data))
      .catch((error) => console.log('Profile fetch failed:', error))
      .finally(() => setLoading(false))
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    window.location.href = '/login'
  }

  return (
    <div className="page-content">
      <h1>Platform Settings</h1>
      <p>Manage your platform configuration and preferences.</p>

      <h2>Profile Information</h2>

      {loading ? (
        <p>Loading profile...</p>
      ) : profile ? (
        <div>
          <p><strong>Name:</strong> {profile.full_name}</p>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>User ID:</strong> {profile.id}</p>
        </div>
      ) : (
        <p>Unable to load profile information.</p>
      )}

      <h2>Platform Preferences</h2>
      <p>Platform: Enterprise Agentic AI Platform</p>
      <p>Backend: Connected</p>

      <h2>Account Settings</h2>
      <button onClick={handleLogout}>Logout</button>
      {message && <p>{message}</p>}
    </div>
  )
}

export default SettingsPage
