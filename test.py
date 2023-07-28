import unittest
from unittest.mock import patch, Mock
from main import get_current_price, calculate_price_changes, get_average_gain_loss, generate_signals

class TestTradingAlgorithm(unittest.TestCase):

    @patch('requests.get')
    def test_get_current_price(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"amount": "1000"}}
        mock_get.return_value = mock_response

        result = get_current_price("BTC")
        self.assertEqual(result, 1000.0)

    def test_calculate_price_changes(self):
        prices = [1, 2, 3, 4, 5]
        expected_result = [1, 1, 1, 1]
        result = calculate_price_changes(prices)
        self.assertEqual(result, expected_result)

    def test_get_average_gain_loss(self):
        delta = [1, -2, 3, -4, 5]
        expected_gain, expected_loss = 300, 2
        avg_gain, avg_loss = get_average_gain_loss(delta)
        self.assertEqual(avg_gain, expected_gain)
        self.assertEqual(avg_loss, expected_loss)

    def test_generate_signals(self):
        self.assertEqual(generate_signals(20), "BUY")
        self.assertEqual(generate_signals(80), "SELL")
        self.assertEqual(generate_signals(50), None)

if __name__ == '__main__':
    unittest.main()