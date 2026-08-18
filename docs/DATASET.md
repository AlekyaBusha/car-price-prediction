# Dataset Documentation

## 1. Dataset Overview & Inventory

The project utilizes verified used car transaction listings in India.

| File Path | Rows | Columns | Purpose |
|---|---|---|---|
| `backend/data/raw/car dataset/cardekho_dataset.csv` | 15,411 | 14 | Source raw dataset |
| `backend/data/raw/car dataset/cars_data_clean.csv` | 37,813 | 66 | Raw variant specification catalog |
| `backend/data/processed/cleaned_car_data.csv` | **15,244** | **12** | **Official Production Training Dataset** |
| `backend/data/processed/car_price_variant_training.csv` | 37,370 | 12 | Variant batch pricing catalog |
| `backend/data/processed/unified_car_price_dataset.csv` | 52,579 | 12 | Unified master reference dataset |

---

## 2. Data Preprocessing & Cleaning Pipeline

The raw dataset was cleaned via [`backend/data/scripts/clean_canonical_dataset.py`](file:///c:/Users/Dell/OneDrive/Desktop/car%20price%20pridiction/backend/data/scripts/clean_canonical_dataset.py):
1. **Deduplication**: Exact duplicate listings removed.
2. **Text Normalization**: Standardized brand names, model names, and fuel types (e.g. Maruti, Hyundai, Tata).
3. **Imputation**: Missing or zero seat counts imputed using the mode of the corresponding car model.
4. **Unit Stripping**: Numeric fields (`km/l` -> `mileage`, `CC` -> `engine`, `bhp` -> `max_power`) stripped and coerced to floating-point numbers.

---

## 3. Data Dictionary

| Column | Type | Range / Values | Description |
|---|---|---|---|
| `brand` | String | 32 brands | Manufacturer (e.g. Maruti, Hyundai, Honda, BMW) |
| `model` | String | 119 models | Car model name (e.g. Swift, City, Creta) |
| `vehicle_age` | Numeric | 0 to 29 years | Age of the car from manufacturing year |
| `km_driven` | Numeric | 100 to 3,800,000 km | Total odometer kilometers driven |
| `seller_type` | String | Individual, Dealer, Trustmark Dealer | Seller classification |
| `fuel_type` | String | Petrol, Diesel, CNG, LPG, Electric | Engine fuel type |
| `transmission_type`| String | Manual, Automatic | Transmission type |
| `mileage` | Numeric | 4.0 to 33.54 km/l | Fuel efficiency |
| `engine` | Numeric | 624 to 6592 CC | Engine displacement in cubic centimeters |
| `max_power` | Numeric | 34.2 to 626.0 bhp | Maximum engine brake horsepower |
| `seats` | Numeric | 2 to 14 | Total passenger seating capacity |
| `selling_price` | Numeric | ₹40,000 to ₹39,500,000 | Target market selling price in Indian Rupees (INR) |

---

## 4. Price Segment Breakdown

| Price Tier | Test Samples | Mean Price | Segment MAE | Segment MedAE | Segment MAPE |
|---|---|---|---|---|---|
| **Budget (< ₹3 Lakhs)** | 400 | ₹2,28,840 | **₹44,606** | **₹35,727** | 21.71% |
| **Economy (₹3L – ₹6L)** | 1,247 | ₹4,51,071 | **₹57,261** | **₹44,384** | 13.02% |
| **Mid-Range (₹6L – ₹10L)** | 910 | ₹7,66,603 | **₹81,281** | **₹61,238** | 10.54% |
| **Upper Mid (₹10L – ₹20L)** | 329 | ₹13,87,726 | **₹1,63,296** | **₹1,32,296** | 11.81% |
| **Premium (₹20L – ₹50L)** | 142 | ₹29,96,099 | **₹3,67,911** | **₹2,63,980** | 12.74% |
| **Super Luxury (> ₹50L)** | 21 | ₹62,53,714 | **₹10,32,628** | **₹8,17,683** | 16.22% |
