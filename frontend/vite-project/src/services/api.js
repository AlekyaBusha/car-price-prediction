const BASE_URL = "http://127.0.0.1:8000";


// =========================================================
// DROPDOWNS
// =========================================================

export async function fetchBrands() {
  const response = await fetch(
    `${BASE_URL}/dropdown/brands`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch brands");
  }

  return response.json();
}


export async function fetchModels(brand) {
  const response = await fetch(
    `${BASE_URL}/dropdown/models/${encodeURIComponent(brand)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch models");
  }

  return response.json();
}


export async function fetchFuelTypes(brand, model) {
  const response = await fetch(
    `${BASE_URL}/dropdown/fuel-types/${encodeURIComponent(brand)}/${encodeURIComponent(model)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch fuel types");
  }

  return response.json();
}


export async function fetchTransmissions(brand, model) {
  const response = await fetch(
    `${BASE_URL}/dropdown/transmissions/${encodeURIComponent(brand)}/${encodeURIComponent(model)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch transmissions");
  }

  return response.json();
}


export async function fetchSellerTypes(brand, model) {
  const response = await fetch(
    `${BASE_URL}/dropdown/seller-types/${encodeURIComponent(brand)}/${encodeURIComponent(model)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch seller types");
  }

  return response.json();
}


export async function fetchEngines(brand, model) {
  const response = await fetch(
    `${BASE_URL}/dropdown/engines/${encodeURIComponent(brand)}/${encodeURIComponent(model)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch engines");
  }

  return response.json();
}


export async function fetchMaxPowers(brand, model) {
  const response = await fetch(
    `${BASE_URL}/dropdown/max-powers/${encodeURIComponent(brand)}/${encodeURIComponent(model)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch max powers");
  }

  return response.json();
}


export async function fetchSeats(brand, model) {
  const response = await fetch(
    `${BASE_URL}/dropdown/seats/${encodeURIComponent(brand)}/${encodeURIComponent(model)}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch seats");
  }

  return response.json();
}


// =========================================================
// PREDICTION
// =========================================================

export async function predictPrice(carData) {

  const response = await fetch(
    `${BASE_URL}/predict/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },

      body: JSON.stringify(carData),
    }
  );


  if (!response.ok) {

    const errorText =
      await response.text();

    throw new Error(
      `Prediction failed: ${errorText}`
    );
  }


  return response.json();
}


// =========================================================
// SHAP EXPLANATION
// =========================================================

export async function explainPrice(carData) {

  const response = await fetch(
    `${BASE_URL}/explain/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },

      body: JSON.stringify(carData),
    }
  );


  if (!response.ok) {

    const errorText =
      await response.text();

    throw new Error(
      `Explanation failed: ${errorText}`
    );
  }


  return response.json();
}


// =========================================================
// FORECAST
// =========================================================

export async function forecastPrice(carData) {

  const response = await fetch(
    `${BASE_URL}/forecast/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },

      body: JSON.stringify(carData),
    }
  );


  if (!response.ok) {

    const errorText =
      await response.text();

    throw new Error(
      `Forecast failed: ${errorText}`
    );
  }


  return response.json();
}
// =========================================================
// PREDICTION OPTIONS / SUGGESTIONS
// =========================================================

export async function predictOptions(carData) {

  const response = await fetch(
    `${BASE_URL}/predict/options/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },

      body: JSON.stringify(carData),
    }
  );

  if (!response.ok) {

    const errorText =
      await response.text();

    throw new Error(
      `Prediction options failed: ${errorText}`
    );
  }

  return response.json();

}
// =========================================================
// VARIANT PREDICTION
// =========================================================

export async function predictVariants(carData) {

  const response = await fetch(
    `${BASE_URL}/predict/variants`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },

      body: JSON.stringify(carData),
    }
  );

  if (!response.ok) {

    const errorText =
      await response.text();

    throw new Error(
      `Variant prediction failed: ${errorText}`
    );
  }

  return response.json();
}