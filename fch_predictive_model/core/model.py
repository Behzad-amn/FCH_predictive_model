import yaml
from .domain_initializer import initialize_domain_properties
from .model_trainer import solve
from .pressure_drop_calculator import calculate_pressure_drop
from .parameter_calculator import (
    calculate_channel_parameter, calculate_model_parameter,
    calculate_solver_parameters,
)
from .results_compiler import result_compiler
from ..utils.model_output import write_to_excel


class FCHPerformanceModel:
    """
    A class to model and solve the performance of a Fuel Cell Humidifier (FCH).

    Attributes:
        product_model (str): The model of the product (AX_150, AX_100).
        layer_count (int): Number of layers in the model.
        life_cycle (str): The lifecycle stage of the product.
        mass_flow_rates (dict): Mass flow rates for 'dry' and 'wet' conditions.
        temperatures (dict): Temperatures for 'dry' and 'wet' conditions.
        relative_humidities (dict): Relative humidities for 'dry' and 'wet' conditions.
        pressures (dict): Pressures for 'dry' and 'wet' conditions.
        config_path (str): Path to the configuration YAML file.
    """

    def __init__(self, product_model: str, layer_count: int, life_cycle: str, mass_flow_rates: dict,
                 temperatures: dict, relative_humidities: dict, pressures: dict,
                 config_path: str = 'app/config/config.yaml'):
        """
        Initializes the FCHPerformanceModel with the given parameters.

        Args:
            product_model (str): Model of the product.
            layer_count (int): Number of layers.
            life_cycle (str): Life cycle stage.
            mass_flow_rates (dict): Mass flow rates.
            temperatures (dict): Temperatures for dry and wet conditions.
            relative_humidities (dict): Relative humidities for dry and wet conditions.
            pressures (dict): Pressures for dry and wet conditions.
            config_path (str): Path to the configuration file.
        """

        self.product_model = self._normalize_product_model(product_model)
        self.layer_count = layer_count
        self.life_cycle = life_cycle
        self.mass_flow_rates = mass_flow_rates
        self.temperatures = temperatures
        self.relative_humidities = relative_humidities
        self.pressures = pressures

        # Load the configuration file
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)

        self._compiled_results = None

        # Section 1 - Importing variables from the configuration
        self.channel_properties = config['channel_properties'][self.product_model]
        self.air_properties = config['air_properties']
        self.membrane_properties = config['membrane_properties']
        self.model_properties = config['model_properties']
        self.press_drop_coeff = config['pressure_drop_model'][self.product_model]
        self.life_cycle_factor = config['life_cycle_factor'][life_cycle]

        # Section 2 - Calculate model parameters
        self.mesh, self.transfer_area = calculate_model_parameter(
            self.channel_properties)
        self.hyd_dia, self.area, self.channel_flow = calculate_channel_parameter(
            self.channel_properties, self.mass_flow_rates, self.layer_count, self.mesh
        )

        # Section 3 - Initialize domain properties
        (self.humidity_ratio_matrix, self.temperature_matrix, self.relative_humidity_matrix,
         self.enthalpy_matrix, self.specific_volume_matrix) = initialize_domain_properties(
            self.mesh, self.temperatures, self.relative_humidities, self.pressures
        )

        # Section 5 - Calculate solver parameters
        self.heat_res_tot, self.mas_res_tot = calculate_solver_parameters(
            self.temperatures, self.hyd_dia, self.area, self.channel_flow, self.channel_properties,
            self.air_properties, self.membrane_properties, self.transfer_area,
            self.specific_volume_matrix
        )

    def _normalize_product_model(self, product_model: str) -> str:
        """
        Normalizes the product model name to a standard format.

        Args:
            product_model (str): The raw product model name.

        Returns:
            str: The normalized product model name.
        """
        normalized_models = {
            "ax150": "AX_150", "ax-150": "AX_150", "ax 150": "AX_150", "ax_150": "AX_150",
            "ax100": "AX_100", "ax-100": "AX_100", "ax 100": "AX_100", "ax_100": "AX_100"
        }
        return normalized_models.get(product_model.lower(), product_model)

    def train(self):
        """
        train the FCH performance model using numerical methods.

        Returns:
            None
        """
        max_iterations = self.model_properties['max_iterations']
        convergence_threshold = self.model_properties['convergence_threshold']
        relax_factor = self.model_properties['relaxation_factor']

        (self.humidity_ratio_matrix, self.enthalpy_matrix, self.temperature_matrix,
         self.relative_humidity_matrix) = solve(
            self.humidity_ratio_matrix, self.enthalpy_matrix, self.temperature_matrix,
            self.relative_humidity_matrix, self.specific_volume_matrix,
            self.channel_flow, self.mesh, self.temperatures, self.pressures,
            self.heat_res_tot, self.mas_res_tot, self.life_cycle_factor,
            max_iterations, convergence_threshold, relax_factor
        )
        self.calculate_pressure_drop()

    def calculate_pressure_drop(self) -> dict:
        """
        Calculates the pressure drop for dry and wet conditions.

        Returns:
            dict: Pressure drop values for dry and wet conditions.
        """
        self.pressure_drop = {}
        for condition in ['dry', 'wet']:
            coefficients = self.press_drop_coeff[condition]
            self.pressure_drop[condition] = calculate_pressure_drop(
                self.mass_flow_rates[condition], self.layer_count, coefficients
            )
        return self.pressure_drop

    def compile_results(self) -> dict:
        """
        Compiles the results from the model solution.

        Returns:
            dict: Compiled results including pressures, pressure drops, and other relevant data.
        """
        self.train()
        self._compiled_results = result_compiler(
            self.pressures, self.pressure_drop, self.enthalpy_matrix, self.humidity_ratio_matrix, self.mass_flow_rates
        )

        return self._compiled_results

    def save_results(self, filename: str):
        """
        Saves the compiled results to an Excel file.

        Args:
            filename (str): The name of the file to save results to.

        Returns:
            None
        """
        if self._compiled_results is None:
            self.compile_results()

        write_to_excel(self._compiled_results, filename)

    def __repr__(self):
        return (f"FCHPerformanceModel(product_model={self.product_model}, "
                f"layer_count={self.layer_count}, life_cycle={self.life_cycle})")


if __name__ == "__main__":
    print("Please use the run_model script to access this function")
