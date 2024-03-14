import pandas as pd
import pytest
from pathogen_decision_engine import PathogenDecisionEngine

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


@pytest.fixture(scope='module')
def test_pathogen_decision_engine():
    path = "data/sovad_rules_table.csv"
    df = pd.read_csv(path)
    df = df.fillna(0)

    rule_table = pd.DataFrame(df)
    pde = PathogenDecisionEngine(rule_table)

    return pde


def test_infer(test_pathogen_decision_engine):
    test_cases = load_test_cases()
    input_samples, expected_results = test_cases['input_samples'], test_cases['expected_results']
    for input_sample, expected_result in zip(input_samples, expected_results):
        result = test_pathogen_decision_engine.infer(input_sample)
        assert result[0].lower() == expected_result.lower()
