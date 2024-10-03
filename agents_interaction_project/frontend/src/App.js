import './App.css';
import { Link, Route, Routes } from "react-router-dom"
import { ConvoDisplay } from "./components/ConvoDisplay"
import { AllConvoLogs } from "./components/AllConvoLogs"
import { SpecificConvo } from './components/SpecificConvo';
import { AllStoredPapers } from './components/AllStoredPapers';
import { SpecificPaper } from './components/SpecificPaper';

function App() {
  return (
    <>
    <nav>
      <ul>
        <li><Link to="/dailyconvodisplay">Daily ConvoDisplay</Link></li>
        <li><Link to="/allconvodisplay">All ConvoDisplay</Link></li>
        <li><Link to= "/allstoredpapers">All Stored Papers</Link></li>
      </ul>
    </nav>
    <Routes>
      <Route path="/dailyconvodisplay" element={<ConvoDisplay/>} />
      <Route path="/allconvodisplay" element={<AllConvoLogs/>} />
      <Route path="/allstoredpapers" element={<AllStoredPapers/>} />
      <Route path="/convolog/:date" element={<SpecificConvo/>} />
      <Route path="/storedpaper/:doi" element={<SpecificPaper/>} />    
    </Routes>
    </>
  )
}

export default App;
