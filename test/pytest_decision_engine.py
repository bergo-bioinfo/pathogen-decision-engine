import pandas as pd
import pytest
from pathogen_decision_engine import PathogenDecisionEngine


common_args = ("input_sample,expected_result", [
    ({'BA': 1}, 'Benign'),
    ({'BS': 2}, 'Benign'),
    ({'BS': 3}, 'Benign'),
    ({'BS': 1, 'BP': 1}, 'Likely Benign'),
    ({'BP': 2}, 'Likely Benign'),
    ({'BP': 3}, 'Likely Benign'),
    ({'BA': 1, 'PA': 1}, 'Uncertain significance'),
    ({'BS': 2, 'PS': 2}, 'Uncertain significance'),
    ({'PS': 1}, 'Uncertain significance'),
    ({'BS': 1}, 'Uncertain significance'),
    ({'PVS': 1, 'PM': 1}, 'Likely pathogenic'),
    ({'PS': 1, 'PM': 1}, 'Likely pathogenic'),
    ({'PS': 1, 'PM': 2}, 'Likely pathogenic'),
    ({'PS': 1, 'PP': 2}, 'Likely pathogenic'),
    ({'PS': 1, 'PP': 3}, 'Likely pathogenic'),
    ({'PM': 3}, 'Likely pathogenic'),
    ({'PM': 4}, 'Likely pathogenic'),
    ({'PM': 2, 'PP': 2}, 'Likely pathogenic'),
    ({'PM': 2, 'PP': 3}, 'Likely pathogenic'),
    ({'PM': 1, 'PP': 4}, 'Likely pathogenic'),
    ({'PM': 1, 'PP': 5}, 'Likely pathogenic'),
    ({'PA': 1}, 'Pathogenic'),
    ({'PA': 2}, 'Pathogenic'),
    ({'PVS': 1, 'PS': 1}, 'Pathogenic'),
    ({'PVS': 1, 'PS': 2}, 'Pathogenic'),
    ({'PVS': 1, 'PM': 1, 'PP': 1}, 'Pathogenic'),
    ({'PVS': 1, 'PM': 0, 'PP': 2}, 'Pathogenic'),
    ({'PVS': 1, 'PM': 2, 'PP': 0}, 'Pathogenic'),
    ({'PVS': 1, 'PM': 2, 'PP': 2}, 'Pathogenic'),
    ({'PS': 2}, 'Pathogenic'),
    ({'PS': 3}, 'Pathogenic'),
    ({'PS': 1, 'PM': 3}, 'Pathogenic'),
    ({'PS': 1, 'PM': 4}, 'Pathogenic')
])


@pytest.fixture(scope='module')
def test_pathogen_decision_engine():
    path = "data/sovad_rules_table.csv"
    df = pd.read_csv(path)
    df = df.fillna(0)
    rule_table = pd.DataFrame(df)
    pde = PathogenDecisionEngine(rule_table)

    return pde


@pytest.mark.parametrize(*common_args)
def test_infer(test_pathogen_decision_engine, input_sample, expected_result):
    result = test_pathogen_decision_engine.infer(input_sample)
    assert result[0].lower() == expected_result.lower()
