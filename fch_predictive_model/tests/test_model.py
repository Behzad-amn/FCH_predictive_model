import unittest
import yaml
from core.model import FCHPerformanceModel


class TestFCHPerformanceModel(unittest.TestCase):
    """
    Unit tests for the FCHPerformanceModel class.
    """

    def setUp(self) -> None:
        """Set up necessary parameters before each test."""
        # Load configuration file
        with open('config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

        # Common model parameters
        self.product_model = "AX_150"
        self.layer_count = 100
        self.life_cycle = 'BOL'

    def test_initialization(self) -> None:
        """Test if the model initializes correctly."""
        mass_flow_rates = {'dry': 100 / 1000, 'wet': 100 / 1000}
        temperatures = {'dry': 80, 'wet': 80}
        relative_humidities = {'dry': 10, 'wet': 90}
        pressures = {'dry': 120, 'wet': 120}

        model = FCHPerformanceModel(
            self.product_model, self.layer_count, self.life_cycle,
            mass_flow_rates, temperatures, relative_humidities, pressures, self.config
        )

        self.assertEqual(model.product_model, self.product_model)
        self.assertEqual(model.layer_count, self.layer_count)
        self.assertEqual(model.life_cycle, self.life_cycle)
        self.assertEqual(model.mass_flow_rates['dry'], 0.1)
        self.assertEqual(model.temperatures['dry'], 80)

    def test_solve_function(self) -> None:
        """Test the solve function to ensure it runs without errors."""
        mass_flow_rates = {'dry': 100 / 1000, 'wet': 100 / 1000}
        temperatures = {'dry': 80, 'wet': 80}
        relative_humidities = {'dry': 10, 'wet': 90}
        pressures = {'dry': 120, 'wet': 120}

        model = FCHPerformanceModel(
            self.product_model, self.layer_count, self.life_cycle,
            mass_flow_rates, temperatures, relative_humidities, pressures, self.config
        )

        model.solve()  # If this raises an exception, the test will fail

        self.assertTrue(True)  # Explicit assertion to indicate success


if __name__ == '__main__':
    unittest.main()
