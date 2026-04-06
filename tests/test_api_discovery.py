import unittest
from api_discovery.api_searcher import discover_apis
from api_discovery.endpoint_extractor import extract
from api_discovery.api_validator import validate_endpoint

class TestApiDiscovery(unittest.TestCase):
    def test_extract_endpoints(self):
        text = "Found API at https://example.com/api/v1/chat/completions and another at http://test.org/v1/inference"
        endpoints = extract(text)
        self.assertIn("https://example.com/api/v1/chat/completions", endpoints)
        self.assertIn("http://test.org/v1/inference", endpoints)

    # Add more tests for discovery_apis and validate_endpoint (mocking external calls)

if __name__ == '__main__':
    unittest.main()
