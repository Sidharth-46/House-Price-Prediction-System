import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { HiMenuAlt3, HiX } from 'react-icons/hi'
import '../App.css'

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  const links = [
    { to: '/', label: 'Home' },
    { to: '/predict', label: 'Predict' },
    { to: '/dashboard', label: 'Dashboard' },
    { to: '/about', label: 'About' },
  ]

  return (
    <nav className="navbar">
      <div className="container navbar-inner">
        <Link to="/" className="navbar-logo">
          <span className="navbar-logo-icon">🏠</span>
          <span>Price<span className="text-gradient">Vision</span></span>
        </Link>

        <button
          className="navbar-mobile-btn"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle navigation"
        >
          {isOpen ? <HiX /> : <HiMenuAlt3 />}
        </button>

        <div className={`navbar-links ${isOpen ? 'open' : ''}`}>
          {links.map(link => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              onClick={() => setIsOpen(false)}
              end={link.to === '/'}
            >
              {link.label}
            </NavLink>
          ))}
          <Link to="/predict" className="btn btn-primary" style={{ marginLeft: '0.5rem', padding: '0.5rem 1.25rem', fontSize: '0.85rem' }}>
            Get Estimate
          </Link>
        </div>
      </div>
    </nav>
  )
}
