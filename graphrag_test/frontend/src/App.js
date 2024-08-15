import './App.css';
import { Link, Route, Routes } from "react-router-dom"
import { Home } from "./components/Home"
import { AgentForm } from "./components/AgentForm"
import { CrewForm } from "./components/CrewForm"
import { RunCrew } from './RunCrew';



function App() {
  return (
    <>
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/agents">Agents</Link></li>
        <li><Link to="/crews">Crews</Link></li>
        <li><Link to="/runcrew">Task running</Link></li>
      </ul>
    </nav>
    <Routes>
      <Route path="/" element={<Home/>} />
      <Route path="/agents" element={<AgentForm/>} />
      <Route path="/crews" element={<CrewForm/>} />
      <Route path="/runcrew" element={<RunCrew/>} />
    </Routes>
    </>
  )
}

export default App;
