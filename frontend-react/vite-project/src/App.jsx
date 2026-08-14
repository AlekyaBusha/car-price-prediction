import { useState, useEffect } from 'react'
import './App.css'

import InputForm from './components/InputForm'
import Sliders from './components/Sliders'
import PriceCard from './components/PriceCard'
import ShapChart from './components/ShapChart'
import ForecastChart from './components/ForecastChart'
import TimingBanner from './components/TimingBanner'

const API_URL = "http://127.0.0.1:8000"

function App() {
  const [carDetails, setCarDetails] = useState({
    brand: "Maruti",
    model: "Swift",
    vehicle_age: 3,
    km_driven: 40000,
    seller_type: "Individual",
    fuel_type: "Petrol",
    transmission_type: "Manual",
    mileage: 21,
    engine: 1197,
    max_power: 82,
    seats: 5
  })

  const [priceData, setPriceData] = useState(null)
  const [contributions, setContributions] = useState([])
  const [forecast, setForecast] = useState([])
  const [advice, setAdvice] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (field, value) => {
    setCarDetails(prev => ({ ...prev, [field]: value }))
  }

  useEffect(() => {
    const fetchAll = async () => {
      setLoading(true)
      setError(null)
      try {
        const [predictRes, explainRes, forecastRes] = await Promise.all([
          fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(carDetails)
          }),
          fetch(`${API_URL}/explain`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(carDetails)
          }),
          fetch(`${API_URL}/forecast`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(carDetails)
          })
        ])

        if (!predictRes.ok || !explainRes.ok || !forecastRes.ok) {
          throw new Error("One or more API calls failed")
        }

        const predictJson = await predictRes.json()
        const explainJson = await explainRes.json()
        const forecastJson = await forecastRes.json()

        setPriceData(predictJson)
        setContributions(explainJson.contributions)
        setForecast(forecastJson.forecast)
        setAdvice(forecastJson.advice)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    // Wait 400ms after the last change before calling the API,
    // so dragging a slider doesn't fire dozens of requests
    const timer = setTimeout(fetchAll, 400)
    return () => clearTimeout(timer)
  }, [carDetails])

  return (
    <div className="page">
      <h1 className="main-title">Car Valuation Advisor</h1>
      <p className="subtitle">Get a fair price estimate, understand why, and know when to buy.</p>

      <InputForm carDetails={carDetails} onChange={handleChange} />
      <Sliders carDetails={carDetails} onChange={handleChange} />

      {loading && <p className="status-text">Updating prediction...</p>}
      {error && <p className="error-text">Error: {error}. Is the API running on port 8000?</p>}

      <PriceCard priceData={priceData} />
      <ShapChart contributions={contributions} />

      <section>
        <h2 className="section-header">Should You Buy Now or Wait?</h2>
        <ForecastChart forecast={forecast} />
        <TimingBanner advice={advice} />
      </section>
    </div>
  )
}

export default App