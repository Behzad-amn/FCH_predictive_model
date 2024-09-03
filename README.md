# FCH Performance Model

## Overview

The FCH Performance Model is a software package designed to simulate and optimize the performance of Fuel Cell Humidifiers (FCH). This tool uses predictive modeling methodologies to forecast the behavior of FCH systems under various operating conditions.

**Important Notice:** The code in `config.yaml` and `trainer.py` has been intentionally removed to comply with non-disclosure agreements (NDA) and protect proprietary algorithms.

## Features

- **Predictive Modeling Framework:** The FCH Performance Model utilizes advanced algorithms to simulate complex system interactions, providing reliable predictions of FCH performance.
- **Configurable Parameters:** Users can specify various operating conditions, such as temperature, humidity, and pressure, allowing for detailed performance simulations.
- **Modular Design:** The package is designed for modularity, enabling easy integration, customization, and scalability within different system configurations.

## Installation

### Prerequisites

- Python 3+
- Docker (optional, for containerized deployment)
- Uvicorn (for running the FastAPI app)

### Running the FastAPI Application

To run the FastAPI application locally using Uvicorn, follow these steps:

1. **Navigate to the project directory:**

   ```bash
   cd fch_performance_model
   ```

2. **Run the FastAPI app using Uvicorn:**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 80
   ```

3. **Access the application in your web browser:**
   ```
   http://localhost:80
   ```

### Docker Container

To create a Docker container for the FCH Performance Model, follow these steps:

1. **Build the Docker image:**

   ```bash
   docker build -t fch_performance_model .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -p 80:80 fch_performance_model
   ```

3. **Access the application in your web browser:**
   ```
   http://localhost:80
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Disclaimer

Please note that certain components, such as `config.yaml` and `trainer.py`, have been removed or obfuscated to comply with NDAs. As a result, the software may not be fully functional in its current public form.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions or find a bug.

## Contact

For any questions or further information, please contact Behzad Aminian at [aminian.bz@gmail.com](mailto:aminian.bz@gmail.com).
