import pytest
from cicd.promote import get_sorted_dict, _find_difference


@pytest.mark.parametrize("input_items, expected_result_dict, expected_result_list", [
    ([('1', 'one'), ('3', 'three'), ('2', 'two')], ({"1": "one", "3": "three", "2": "two"}), ([1, 2, 3]))])
def test_get_sorted_dict(input_items, expected_result_dict, expected_result_list):
    result_dict, result_list = get_sorted_dict(input_items)
    assert result_dict == expected_result_dict
    assert result_list == expected_result_list


def test_find_difference(create_change_file_json):

    result_set = _find_difference('/tmp/changelog/')

    assert isinstance(result_set, set)
