import { Link } from 'react-router-dom'
import { HiOutlineChartBar, HiOutlineLocationMarker, HiOutlineLightningBolt } from 'react-icons/hi'
import '../App.css'

export default function Home() {
  return (
    <div className="page-enter">
      {/* ── Hero Section ──────────────────────────────────────────── */}
      <section className="hero">
        <div className="container">
          <div className="hero-badge">
            🇮🇳 Powered by India Housing Data — 250,000+ Properties
          </div>

          <h1>
            Predict House Prices <br />
            Across <span className="text-gradient">India</span> Instantly
          </h1>

          <p className="hero-subtitle">
            MLOps Project by:<br></br>
            Sidharth M K - 24IT0156<br></br>
            Sarvesh R    - 24IT0145
          </p>

          <div className="hero-actions">
            <Link to="/predict" className="btn btn-primary">
              Get Price Estimate →
            </Link>
            <Link to="/dashboard" className="btn btn-outline">
              View Model Metrics
            </Link>
          </div>

          <div className="hero-stats">
            <div className="hero-stat">
              <div className="hero-stat-value">250K+</div>
              <div className="hero-stat-label">Properties Analyzed</div>
            </div>
            <div className="hero-stat">
              <div className="hero-stat-value">42</div>
              <div className="hero-stat-label">Cities Covered</div>
            </div>
            <div className="hero-stat">
              <div className="hero-stat-value">20</div>
              <div className="hero-stat-label">States</div>
            </div>
            <div className="hero-stat">
              <div className="hero-stat-value">22</div>
              <div className="hero-stat-label">Features</div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Features Section ──────────────────────────────────────── */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <h2>How It <span className="text-gradient">Works</span></h2>
            <p>
              Our ML pipeline processes 22 property features to deliver
              price predictions in under a second.
            </p>
          </div>

          <div className="features-grid">
            <div className="glass-card feature-card">
              <div className="feature-icon">
                <HiOutlineLocationMarker />
              </div>
              <h3>Enter Property Details</h3>
              <p>
                Provide details like state, city, BHK, area, furnished status,
                amenities, and more through our intuitive form.
              </p>
            </div>

            <div className="glass-card feature-card">
              <div className="feature-icon">
                <HiOutlineLightningBolt />
              </div>
              <h3>Instant ML Prediction</h3>
              <p>
                Our trained Multiple Linear Regression model processes
                your input through the same preprocessing pipeline
                used during training.
              </p>
            </div>

            <div className="glass-card feature-card">
              <div className="feature-icon">
                <HiOutlineChartBar />
              </div>
              <h3>Get Price Estimate</h3>
              <p>
                Receive the predicted price in Indian Rupees (₹ Lakhs)
                along with model confidence metrics on the dashboard.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
