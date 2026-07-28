import { useState, useRef } from 'react'
import './AICopilotPanel.css'

function AICopilotPanel() {
  const [mode, setMode] = useState('upload') // 'upload' | 'paste'
  const [pastedText, setPastedText] = useState('')
  const [chatInput, setChatInput] = useState('')
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Upload a complaint document or paste text above. I will automatically extract the details and populate the form for you.' },
  ])
  const [selectedFileName, setSelectedFileName] = useState(null)
  const fileInputRef = useRef(null)

 const handleFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) {
    setSelectedFileName(file.name)
    console.log('File selected:', file.name)
  }
}

const handleDrop = (e) => {
  e.preventDefault()
  const file = e.dataTransfer.files[0]
  if (file) {
    setSelectedFileName(file.name)
    console.log('File dropped:', file.name)
  }
}

  const handleSendChat = () => {
    if (!chatInput.trim()) return
    setMessages([...messages, { role: 'user', content: chatInput }])
    setChatInput('')
    // Real copilot API call comes in Phase 8
  }

  return (
    <div className="copilot-panel">
      <div className="copilot-header">
        <div className="copilot-title">
          <span className="sparkle">✦</span>
          <h2>AI Complaint Intake Assistant</h2>
        </div>
        <span className="beta-badge">BETA</span>
      </div>

      <div
  className="upload-zone"
  onDragOver={(e) => e.preventDefault()}
  onDrop={handleDrop}
  onClick={() => fileInputRef.current.click()}
>
  <div className="upload-icon">⬆</div>
  {selectedFileName ? (
    <p><strong>{selectedFileName}</strong> selected</p>
  ) : (
    <>
      <p>Drag &amp; drop complaint document here</p>
      <p className="upload-link">or click to browse</p>
    </>
  )}
  <input
    type="file"
    ref={fileInputRef}
    style={{ display: 'none' }}
    accept=".pdf,.docx,.txt,.eml"
    onChange={handleFileSelect}
  />
</div>

      <div className="divider-or">OR</div>

      <button className="paste-text-btn" onClick={() => setMode(mode === 'paste' ? 'upload' : 'paste')}>
        📄 Paste Complaint Text / Email
      </button>

      {mode === 'paste' && (
        <textarea
          className="paste-textarea"
          rows={5}
          placeholder="Paste complaint email or document text here..."
          value={pastedText}
          onChange={(e) => setPastedText(e.target.value)}
        />
      )}

      <div className="supported-formats">
        ℹ️ Supported formats: PDF, DOCX, TXT, EML<br />
        Max file size: 10MB
      </div>

      <div className="chat-section">
        <h4>AI ASSISTANT</h4>
        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-bubble ${msg.role}`}>
              {msg.role === 'assistant' && <span className="bot-icon">🤖</span>}
              <span>{msg.content}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="chat-input-row">
        <input
          type="text"
          placeholder="Ask me anything about this complaint..."
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSendChat()}
        />
        <button onClick={handleSendChat}>➤</button>
      </div>
      <p className="disclaimer">AI responses may contain errors. Please verify information.</p>
    </div>
  )
}

export default AICopilotPanel