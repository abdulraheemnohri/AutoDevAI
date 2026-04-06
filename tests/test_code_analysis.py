import unittest
import os
from code_analysis.analyzer import analyze_python_file

class TestCodeAnalysis(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "test_code.py"
        with open(self.test_file_path, "w") as f:
            f.write("""
def bad_function():
    try:
        pass
    except:
        print("Error")
    eval("1+1")

def good_function():
    print("Hello")
""")

    def tearDown(self):
        os.remove(self.test_file_path)

    def test_analyze_python_file(self):
        issues = analyze_python_file(self.test_file_path)
        self.assertIsInstance(issues, list)
        self.assertTrue(any("Bare 'except:'" in issue for issue in issues))
        self.assertTrue(any("Use of 'eval()'" in issue for issue in issues))
        self.assertTrue(any("'print()' used" in issue for issue in issues))

if __name__ == '__main__':
    unittest.main()
