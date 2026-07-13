import { useState, useEffect } from 'react'
import { getFeatureOptions, predictPrice } from '../services/api'
import { useToast } from '../context/ToastContext'
import '../App.css'

const INITIAL_FORM = {
  State: '',
  City: '',
  Property_Type: '',
  BHK: '',
  Size_in_SqFt: '',
  Year_Built: '',
  Furnished_Status: '',
  Floor_No: '',
  Total_Floors: '',
  Nearby_Schools: '5',
  Nearby_Hospitals: '5',
  Public_Transport_Accessibility: 'Medium',
  Parking_Space: 'No',
  Security: 'No',
  Amenities: '',
  Facing: '',
  Owner_Type: '',
  Availability_Status: '',
}

export default function Predict() {
  const { addToast } = useToast()
  const [options, setOptions] = useState(null)
  const [form, setForm] = useState(INITIAL_FORM)
  const [amenities, setAmenities] = useState([])
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [optionsLoading, setOptionsLoading] = useState(true)
  const [errors, setErrors] = useState({})

  // Fetch dropdown options from Flask API on mount
  useEffect(() => {
    getFeatureOptions()
      .then(data => {
        setOptions(data)
        setOptionsLoading(false)
      })
      .catch(err => {
        addToast('Failed to load form options. Is the Flask server running?', 'error')
        setOptionsLoading(false)
      })
  }, [])

  // Get cities filtered by selected state
  const filteredCities = form.State && options?.state_city_map
    ? options.state_city_map[form.State] || []
    : options?.cities || []

  // Handle form field changes
  function handleChange(e) {
    const { name, value } = e.target
    setForm(prev => ({
      ...prev,
      [name]: value,
      // Reset city when state changes
      ...(name === 'State' ? { City: '' } : {}),
    }))
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }))
    }
  }

  // Handle amenity checkbox toggle
  function toggleAmenity(amenity) {
    setAmenities(prev =>
      prev.includes(amenity)
        ? prev.filter(a => a !== amenity)
        : [...prev, amenity]
    )
  }

  // Validate form before submission
  function validate() {
    const newErrors = {}
    const required = ['State', 'City', 'Property_Type', 'BHK', 'Size_in_SqFt', 'Year_Built', 'Furnished_Status', 'Floor_No', 'Total_Floors', 'Facing', 'Owner_Type', 'Availability_Status']
    required.forEach(field => {
      if (!form[field]) newErrors[field] = 'Required'
    })

    // Numeric validations
    if (form.BHK && (form.BHK < 1 || form.BHK > 10)) newErrors.BHK = 'BHK must be 1–10'
    if (form.Size_in_SqFt && (form.Size_in_SqFt < 100 || form.Size_in_SqFt > 50000)) newErrors.Size_in_SqFt = 'Must be 100–50,000'
    if (form.Year_Built && (form.Year_Built < 1900 || form.Year_Built > 2030)) newErrors.Year_Built = 'Must be 1900–2030'
    if (form.Floor_No && (form.Floor_No < 0 || form.Floor_No > 100)) newErrors.Floor_No = 'Must be 0–100'
    if (form.Total_Floors && (form.Total_Floors < 1 || form.Total_Floors > 100)) newErrors.Total_Floors = 'Must be 1–100'

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Submit prediction request
  async function handleSubmit(e) {
    e.preventDefault()
    if (!validate()) {
      addToast('Please fix the highlighted errors.', 'error')
      return
    }

    setLoading(true)
    setResult(null)

    try {
      // Build the payload
      const payload = {
        ...form,
        BHK: parseInt(form.BHK),
        Size_in_SqFt: parseInt(form.Size_in_SqFt),
        Year_Built: parseInt(form.Year_Built),
        Floor_No: parseInt(form.Floor_No),
        Total_Floors: parseInt(form.Total_Floors),
        Nearby_Schools: parseInt(form.Nearby_Schools || 5),
        Nearby_Hospitals: parseInt(form.Nearby_Hospitals || 5),
        Amenities: amenities.join(', ') || 'None',
      }

      const data = await predictPrice(payload)
      setResult(data)
      addToast('Prediction successful!', 'success')
    } catch (err) {
      addToast(err.message || 'Prediction failed. Please try again.', 'error')
    } finally {
      setLoading(false)
    }
  }

  // Reset form
  function handleReset() {
    setForm(INITIAL_FORM)
    setAmenities([])
    setResult(null)
    setErrors({})
  }

  // Loading state
  if (optionsLoading) {
    return (
      <div className="loading-screen">
        <div className="spinner spinner-lg" />
        <p>Loading form options...</p>
      </div>
    )
  }

  return (
    <div className="predict-page page-enter">
      <div className="container">
        <div className="section-header">
          <h2>Predict House <span className="text-gradient">Price</span></h2>
          <p>Enter your property details below to get an instant price estimate.</p>
        </div>

        <div className="predict-layout">
          {/* ── Prediction Form ──────────────────────────────────────── */}
          <div className="glass-card predict-form-card">
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                {/* State */}
                <div className="form-group">
                  <label className="form-label">State *</label>
                  <select name="State" value={form.State} onChange={handleChange} className="form-select">
                    <option value="">Select State</option>
                    {options?.states?.map(s => <option key={s} value={s}>{s}</option>)}
                  </select>
                  {errors.State && <span className="form-error">{errors.State}</span>}
                </div>

                {/* City */}
                <div className="form-group">
                  <label className="form-label">City *</label>
                  <select name="City" value={form.City} onChange={handleChange} className="form-select">
                    <option value="">Select City</option>
                    {filteredCities.map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                  {errors.City && <span className="form-error">{errors.City}</span>}
                </div>

                {/* Property Type */}
                <div className="form-group">
                  <label className="form-label">Property Type *</label>
                  <select name="Property_Type" value={form.Property_Type} onChange={handleChange} className="form-select">
                    <option value="">Select Type</option>
                    {options?.property_types?.map(t => <option key={t} value={t}>{t}</option>)}
                  </select>
                  {errors.Property_Type && <span className="form-error">{errors.Property_Type}</span>}
                </div>

                {/* BHK */}
                <div className="form-group">
                  <label className="form-label">BHK *</label>
                  <input type="number" name="BHK" value={form.BHK} onChange={handleChange}
                    className="form-input" placeholder="e.g. 2" min="1" max="10" />
                  {errors.BHK && <span className="form-error">{errors.BHK}</span>}
                </div>

                {/* Size */}
                <div className="form-group">
                  <label className="form-label">Size (sq. ft.) *</label>
                  <input type="number" name="Size_in_SqFt" value={form.Size_in_SqFt} onChange={handleChange}
                    className="form-input" placeholder="e.g. 1200" min="100" max="50000" />
                  {errors.Size_in_SqFt && <span className="form-error">{errors.Size_in_SqFt}</span>}
                </div>

                {/* Year Built */}
                <div className="form-group">
                  <label className="form-label">Year Built *</label>
                  <input type="number" name="Year_Built" value={form.Year_Built} onChange={handleChange}
                    className="form-input" placeholder="e.g. 2015" min="1900" max="2030" />
                  {errors.Year_Built && <span className="form-error">{errors.Year_Built}</span>}
                </div>

                {/* Furnished Status */}
                <div className="form-group">
                  <label className="form-label">Furnished Status *</label>
                  <select name="Furnished_Status" value={form.Furnished_Status} onChange={handleChange} className="form-select">
                    <option value="">Select Status</option>
                    {options?.furnished_statuses?.map(s => <option key={s} value={s}>{s}</option>)}
                  </select>
                  {errors.Furnished_Status && <span className="form-error">{errors.Furnished_Status}</span>}
                </div>

                {/* Floor No */}
                <div className="form-group">
                  <label className="form-label">Floor Number *</label>
                  <input type="number" name="Floor_No" value={form.Floor_No} onChange={handleChange}
                    className="form-input" placeholder="e.g. 5" min="0" max="100" />
                  {errors.Floor_No && <span className="form-error">{errors.Floor_No}</span>}
                </div>

                {/* Total Floors */}
                <div className="form-group">
                  <label className="form-label">Total Floors *</label>
                  <input type="number" name="Total_Floors" value={form.Total_Floors} onChange={handleChange}
                    className="form-input" placeholder="e.g. 20" min="1" max="100" />
                  {errors.Total_Floors && <span className="form-error">{errors.Total_Floors}</span>}
                </div>

                {/* Facing */}
                <div className="form-group">
                  <label className="form-label">Facing *</label>
                  <select name="Facing" value={form.Facing} onChange={handleChange} className="form-select">
                    <option value="">Select Facing</option>
                    {options?.facings?.map(f => <option key={f} value={f}>{f}</option>)}
                  </select>
                  {errors.Facing && <span className="form-error">{errors.Facing}</span>}
                </div>

                {/* Owner Type */}
                <div className="form-group">
                  <label className="form-label">Owner Type *</label>
                  <select name="Owner_Type" value={form.Owner_Type} onChange={handleChange} className="form-select">
                    <option value="">Select Owner</option>
                    {options?.owner_types?.map(o => <option key={o} value={o}>{o}</option>)}
                  </select>
                  {errors.Owner_Type && <span className="form-error">{errors.Owner_Type}</span>}
                </div>

                {/* Availability */}
                <div className="form-group">
                  <label className="form-label">Availability *</label>
                  <select name="Availability_Status" value={form.Availability_Status} onChange={handleChange} className="form-select">
                    <option value="">Select Status</option>
                    {options?.availability_statuses?.map(a => <option key={a} value={a}>{a}</option>)}
                  </select>
                  {errors.Availability_Status && <span className="form-error">{errors.Availability_Status}</span>}
                </div>

                {/* Transport Accessibility */}
                <div className="form-group">
                  <label className="form-label">Transport Access</label>
                  <select name="Public_Transport_Accessibility" value={form.Public_Transport_Accessibility} onChange={handleChange} className="form-select">
                    {options?.transport_accessibility?.map(t => <option key={t} value={t}>{t}</option>)}
                  </select>
                </div>

                {/* Parking */}
                <div className="form-group">
                  <label className="form-label">Parking Space</label>
                  <select name="Parking_Space" value={form.Parking_Space} onChange={handleChange} className="form-select">
                    <option value="No">No</option>
                    <option value="Yes">Yes</option>
                  </select>
                </div>

                {/* Security */}
                <div className="form-group">
                  <label className="form-label">Security</label>
                  <select name="Security" value={form.Security} onChange={handleChange} className="form-select">
                    <option value="No">No</option>
                    <option value="Yes">Yes</option>
                  </select>
                </div>

                {/* Nearby Schools */}
                <div className="form-group">
                  <label className="form-label">Nearby Schools</label>
                  <input type="number" name="Nearby_Schools" value={form.Nearby_Schools} onChange={handleChange}
                    className="form-input" placeholder="e.g. 5" min="0" max="50" />
                </div>

                {/* Amenities — full width */}
                <div className="form-group full-width">
                  <label className="form-label">Amenities</label>
                  <div className="checkbox-group">
                    {options?.amenities?.map(a => (
                      <label key={a} className="checkbox-label">
                        <input type="checkbox" checked={amenities.includes(a)} onChange={() => toggleAmenity(a)} />
                        {a}
                      </label>
                    ))}
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="form-actions full-width">
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? (
                    <><div className="spinner" /> Predicting...</>
                  ) : (
                    'Predict Price →'
                  )}
                </button>
                <button type="button" className="btn btn-ghost" onClick={handleReset}>
                  Reset Form
                </button>
              </div>
            </form>
          </div>

          {/* ── Result Sidebar ───────────────────────────────────────── */}
          <div className="result-sidebar">
            {result ? (
              <div className="glass-card result-card">
                <div className="result-label">Estimated Price</div>
                <div className="result-price text-gradient">
                  ₹ {result.predicted_price_lakhs?.toFixed(2)} L
                </div>
                <div className="result-price-rupees">
                  {result.predicted_price_rupees}
                </div>
                <div className="result-model-info">
                  <span className="badge badge-primary">{result.model_used}</span>
                </div>
              </div>
            ) : (
              <div className="glass-card result-card">
                <div className="result-placeholder">
                  <div className="result-placeholder-icon">🏠</div>
                  <p>Fill out the form and click <strong>Predict Price</strong> to see the estimated value here.</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
