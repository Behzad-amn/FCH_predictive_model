from app.core.model import FCHPerformanceModel

# Define model parameters
product_model = "Ax150"  # Model name/identifier
layer_count = 100        # Number of layers in the model
life_cycle = 'BOL'       # Life cycle stage (e.g., Beginning of Life)

# Define operating conditions
mass_flow_rates = {
    'dry': 100 / 1000,  # Mass flow rate on the dry side (kg/s)
    'wet': 100 / 1000   # Mass flow rate on the wet side (kg/s)
}
temperatures = {
    'dry': 80,  # Temperature on the dry side (°C)
    'wet': 80   # Temperature on the wet side (°C)
}
relative_humidities = {
    'dry': 10,  # Relative humidity on the dry side (%)
    'wet': 90   # Relative humidity on the wet side (%)
}
pressures = {
    'dry': 120,  # Pressure on the dry side (kPa)
    'wet': 120   # Pressure on the wet side (kPa)
}

# Instantiate the model
model = FCHPerformanceModel(
    product_model, layer_count, life_cycle,
    mass_flow_rates, temperatures,
    relative_humidities, pressures
)

# Compile the results
results = model.compile_results()

# Optionally save the results to an Excel file
# Uncomment the line below to save the results
# model.save_results('results.xlsx')
