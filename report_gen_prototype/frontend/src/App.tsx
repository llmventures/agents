import {BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Agents from './pages/Agents';
import Leads from './pages/Leads';
import LeadPage from './pages/LeadPage';
import Papers from './pages/Papers';
import AgentPage from './pages/AgentPage';
import ReportOutputPage from './pages/ReportOutputPage'

function App() {
  
  return ( 
  <Router>
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='/agents' element = {<Agents />} />
        <Route path='/leads' element = {<Leads />} />
        <Route path='/papers' element = {<Papers />} />
        <Route path='/report_output' element = {<ReportOutputPage />} />
        <Route path="/leads/:name" element = {< LeadPage />} />
        <Route path="/agents/:name" element = {< AgentPage />} />
      </Routes>
    </Layout>
  </Router>
  );
}

export default App