import unittest
from pefc.mlutils import (percent_change, percent_changefrom_target,
                          percent_diff, percent_error, snake2camel_case,
                          camel2snake_case)


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
        self.assertEqual(percent_diff(1e6, 3e6), 100.0)
        self.assertEqual(percent_diff(1e-6, 3e-6), 100.0)
        self.assertEqual(percent_diff(
            2e6, 6e5), 107.69230769230771)
        self.assertEqual(percent_diff(
            2e-6, 6e-7), 107.69230769230771)

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
        self.assertEqual(snake2camel_case('_word_'), 'Word')
        self.assertEqual(snake2camel_case(
            '__double__underscore__'), 'DoubleUnderscore')

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
            'already_Capitalized_words'), 'AlreadyCapitalizedWords')
        self.assertEqual(snake2camel_case(
            'UPPERCASE_WORDS'), 'UPPERCASEWORDS')


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
        """Test edge cases like empty string, single word."""
        self.assertEqual(camel2snake_case(''), '')
        self.assertEqual(camel2snake_case('Word'), 'word')
        self.assertEqual(camel2snake_case('word'), 'word')
        self.assertEqual(camel2snake_case('w'), 'w')

    def test_with_numbers(self):
        """Test with numbers and special characters."""
        self.assertEqual(camel2snake_case('User123'), 'user123')
        self.assertEqual(camel2snake_case(
            'Item1Name2'), 'item1_name2')

    def test_consecutive_uppercase(self):
        """Test with consecutive uppercase letters."""
        self.assertEqual(camel2snake_case(
            'HTTPRequest'), 'http_request')
        self.assertEqual(camel2snake_case(
            'APIEndpoint'), 'api_endpoint')
        self.assertEqual(camel2snake_case('iOS'), 'i_os')

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


if __name__ == '__main__':
    unittest.main()
