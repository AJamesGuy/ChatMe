import React, { useEffect, useState } from 'react'
import { ChatroomAPI } from '../services/api'

function Chatrooms() {
  const [chatrooms, setChatrooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchChatrooms = async () => {
      try {
        const data = await ChatroomAPI.listChatrooms()
        setChatrooms(data.chat_rooms || [])
      } catch (err) {
        setError(err?.message || 'Failed to load chatrooms.')
      } finally {
        setLoading(false)
      }
    }

    fetchChatrooms()
  }, [])

  return (
    <div>
      <h2>Chatrooms</h2>

      {loading && <p>Loading chatrooms...</p>}
      {error && <p>{error}</p>}

      {!loading && !error && chatrooms.length === 0 && (
        <p>No chatrooms found.</p>
      )}

      {!loading && !error && chatrooms.length > 0 && (
        <ul>
          {chatrooms.map((room) => (
            <li key={room.id}>
              <strong>{room.name}</strong> - {room.access_code}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default Chatrooms