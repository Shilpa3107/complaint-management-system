import ComplaintForm from './components/ComplaintForm'
import AICopilotPanel from './components/AICopilotPanel'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <div className="panel panel-left">
        <ComplaintForm />
      </div>
      <div className="panel panel-right">
        <AICopilotPanel />
      </div>
    </div>
  )
}

export default App