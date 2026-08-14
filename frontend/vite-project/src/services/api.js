const BASE_URL = "http://127.0.0.1:8000";

export async function fetchBrands() {
  const response = await fetch(`${BASE_URL}/dropdown/brands`);

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

export async function fetchFuelTypes() {
  const response = await fetch(`${BASE_URL}/dropdown/fuel-types`);

  if (!response.ok) {
    throw new Error("Failed to fetch fuel types");
  }

  return response.json();
}

export async function fetchTransmissions() {
  const response = await fetch(`${BASE_URL}/dropdown/transmissions`);

  if (!response.ok) {
    throw new Error("Failed to fetch transmissions");
  }

  return response.json();
}

export async function fetchSellerTypes() {
  const response = await fetch(`${BASE_URL}/dropdown/seller-types`);

  if (!response.ok) {
    throw new Error("Failed to fetch seller types");
  }

  return response.json();
}

export async function fetchEngines() {
  const response = await fetch(`${BASE_URL}/dropdown/engines`);

  if (!response.ok) {
    throw new Error("Failed to fetch engines");
  }

  return response.json();
}

export async function fetchSeats() {
  const response = await fetch(`${BASE_URL}/dropdown/seats`);

  if (!response.ok) {
    throw new Error("Failed to fetch seats");
  }

  return response.json();
}

export async function fetchMaxPowers() {
  const response = await fetch(`${BASE_URL}/dropdown/max-powers`);

  if (!response.ok) {
    throw new Error("Failed to fetch max powers");
  }

  return response.json();
}