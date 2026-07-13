import '../App.css'

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <span>© {new Date().getFullYear()} PriceVision — India House Price Prediction</span>
        <div className="footer-links">
          <a href="https://github.com/Sidharth-46/House-Price-Prediction-System" target="_blank" rel="noreferrer">GitHub</a>
          <a href="https://www.kaggle.com/datasets/ankushpanday1/india-house-price-prediction" target="_blank" rel="noreferrer">Dataset</a>
        </div>
      </div>
    </footer>
  )
}
