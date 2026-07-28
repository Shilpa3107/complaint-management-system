import { useState, useRef, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import axios from 'axios'
import { messageSent, fileAttached, responseReceived, responseFailed } from '../features/chatSlice'
import {
  requestStarted,
  requestFailed,
  newComplaintApplied,
  editApplied,
  aiMetaUpdated,
} from '../features/complaintSlice'
import './AICopilotPanel.css'


const API_BASE = 'http://127.0.0.1:8000'

function AICopilotPanel() {
  const dispatch = useDispatch()
  const messages = useSelector((state) => state.chat.messages)
  const chatStatus = useSelector((state) => state.chat.status)
  const form = useSelector((state) => state.complaint.form)
  const fileInputRef = useRef(null)
  const [chatInput, setChatInput] = useState('')
  const hasComplaintLoaded = useSelector((state) => state.complaint.hasComplaintLoaded)
  const messagesEndRef = useRef(null)

useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
}, [messages, chatStatus])

  const callUnifiedCopilot = async ({ userMessage, file }) => {
    dispatch(requestStarted())

    const formData = new FormData()
    formData.append('user_message', userMessage || '')
    formData.append('current_complaint', hasComplaintLoaded ? JSON.stringify(form) : '{}')
    formData.append(
      'chat_history',
      JSON.stringify(messages.map((m) => ({ role: m.role, content: m.content })))
    )
    if (file) formData.append('file', file)

    try {
      const res = await axios.post(`${API_BASE}/copilot-unified/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      const data = res.data

      if (data.intent === 'new_complaint' && data.extracted) {
        dispatch(newComplaintApplied(data.extracted))
        dispatch(aiMetaUpdated(data))
      } else if (data.intent === 'edit' && data.field_edits) {
        dispatch(editApplied(data.field_edits))
      }

      dispatch(responseReceived(data.assistant_message))
    } catch (err) {
      console.error('Copilot request failed:', err)
      dispatch(requestFailed())
      dispatch(responseFailed('I ran into an error processing that. Please check the backend is running and try again.'))
    }
  }

  const handleSendChat = () => {
    if (!chatInput.trim() || chatStatus === 'loading') return
    const text = chatInput
    setChatInput('')
    dispatch(messageSent(text))
    callUnifiedCopilot({ userMessage: text })
  }

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (!file) return
    dispatch(fileAttached(file.name))
    callUnifiedCopilot({ userMessage: `Uploaded document: ${file.name}`, file })
    e.target.value = '' // allow re-selecting the same file later
  }

  return (
    <div className="copilot-panel">
      <div className="copilot-header">
        <div className="copilot-title">
          <span className="sparkle">✦</span>
          <h2>AIVOA Copilot</h2>
        </div>
        <span className="beta-badge">BETA</span>
      </div>
      <p className="copilot-subtitle">Drop complaint files or paste text below.</p>

      <div className="chat-messages">
  {messages.map((msg, i) => (
    <div key={i} className={`chat-bubble ${msg.role}`}>
      {msg.role === 'assistant' && <span className="bot-icon">🤖</span>}
      <span>{msg.content}</span>
    </div>
  ))}
  {chatStatus === 'loading' && (
    <div className="chat-bubble assistant loading">
      <span className="bot-icon">⚡</span>
      <span>Thinking...</span>
    </div>
  )}
  <div ref={messagesEndRef} />
</div>

      <div className="chat-input-row">
        <button
          className="attach-btn"
          onClick={() => fileInputRef.current.click()}
          disabled={chatStatus === 'loading'}
          title="Attach a complaint document"
        >
          📎
        </button>
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          accept=".pdf,.docx,.txt,.eml"
          onChange={handleFileSelect}
        />
        <input
          type="text"
          placeholder="Type a message or paste a complaint..."
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSendChat()}
          disabled={chatStatus === 'loading'}
        />
        <button onClick={handleSendChat} disabled={chatStatus === 'loading'}>➤</button>
      </div>
      <p className="disclaimer">AI responses may contain errors. Please verify information.</p>
    </div>
  )
}

export default AICopilotPanel