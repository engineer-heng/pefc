import unittest
from pefc.mlutils import (percent_change, percent_changefrom_target,
                          percent_diff, percent_error, snake2camel_case,
                          camel2snake_case, mround)
import numpy as np


class TestPercentChange(unittest.TestCase):
    """Test cases for the percent_change function."""

    def test_basic_positive_numbers(self):
        """Test with basic positive numbers."""
        self.assertEqual(percent_change(100, 110), 10.0)
        self.assertEqual(percent_change(50, 75), 50.0)
        self.assertEqual(percent_change(200, 150), -25.0)
        self.assertEqual(percent_change(10, 10), 0.0)

    def test_negative_numbers(self):
        """Test with negative numbers."""
        self.assertEqual(percent_change(-10, -6), -40.0)
        self.assertEqual(percent_change(-20, -10), -50.0)
        self.assertEqual(percent_change(-100, -150), 50.0)
        self.assertEqual(percent_change(-50, 50), -200.0)

    def test_zero_values(self):
        """Test with zero values."""
        with self.assertRaises(ZeroDivisionError):
            percent_change(0, 10)

        self.assertEqual(percent_change(10, 0), -100.0)

    def test_fraction_output(self):
        """Test with fraction output flag."""
        self.assertEqual(percent_change(100, 110, frac=True), 0.1)
        self.assertEqual(percent_change(50, 75, frac=True), 0.5)
        self.assertEqual(percent_change(
            200, 150, frac=True), -0.25)
        self.assertEqual(percent_change(10, 10, frac=True), 0.0)

    def test_large_and_small_numbers(self):
        """Test with very large and very small numbers."""
        self.assertEqual(percent_change(1e6, 2e6), 100.0)
        self.assertEqual(percent_change(1e-6, 2e-6), 100.0)
        self.assertEqual(percent_change(1e6, 5e5), -50.0)
        self.assertEqual(percent_change(1e-6, 5e-7), -50.0)

    def test_floating_point_precision(self):
        """Test with floating point precision."""
        self.assertAlmostEqual(percent_change(
            3.33, 4.44), 33.3333, places=4)
        self.assertAlmostEqual(
            percent_change(4.44, 3.33), -25.0, places=4)
        self.assertAlmostEqual(percent_change(
            3.33, 4.44, frac=True), 0.3333, places=4)
        self.assertAlmostEqual(percent_change(
            4.44, 3.33, frac=True), -0.25, places=4)

    def test_formula_verification(self):
        """Verify the formula implementation is correct."""
        # Formula: perchg = (value2 - value1)/value1 * 100
        value1 = 50
        value2 = 75
        expected = (value2 - value1) / value1 * 100
        self.assertEqual(percent_change(value1, value2), expected)

        # With frac=True
        expected_frac = (value2 - value1) / value1
        self.assertEqual(percent_change(
            value1, value2, frac=True), expected_frac)


class TestPercentChangeFromTarget(unittest.TestCase):
    """Test cases for the percent_changefrom_target function."""

    def test_basic_positive_numbers(self):
        """Test with basic positive numbers."""
        self.assertEqual(percent_changefrom_target(5, 7), -40.0)
        self.assertEqual(percent_changefrom_target(10, 15), -50.0)
        self.assertEqual(percent_changefrom_target(100, 90), 10.0)
        self.assertEqual(percent_changefrom_target(200, 150), 25.0)

    def test_negative_numbers(self):
        """Test with negative numbers."""
        self.assertEqual(percent_changefrom_target(-10, -15), -50.0)
        self.assertEqual(percent_changefrom_target(-10, -5), 50.0)
        self.assertEqual(percent_changefrom_target(-100, 100), 200.0)
        self.assertEqual(percent_changefrom_target(100, -100), 200.0)

    def test_zero_values(self):
        """Test with zero values."""
        with self.assertRaises(ZeroDivisionError):
            percent_changefrom_target(0, 10)

        self.assertEqual(percent_changefrom_target(10, 0), 100.0)

    def test_fraction_output(self):
        """Test with fraction output flag."""
        self.assertEqual(percent_changefrom_target(5, 7, frac=True), -0.4)
        self.assertEqual(percent_changefrom_target(10, 15, frac=True), -0.5)
        self.assertEqual(percent_changefrom_target(100, 90, frac=True), 0.1)
        self.assertEqual(percent_changefrom_target(200, 150, frac=True), 0.25)

    def test_large_and_small_numbers(self):
        """Test with very large and very small numbers."""
        self.assertEqual(percent_changefrom_target(1e6, 2e6), -100.0)
        self.assertEqual(percent_changefrom_target(1e-6, 2e-6), -100.0)
        self.assertEqual(percent_changefrom_target(1e6, 5e5), 50.0)
        self.assertEqual(percent_changefrom_target(1e-6, 5e-7), 50.0)

    def test_same_values(self):
        """Test with same values for target and actual."""
        self.assertEqual(percent_changefrom_target(10, 10), 0.0)
        self.assertEqual(percent_changefrom_target(-10, -10), 0.0)
        self.assertEqual(percent_changefrom_target(0.5, 0.5), 0.0)
        self.assertEqual(percent_changefrom_target(10, 10, frac=True), 0.0)

    def test_floating_point_precision(self):
        """Test with floating point precision."""
        self.assertAlmostEqual(percent_changefrom_target(
            3.33, 1.11), 66.6667, places=4)
        self.assertAlmostEqual(percent_changefrom_target(
            1.11, 3.33), -200.0, places=4)
        self.assertAlmostEqual(percent_changefrom_target(
            3.33, 1.11, frac=True), 0.6667, places=4)
        self.assertAlmostEqual(percent_changefrom_target(
            1.11, 3.33, frac=True), -2.0, places=4)

    def test_formula_verification(self):
        """Verify the formula implementation is correct."""
        # Formula: perchg = (target_val - actual_val)/target_val * 100
        target = 50
        actual = 40
        expected = (target - actual) / target * 100
        self.assertEqual(percent_changefrom_target(target, actual), expected)

        # With frac=True
        expected_frac = (target - actual) / target
        self.assertEqual(percent_changefrom_target(
            target, actual, frac=True), expected_frac)


class TestPercentDiff(unittest.TestCase):
    """Test cases for the percent_diff function."""

    def test_basic_positive_numbers(self):
        """Test with basic positive numbers."""
        self.assertAlmostEqual(
            percent_diff(5, 7), 33.3333, places=4)
        self.assertAlmostEqual(
            percent_diff(10, 20), 66.6667, places=4)
        self.assertAlmostEqual(
            percent_diff(100, 150), 40.0, places=4)
        self.assertEqual(percent_diff(10, 10), 0.0)

    def test_negative_values(self):
        """Test with negative values which should raise an assertion error."""
        with self.assertRaises(AssertionError):
            percent_diff(-5, 7)
        with self.assertRaises(AssertionError):
            percent_diff(5, -7)
        with self.assertRaises(AssertionError):
            percent_diff(-5, -7)

    def test_zero_values(self):
        """Test with zero values."""
        self.assertEqual(percent_diff(0, 10), 200.0)
        self.assertEqual(percent_diff(10, 0), 200.0)
        with self.assertRaises(ZeroDivisionError):
            percent_diff(0, 0)

    def test_fraction_output(self):
        """Test with fraction output flag."""
        self.assertAlmostEqual(percent_diff(
            5, 7, frac=True), 0.3333, places=4)
        self.assertAlmostEqual(percent_diff(
            10, 20, frac=True), 0.6667, places=4)
        self.assertEqual(percent_diff(100, 150, frac=True), 0.4)
        self.assertEqual(percent_diff(10, 10, frac=True), 0.0)

    def test_large_and_small_numbers(self):
        """Test with very large and very small numbers."""
        self.assertAlmostEqual(percent_diff(1e6, 3e6), 100.0, places=4)
        self.assertAlmostEqual(percent_diff(1e-6, 3e-6), 100.0, places=4)
        self.assertAlmostEqual(percent_diff(2e6, 6e5), 107.6923, places=4)
        self.assertAlmostEqual(percent_diff(2e-6, 6e-7), 107.6923, places=4)

    def test_order_invariance(self):
        """Test that the order of arguments doesn't matter."""
        self.assertEqual(percent_diff(5, 7), percent_diff(7, 5))
        self.assertEqual(percent_diff(100, 150),
                         percent_diff(150, 100))

    def test_formula_verification(self):
        """Verify the formula implementation is correct."""
        # Formula: perdiff = abs(value1 - value2)/((value1 + value2)/2.0) * 100
        value1 = 50
        value2 = 75
        expected = abs(value1 - value2) / \
            ((value1 + value2) / 2.0) * 100
        self.assertEqual(percent_diff(value1, value2), expected)

        # With frac=True
        expected_frac = abs(value1 - value2) / \
            ((value1 + value2) / 2.0)
        self.assertEqual(percent_diff(
            value1, value2, frac=True), expected_frac)


class TestPercentError(unittest.TestCase):
    """Test cases for the percent_error function."""

    def test_basic_positive_numbers(self):
        """Test with basic positive numbers."""
        self.assertEqual(percent_error(100, 110), 10.0)
        self.assertEqual(percent_error(50, 75), 50.0)
        self.assertEqual(percent_error(200, 150), 25.0)
        self.assertEqual(percent_error(10, 10), 0.0)

    def test_negative_numbers(self):
        """Test with negative numbers."""
        self.assertEqual(percent_error(-10, -6), 40.0)
        self.assertEqual(percent_error(-20, -10), 50.0)
        self.assertEqual(percent_error(-100, -150), 50.0)
        self.assertEqual(percent_error(-50, 50), 200.0)

    def test_zero_values(self):
        """Test with zero values."""
        with self.assertRaises(ZeroDivisionError):
            percent_error(0, 10)

        self.assertEqual(percent_error(10, 0), 100.0)

    def test_fraction_output(self):
        """Test with fraction output flag."""
        self.assertEqual(percent_error(100, 110, frac=True), 0.1)
        self.assertEqual(percent_error(50, 75, frac=True), 0.5)
        self.assertEqual(percent_error(200, 150, frac=True), 0.25)
        self.assertEqual(percent_error(10, 10, frac=True), 0.0)

    def test_large_and_small_numbers(self):
        """Test with very large and very small numbers."""
        self.assertEqual(percent_error(1e6, 2e6), 100.0)
        self.assertEqual(percent_error(1e-6, 2e-6), 100.0)
        self.assertEqual(percent_error(1e6, 5e5), 50.0)
        self.assertEqual(percent_error(1e-6, 5e-7), 50.0)

    def test_floating_point_precision(self):
        """Test with floating point precision."""
        self.assertAlmostEqual(percent_error(
            3.33, 4.44), 33.3333, places=4)
        self.assertAlmostEqual(
            percent_error(4.44, 3.33), 25.0, places=4)
        self.assertAlmostEqual(percent_error(
            3.33, 4.44, frac=True), 0.3333, places=4)
        self.assertAlmostEqual(percent_error(
            4.44, 3.33, frac=True), 0.25, places=4)

    def test_formula_verification(self):
        """Verify the formula implementation is correct."""
        # Formula: pererr = abs(value2 - value1)/abs(value1) * 100
        value1 = 50
        value2 = 75
        expected = abs(value2 - value1) / abs(value1) * 100
        self.assertEqual(percent_error(value1, value2), expected)

        # With frac=True
        expected_frac = abs(value2 - value1) / abs(value1)
        self.assertEqual(percent_error(
            value1, value2, frac=True), expected_frac)


class TestSnake2CamelCase(unittest.TestCase):
    """Test cases for the snake2camel_case function."""

    def test_basic_conversion(self):
        """Test basic snake_case to CamelCase conversion."""
        self.assertEqual(snake2camel_case(
            'team_member'), 'TeamMember')
        self.assertEqual(snake2camel_case('user_id'), 'UserId')
        self.assertEqual(snake2camel_case(
            'first_name_last_name'), 'FirstNameLastName')

    def test_with_spaces(self):
        """Test conversion with addspace=True."""
        self.assertEqual(snake2camel_case(
            'team_member', addspace=True), 'Team Member')
        self.assertEqual(snake2camel_case(
            'user_id', addspace=True), 'User Id')
        self.assertEqual(snake2camel_case(
            'first_name_last_name', addspace=True), 'First Name Last Name')

    def test_edge_cases(self):
        """Test edge cases like empty string, single word."""
        self.assertEqual(snake2camel_case(''), '')
        self.assertEqual(snake2camel_case('word'), 'Word')
        self.assertEqual(snake2camel_case(
            '_leading_underscore'), 'LeadingUnderscore')
        self.assertEqual(snake2camel_case(
            'trailing_underscore_'), 'TrailingUnderscore')
        self.assertEqual(snake2camel_case(
            '__double__multiple_underscores__'), 'DoubleMultipleUnderscores')

    def test_edge_cases_with_space(self):
        """Test edge cases with addspace=True."""
        self.assertEqual(snake2camel_case('', addspace=True), '')
        self.assertEqual(snake2camel_case('word', addspace=True), 'Word')
        self.assertEqual(snake2camel_case('_leading_underscore',
                         addspace=True), ' Leading Underscore')
        self.assertEqual(snake2camel_case(
            'trailing_underscore_', addspace=True), 'Trailing Underscore ')
        self.assertEqual(snake2camel_case('__double__multiple_underscores__',
                         addspace=True), '  Double  Multiple Underscores  ')
        self.assertEqual(snake2camel_case('_word_', addspace=True), ' Word ')

    def test_with_numbers(self):
        """Test with numbers and special characters."""
        self.assertEqual(snake2camel_case('user_123'), 'User123')
        self.assertEqual(snake2camel_case(
            'item_1_name_2'), 'Item1Name2')
        self.assertEqual(snake2camel_case(
            'user_123', addspace=True), 'User 123')

    def test_already_camel_case(self):
        """Test with input that's already in CamelCase or other formats."""
        self.assertEqual(snake2camel_case(
            'already_Capitalized_Words'), 'AlreadyCapitalizedWords')
        self.assertEqual(snake2camel_case(
            'UPPERCASE_WORDS'), 'UppercaseWords')


class TestCamel2SnakeCase(unittest.TestCase):
    """Test cases for the camel2snake_case function."""

    def test_basic_conversion(self):
        """Test basic CamelCase to snake_case conversion."""
        self.assertEqual(camel2snake_case(
            'TeamMember'), 'team_member')
        self.assertEqual(camel2snake_case('UserId'), 'user_id')
        self.assertEqual(camel2snake_case(
            'FirstNameLastName'), 'first_name_last_name')

    def test_edge_cases(self):
        """Test edge cases like empty string, single word, single letter."""
        self.assertEqual(camel2snake_case(''), '')
        self.assertEqual(camel2snake_case('Word'), 'word')
        self.assertEqual(camel2snake_case('word'), 'word')
        self.assertEqual(camel2snake_case('W'), 'w')
        self.assertEqual(camel2snake_case('w'), 'w')

    def test_with_numbers(self):
        """Test with numbers in various positions."""
        self.assertEqual(camel2snake_case('User123'), 'user123')
        self.assertEqual(camel2snake_case(
            'Item1Name2'), 'item1_name2')
        self.assertEqual(camel2snake_case('123User'), '123_user')
        self.assertEqual(camel2snake_case('User123ID'), 'user123_id')
        self.assertEqual(camel2snake_case('Version2Point0'), 'version2_point0')

    def test_consecutive_uppercase(self):
        """Test with consecutive uppercase letters and acronyms."""
        self.assertEqual(camel2snake_case(
            'HTTPRequest'), 'http_request')
        self.assertEqual(camel2snake_case(
            'APIEndpoint'), 'api_endpoint')
        self.assertEqual(camel2snake_case('iOS'), 'i_os')
        self.assertEqual(camel2snake_case('NASAProgram'),
                         'nasa_program')
        self.assertEqual(camel2snake_case('ProgramNASA'), 'program_nasa')
        self.assertEqual(camel2snake_case('MyNASAProgram'),
                         'my_nasa_program')
        self.assertEqual(camel2snake_case('ABCHttp'), 'abc_http')
        self.assertEqual(camel2snake_case('SimpleXMLParser'),
                         'simple_xml_parser')
        self.assertEqual(camel2snake_case('XMLHTTPRequest'), 'xmlhttp_request')
        self.assertEqual(camel2snake_case('AValue'), 'a_value')
        self.assertEqual(camel2snake_case('ValueA'), 'value_a')
        self.assertEqual(camel2snake_case('ABC'), 'abc')
        self.assertEqual(camel2snake_case('ID'), 'id')

    def test_already_snake_case(self):
        """Test with input that's already in snake_case."""
        self.assertEqual(camel2snake_case(
            'already_snake_case'), 'already_snake_case')
        self.assertEqual(camel2snake_case(
            'snake_Case_Mixed'), 'snake_case_mixed')

    def test_mixed_case_patterns(self):
        """Test with mixed case patterns."""
        self.assertEqual(camel2snake_case(
            'mixedCASEPattern'), 'mixed_case_pattern')
        self.assertEqual(camel2snake_case(
            'PascalCaseExample'), 'pascal_case_example')
        self.assertEqual(camel2snake_case(
            'camelCaseExample'), 'camel_case_example')


class TestMround(unittest.TestCase):

    """Test cases for the mround function."""

    def test_basic_integer_values(self):
        """Test basic integer values with default base of 5."""
        self.assertEqual(mround(3332), 3330)
        self.assertEqual(mround(3335), 3335)
        self.assertEqual(mround(3338), 3340)
        self.assertEqual(mround(0), 0)
        self.assertEqual(mround(5), 5)
        self.assertEqual(mround(7), 5)
        self.assertEqual(mround(10), 10)

    def test_negative_integer_values(self):
        """Test negative integer values with default base of 5."""
        self.assertEqual(mround(-3332), -3330)
        self.assertEqual(mround(-3335), -3335)
        self.assertEqual(mround(-3338), -3340)
        self.assertEqual(mround(-5), -5)
        self.assertEqual(mround(-7), -5)

    def test_float_values(self):
        """Test float values with various bases."""
        self.assertAlmostEqual(mround(2.332, 0.005), 2.33)
        self.assertAlmostEqual(mround(2.335, 0.005), 2.335)
        self.assertAlmostEqual(mround(2.338, 0.005), 2.34)
        self.assertAlmostEqual(mround(1.5, 0.1), 1.5)
        self.assertAlmostEqual(mround(1.52, 0.1), 1.5)
        self.assertAlmostEqual(mround(1.55, 0.1), 1.6)
        self.assertAlmostEqual(mround(1.58, 0.1), 1.6)

    def test_negative_float_values(self):
        """Test negative float values with various bases."""
        self.assertAlmostEqual(mround(-2.332, 0.005), -2.33)
        self.assertAlmostEqual(mround(-2.335, 0.005), -2.335)
        self.assertAlmostEqual(mround(-2.338, 0.005), -2.34)
        self.assertAlmostEqual(mround(-1.5, 0.1), -1.5)
        self.assertAlmostEqual(mround(-1.52, 0.1), -1.5)
        self.assertAlmostEqual(mround(-1.55, 0.1), -1.6)
        self.assertAlmostEqual(mround(-1.58, 0.1), -1.6)

    def test_custom_integer_base(self):
        """Test with custom integer base values."""
        self.assertEqual(mround(42, 10), 40)
        self.assertEqual(mround(45, 10), 50)
        self.assertEqual(mround(137, 25), 125)
        self.assertEqual(mround(138, 25), 150)
        self.assertEqual(mround(99, 33), 99)  # closest is 99
        self.assertEqual(mround(100, 33), 99)  # closest is 99

    def test_numpy_array(self):
        """Test with numpy array input."""
        arr = np.array([1006, 987, 1024, 1023, 978])
        np.testing.assert_array_equal(
            mround(arr), np.array([1005., 985., 1025., 1025., 980.]))

        arr = np.array([1.42, 1.45, 1.47])
        np.testing.assert_array_equal(
            mround(arr, 0.1), np.array([1.4, 1.5, 1.5]))

    def test_numpy_array_with_different_base(self):
        """Test numpy array with different base values."""
        arr = np.array([42, 45, 137, 138, 99])
        np.testing.assert_array_equal(
            mround(arr, 10), np.array([40., 50., 140., 140., 100.]))

        arr = np.array([2.332, 2.335, 2.338])
        np.testing.assert_array_almost_equal(
            mround(arr, 0.005), np.array([2.330, 2.335, 2.340]))

    def test_invalid_inputs(self):
        """Test handling of invalid inputs."""
        with self.assertRaises(ValueError):
            mround([1, 2, 3])

        with self.assertRaises(ValueError):
            mround((1, 2, 3))

        # Base of zero should raise an error
        with self.assertRaises(Exception):
            mround(100, 0)

    def test_edge_cases(self):
        """Test edge cases like very large or small numbers."""
        self.assertEqual(mround(1e9, 1e6), 1e9)
        self.assertAlmostEqual(mround(1e-6, 1e-9), 1e-6)

        # Very small base with large number
        self.assertEqual(mround(1000, 0.001), 1000.0)

        # Very large base with small number
        self.assertEqual(mround(0.001, 1000), 0)

    def test_formula_verification(self):
        """Verify the formula implementation is correct."""
        # Formula: ret = base * round(x/base)
        x = 137
        base = 25
        expected = base * round(x / base)
        self.assertEqual(mround(x, base), expected)

        x = 2.338
        base = 0.005
        expected = base * round(x / base)
        self.assertAlmostEqual(mround(x, base), expected)

        # For numpy array
        arr = np.array([1006, 987, 1024])
        base = 5
        expected = base * np.around(arr / base)
        np.testing.assert_array_equal(mround(arr, base), expected)


if __name__ == '__main__':
    unittest.main()
