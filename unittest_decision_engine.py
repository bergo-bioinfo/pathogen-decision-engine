import unittest
import pandas as pd
import rule_engine
from pathogen_decision_engine import PathogenDecisionEngine


class TestPathogenDecisionEngine(unittest.TestCase):
    def setUp(self):
        path = "/home/mancelle/projects/decision_sovad/table.csv"
        df = pd.read_csv(path)
        df = df.fillna(0)

        self.rule_table = pd.DataFrame(df)
        self.pde = PathogenDecisionEngine(self.rule_table)

    def test_infer(self):
        # Create test cases
        test_cases = load_test_cases()
        input_samples, expected_results = test_cases['input_samples'], test_cases['expected_results']
        for input_sample, expected_result in zip(input_samples, expected_results):

            # Call the infer method
            result = self.pde.infer(input_sample)
            print(input_sample, result, result[0], expected_result)

            # Assert the result
            self.assertEqual(result[0].lower(), expected_result.lower())

    def test_infer_invalid_input(self, input_samples):
        for input_sample in input_samples:
            # Call the infer method
            with self.assertRaises(AssertionError):
                self.pde.infer(input_sample)

    def test_build_rule_engine(self):
        # Call the build_rule_engine method
        rule_engine_path = self.pde.build_rule_engine()

        # Assert that the rule engine is a list
        self.assertIsInstance(rule_engine_path, list)

        # Assert that each element in the rule engine is a tuple
        for rule in rule_engine_path:
            self.assertIsInstance(rule, tuple)

        # Assert that each tuple has two elements: a Rule object and a string label
        for rule in rule_engine_path:
            self.assertIsInstance(rule[0], rule_engine.Rule)
            self.assertIsInstance(rule[1], str)

    def test_input_validator(self, input_dicts):
        for input_dict in input_dicts:
            # Call the input_validator method
            self.pde.input_validator(input_dict)


def load_test_cases():
    test_cases = {
            'input_samples': [
                {"BA": 1},
                {"BS": 2},
                {"BS": 3},
                {"BS": 1, "BP": 1},
                {"BP": 2},
                {"BP": 3},
                {"BA": 1, "PA": 1},
                {"BS": 2, "PS": 2},
                {"PS": 1},
                {"BS": 1},
                {"PVS": 1, "PM": 1},
                {"PS": 1, "PM": 1},
                {"PS": 1, "PM": 2},
                {"PS": 1, "PP": 2},
                {"PS": 1, "PP": 3},
                {"PM": 3},
                {"PM": 4},
                {"PM": 2, "PP": 2},
                {"PM": 2, "PP": 3},
                {"PM": 1, "PP": 4},
                {"PM": 1, "PP": 5},
                {"PA": 1},
                {"PA": 2},
                {"PVS": 1, "PS": 1},
                {"PVS": 1, "PS": 2},
                {"PVS": 1, "PM": 1, "PP": 1},
                {"PVS": 1, "PM": 0, "PP": 2},
                {"PVS": 1, "PM": 2, "PP": 0},
                {"PVS": 1, "PM": 2, "PP": 2},
                {"PS": 2},
                {"PS": 3},
                {"PS": 1, "PM": 3},
                {"PS": 1, "PM": 4},
                {"PS": 1, "PM": 2, "PP": 2},
                {"PS": 1, "PM": 2, "PP": 3},
                {"PS": 1, "PM": 1, "PP": 4},
                {"PS": 1, "PM": 1, "PP": 5},

            ],
            'expected_results': [
                'Benign',
                'Benign',
                'Benign',
                'Likely Benign',
                'Likely Benign',
                'Likely Benign',
                'Uncertain significance',
                'Uncertain significance',
                'Uncertain significance',
                'Uncertain significance',
                'Likely pathogenic',
                'Likely pathogenic',
                'Likely pathogenic',
                'Likely pathogenic',
                'Likely pathogenic',
                'Likely pathogenic',
                'Likely pathogenic',
                'Likely pathogenic',
                'Likely pathogenic',
                'Likely pathogenic',
                'Likely pathogenic',
                'Pathogenic',
                'Pathogenic',
                'Pathogenic',
                'Pathogenic',
                'Pathogenic',
                'Pathogenic',
                'Pathogenic',
                'Pathogenic',
                'Pathogenic',
                'Pathogenic',
                'Pathogenic',
                'Pathogenic'
            ]
        }
    return test_cases


def main():
    # Create test suite
    suite = unittest.TestSuite()

    # Add test cases to the suite
    suite.addTest(TestPathogenDecisionEngine('test_infer'))

    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    main()
