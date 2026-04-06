import unittest
from ai_engine.router import generate

class TestAIEngine(unittest.TestCase):
    def test_generate_response(self):
        # This test would require mocking API calls or setting up a test API
        # For now, we'll just assert that it returns a string.
        prompt = "Hello, AI!"
        response = generate(prompt)
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()
