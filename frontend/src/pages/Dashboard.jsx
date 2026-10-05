import { useState, useEffect } from 'react'
import { getMetrics } from '../services/api'
import { useToast } from '../context/ToastContext'
import { HiOutlineChartBar, HiOutlineTrendingUp, HiOutlineCalculator, HiOutlineScale } from 'react-icons/hi'
import '../App.css'

export default function Dashboard() {
  const { addToast } = useToast()
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getMetrics()
      .then(data => {
        setMetrics(data)
        setLoading(false)
      })
      .catch(err => {
        addToast('Failed to load metrics. Is the Flask server running?', 'error')
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner spinner-lg" />
        <p>Loading model metrics...</p>
      </div>
    )
  }

  if (!metrics) {
    return (
      <div className="loading-screen">
        <p>⚠️ Could not load metrics. Please verify the API connection.</p>
      </div>
    )
  }

  // Find the primary model metrics dynamically
  const primaryModelName = metrics.primary_model || 'Linear Regression'
  const primary = metrics.results?.find(r => r.model === primaryModelName) || metrics.results?.[0]

  return (
    <div className="dashboard-page page-enter">
      <div className="container">
        <div className="section-header">
          <h2>Model <span className="text-gradient">Dashboard</span></h2>
          <p>Performance metrics for the trained {primaryModelName} model on the test set.</p>
        </div>

        {/* ── Primary Metrics Cards ────────────────────────────────── */}
        <div className="metrics-grid">
          <div className="glass-card metric-card r2">
            <div className="metric-icon"><HiOutlineChartBar size={24} /></div>
            <div className="metric-value">{primary?.r2?.toFixed(4)}</div>
            <div className="metric-label">R² Score</div>
            <div className="metric-sublabel">Variance Explained</div>
          </div>

          <div className="glass-card metric-card mae">
            <div className="metric-icon"><HiOutlineTrendingUp size={24} /></div>
            <div className="metric-value">₹{primary?.mae?.toFixed(2)}</div>
            <div className="metric-label">MAE (Lakhs)</div>
            <div className="metric-sublabel">Mean Absolute Error</div>
          </div>

          <div className="glass-card metric-card mse">
            <div className="metric-icon"><HiOutlineCalculator size={24} /></div>
            <div className="metric-value">{primary?.mse?.toFixed(2)}</div>
            <div className="metric-label">MSE</div>
            <div className="metric-sublabel">Mean Squared Error</div>
          </div>

          <div className="glass-card metric-card rmse">
            <div className="metric-icon"><HiOutlineScale size={24} /></div>
            <div className="metric-value">₹{primary?.rmse?.toFixed(2)}</div>
            <div className="metric-label">RMSE (Lakhs)</div>
            <div className="metric-sublabel">Root Mean Squared Error</div>
          </div>
        </div>

        {/* ── Model Comparison Table ──────────────────────────────── */}
        <div className="glass-card comparison-card">
          <h3 style={{ marginBottom: 'var(--space-lg)' }}>
            Model Comparison
          </h3>
          <div style={{ overflowX: 'auto' }}>
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Model</th>
                  <th>R² Score</th>
                  <th>MAE (₹ Lakhs)</th>
                  <th>MSE</th>
                  <th>RMSE (₹ Lakhs)</th>
                  <th>CV R²</th>
                </tr>
              </thead>
              <tbody>
                {metrics.results?.map(result => (
                  <tr key={result.model} className={result.model === primaryModelName ? 'primary-row' : ''}>
                    <td>
                      {result.model}
                      {result.model === primaryModelName && (
                        <span className="badge badge-primary" style={{ marginLeft: '0.5rem' }}>Primary</span>
                      )}
                    </td>
                    <td>{result.r2?.toFixed(4)}</td>
                    <td>₹{result.mae?.toFixed(2)}</td>
                    <td>{result.mse?.toFixed(2)}</td>
                    <td>₹{result.rmse?.toFixed(2)}</td>
                    <td>{result.cv_r2?.toFixed(4) || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* ── Training Info ───────────────────────────────────────── */}
        <div className="model-info-grid">
          <div className="glass-card info-card">
            <div className="info-card-label">Training Samples</div>
            <div className="info-card-value text-gradient">
              {metrics.training_samples?.toLocaleString()}
            </div>
          </div>
          <div className="glass-card info-card">
            <div className="info-card-label">Test Samples</div>
            <div className="info-card-value text-gradient">
              {metrics.test_samples?.toLocaleString()}
            </div>
          </div>
          <div className="glass-card info-card">
            <div className="info-card-label">Features Used</div>
            <div className="info-card-value text-gradient">
              {metrics.num_features}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
