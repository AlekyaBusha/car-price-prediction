// Mock data shaped exactly like what the real API will return.
// Once the backend is connected, these get replaced by real fetch() responses.

export const MOCK_PRICE_DATA = {
  low: 539951.71,
  predicted: 645365.03,
  high: 750778.35
}

export const MOCK_CONTRIBUTIONS = [
  { feature: "max_power", impact: -140188.17 },
  { feature: "engine", impact: -103553.04 },
  { feature: "vehicle_age", impact: -83733.23 },
  { feature: "transmission_type_Manual", impact: 45210.50 },
  { feature: "km_driven", impact: -36560.56 }
]

export const MOCK_FORECAST = [
  { months: 0, price: 645365 },
  { months: 6, price: 631971 },
  { months: 12, price: 605704 },
  { months: 24, price: 578284 }
]

export const MOCK_ADVICE = {
  recommendation: "buy_now",
  message: "Price is expected to stay fairly stable (only 2.08% drop over 6 months). This is a reasonable time to buy."
}