import '../App.css'

export default function About() {
  return (
    <div className="about-page page-enter">
      <div className="container">
        <div className="section-header">
          <h2>About <span className="text-gradient">PriceVision</span></h2>
          <p>An end-to-end machine learning system for predicting house prices across India.</p>
        </div>

        <div className="about-grid">
          {/* Project Overview */}
          <div className="glass-card about-card">
            <h3>📋 Project Overview</h3>
            <p>
              PriceVision is a House Price Prediction System built as an MLOps project.
              It uses the <strong>India House Price Prediction</strong> dataset from Kaggle
              (by Ankush Panday) containing 250,000+ property listings across 20 states
              and 42 cities in India.
            </p>
            <br />
            <p>
              The system analyzes 22 property features including location, size, BHK,
              furnished status, amenities, and more to predict property prices using
              <strong> Multiple Linear Regression</strong>.
            </p>
          </div>

          {/* ML Pipeline */}
          <div className="glass-card about-card">
            <h3>🧠 ML Pipeline</h3>
            <ul>
              <li>Data loading & validation (250K rows)</li>
              <li>Feature engineering (amenity extraction)</li>
              <li>Data leakage prevention (Price_per_SqFt dropped)</li>
              <li>Median imputation for numeric features</li>
              <li>One-Hot Encoding for categorical features</li>
              <li>StandardScaler normalization</li>
              <li>80/20 train-test split</li>
              <li>Model evaluation (R², MAE, MSE, RMSE)</li>
            </ul>
          </div>

          {/* Features */}
          <div className="glass-card about-card">
            <h3>✨ Key Features</h3>
            <ul>
              <li>Instant price prediction via REST API</li>
              <li>Dynamic form with cascading state → city dropdowns</li>
              <li>Input validation (frontend + backend)</li>
              <li>Price formatted in ₹ Lakhs and Rupees</li>
              <li>Model comparison dashboard</li>
              <li>Responsive design (mobile + desktop)</li>
              <li>Loading states & error notifications</li>
              <li>Dark mode with glassmorphism UI</li>
            </ul>
          </div>

          {/* SDG Mapping */}
          <div className="glass-card about-card">
            <h3>🌍 SDG Alignment</h3>
            <p style={{ marginBottom: '0.75rem' }}>
              This project aligns with the UN Sustainable Development Goals:
            </p>
            <ul>
              <li><strong>SDG 9</strong>: Industry, Innovation and Infrastructure</li>
              <li><strong>SDG 11</strong>: Sustainable Cities and Communities</li>
            </ul>
            <br />
            <p>
              By providing transparent, data-driven price estimates, PriceVision helps
              buyers, sellers, and urban planners make informed decisions about housing
              affordability and market trends.
            </p>
          </div>
        </div>

        {/* Tech Stack */}
        <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
          <h3 style={{ textAlign: 'center', marginBottom: 'var(--space-lg)' }}>
            🛠️ Tech Stack
          </h3>
          <div className="tech-stack-grid">
            <div className="tech-item">
              <div className="tech-item-icon">🐍</div>
              <div className="tech-item-name">Python</div>
            </div>
            <div className="tech-item">
              <div className="tech-item-icon">🧪</div>
              <div className="tech-item-name">Scikit-Learn</div>
            </div>
            <div className="tech-item">
              <div className="tech-item-icon">🌶️</div>
              <div className="tech-item-name">Flask</div>
            </div>
            <div className="tech-item">
              <div className="tech-item-icon">⚛️</div>
              <div className="tech-item-name">React.js</div>
            </div>
            <div className="tech-item">
              <div className="tech-item-icon">⚡</div>
              <div className="tech-item-name">Vite</div>
            </div>
            <div className="tech-item">
              <div className="tech-item-icon">🐼</div>
              <div className="tech-item-name">Pandas</div>
            </div>
            <div className="tech-item">
              <div className="tech-item-icon">📊</div>
              <div className="tech-item-name">Matplotlib</div>
            </div>
            <div className="tech-item">
              <div className="tech-item-icon">💾</div>
              <div className="tech-item-name">Joblib</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
