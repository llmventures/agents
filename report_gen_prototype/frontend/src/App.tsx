import {BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Agents from './pages/Agents';
import Leads from './pages/Leads';
import LeadPage from './pages/LeadPage';
import Papers from './pages/Papers';
import AgentPage from './pages/AgentPage';
import ReportOutputPage from './pages/ReportOutputPage'
import Login from './pages/Login'
import Logout from './pages/Logout'
import Register from './pages/Register'
import Reports from './pages/Reports'
import ReportPage from './pages/ReportPage'
import "./App.css"

function App() {
  
  return ( 
  <Router>
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='/agents' element = {<Agents />} />
        <Route path='/leads' element = {<Leads />} />
        <Route path='/papers' element = {<Papers />} />
        <Route path='/login' element = {<Login />} />
        <Route path='/register' element = {<Register />} />
        <Route path='/logout' element = {<Logout />} />
        <Route path='/reports' element = {<Reports />} />
        <Route path='/report_output' element = {<ReportOutputPage />} />
        <Route path="/leads/:name" element = {< LeadPage />} />
        <Route path="/agents/:name" element = {< AgentPage />} />
        <Route path="/reports/:name" element = {< ReportPage />} />
      </Routes>
    </Layout>
  </Router>
  );
}

export default App