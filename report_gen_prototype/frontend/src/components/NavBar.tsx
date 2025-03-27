import React, { useState, useEffect} from 'react';
interface NavbarProps {
  handleLogout: () => void;
}
const NavBar: React.FC<NavbarProps> = ({ handleLogout }) => {


    return <nav className="navbar navbar-expand-lg bg-body-tertiary">
    <div className="container-fluid">
      <a className="navbar-brand" href="#">Navbar</a>
      <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarSupportedContent">
        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
          <li className="nav-item">
            <a className="nav-link active" aria-current="page" href="/">Home</a>
          </li>
          <li className="nav-item">
          <a className="nav-link active" aria-current="page" href="/Agents/">Agents</a>
          </li>
          <li className="nav-item">
          <a className="nav-link active" aria-current="page" href="/Leads/">Leads</a>
          </li>
          <li className="nav-item">
          <a className="nav-link active" aria-current="page" href="/Papers/">Papers</a>
          </li>
        </ul>
        <button onClick={handleLogout} style={{ background: "red", color: "white", padding: "5px 10px", border: "none", cursor: "pointer" }}>
                Logout
          </button>
      </div>
    </div>
  </nav>;
}

export default NavBar;