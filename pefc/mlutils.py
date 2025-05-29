""" Common useful utilities including machine learning utilities
    for data preprocessing, feature engineering, and model evaluation.
    This module includes functions for calculating percentage change,
    percentage difference, and percentage error. It also includes
    functions for converting between snake case and camel case.
    The functions are designed to be used in a variety of contexts,
    including data analysis, machine learning, and general programming.
    The functions are implemented in Python and are intended to be
    easy to use and understand.
"""
import math
import datetime
from typing import Union, Any

# NOTE: The percent_* formulas are based on the following references.
# https://www.calculatorsoup.com/calculators/algebra/percent-difference-calculator.php
# https://en.wikipedia.org/wiki/Relative_change_and_difference


def percent_change(value1: float, value2: float, frac: bool = False) -> float:
    """ Return the percentage change between two values. The denominator
        or base value is value1.
        This is for checking the material usage variance to a standard value,
        the value1 parameter.

        value1: float, base value or standard value.

        value2: float, changed value.

        frac: bool, Default is False. Set to True returns a fraction
            instead of percentages. This is useful for performing
            calculations on spreadsheets.

        Equation
        --------
        percent_change = (value2 - value1)/value1

        This is the same as the HP calculator's Δ% as per wikipedia
        value1 ENTER value2 Δ% e.g. -10 ENTER -6 Δ% = -40.
        Don't use relative percentage change i.e (value2 - value1)/abs(value1).

        Returns
        -------
        float, percentage change value in % or fraction.

        Example
        -------
        >>> percent_change(-10, -6)
        -40.0
        >>> percent_change(5, 7)
        40.0
        >>> percent_change(100, 110)
        10.0
        >>> percent_change(100, 110, frac=True)
        0.1

    """
    perchg = (value2 - value1)/value1
    if frac is False:
        perchg *= 100
    return perchg


def percent_changefrom_target(target_val: float, actual_val: float,
                              frac: bool = False) -> float:
    """ Return the percentage change between target and actual value.
        The denominator is the target value. The difference between
        percent_change and percent_changefrom_target is that the latter is
        used to adjust a recipe to a targeted percentage value. This is useful
        for formulation of a product to meet it active ingredients' percentage.

        target_val: float, target value

        actual_val: float, current actual value

        frac: bool, Default is False. Set to True returns a fraction
            instead of percentages. This is useful for performing
            calculations on spreadsheets.

        Equation
        --------
        perchg_from_target = (target_val - actual_val)/target_val
        or (value1 - value2)/value1 using percent_change notation.

        Returns
        -------
        float, percentage change from target value in % or fraction.

        Example
        -------
        >>> percent_changefrom_target(5, 7)
        -40.0
        >>> percent_changefrom_target(5, 7, frac=True)
        -0.4
        """
    perchg = (target_val - actual_val)/target_val
    if frac is False:
        perchg *= 100
    return perchg


def percent_diff(value1: float, value2: float, frac: bool = False) -> float:
    """ Return the percentage difference between two values. The denominator
        is the average of value1 and value2.

        value1: float, first value must be >= 0

        value2: float, second value must be >= 0

        frac: bool, Default is False. Set to True returns a fraction
            instead of percentages. This is useful for performing
            calculations on spreadsheets.

        Equation
        --------
        percent_diff = abs(value1 - value2)/((value1 + value2)/2.0)

        Returns
        -------
        float, absolute value of the difference in percentages

        Example
        -------
        >>> percent_diff(5, 7)
        33.33333333333333
        >>> percent_diff(5, 7, frac=True)
        0.3333333333333333
        """
    assert value1 >= 0 and value2 >= 0, 'Values must not be negative'
    perdiff = abs(value1 - value2)/((value1 + value2)/2.0)
    if frac is False:
        perdiff *= 100
    return perdiff


def percent_error(value1: float, value2: float, frac: bool = False) -> float:
    """ Return the percentage error between two values. The denominator
        or theoretical value is value1.

        value1: float, theoretical or base value

        value2: float, measured value

        frac: bool, Default is False. Set to True returns a fraction
            instead of percentages. This is useful for performing
            calculations on spreadsheets.

        Equation
        --------
        percent_error = abs(value2 - value1)/abs(value1)

        percent_error = |experimental - theoretical| / |theoretical|
        as per wikipedia article.

        Returns
        -------
        float, percentage error value

        Example
        -------
        >>> percent_error(-10, -6)
        40.0
        >>> percent_error(100, 110)
        10.0
        >>> percent_error(100, 110, frac=True)
        0.1

    """
    pererr = abs(value2 - value1)/abs(value1)
    if frac is False:
        pererr *= 100
    return pererr


def snake2camel_case(label: str, addspace=False) -> str:
    """ Convert a snake case string to camel case. e.g. team_member becomes
        TeamMember and vice versa. If addspace is True, then the first letter
        of each word is capitalized and a space is added between words.

        label: str, input string

        addspace: bool, Default is False. Set to True adds a space between
            words.

        Returns
        -------
        str, camel case string

        Example
        -------
        >>> snake2camel_case('team_member')
        'TeamMember'
        >>> snake2camel_case('team_member', addspace=True)
        'Team Member'
    """
    if addspace:
        return label.replace('_', ' ').title()
    else:
        return ''.join(word.title() for word in label.split('_'))


def camel2snake_case(label: str) -> str:
    """ Convert a camel case string to snake case. e.g. TeamMember becomes
        team_member.

        label: str, input string

        Returns
        -------
        str, snake case string

        Example
        -------
        >>> camel2snake_case('TeamMember')
        'team_member'
        >>> camel2snake_case('TeamMemberID')
        'team_member_id'
        >>> camel2snake_case('ABC')
        'abc'
    """
    import re
    # This pattern looks for lowercase followed by uppercase or
    # any character followed by uppercase letter followed by lowercase
    pattern = re.compile(r'([a-z0-9])([A-Z])|([A-Z])([A-Z][a-z])')

    # Insert underscore and convert the entire string to lowercase
    result = pattern.sub(r'\1\3_\2\4', label)
    return result.lower()


def _to_fractional_day(value: Any) -> float:
    """
    Converts a given value to its representation as a fraction of a day,
    or returns it directly if it's already a numeric type.
    Handles numbers, time strings ("HH:MM", "HH:MM:SS", numeric strings),
    datetime.time objects, and datetime.timedelta objects.

    Args:
        value: The value to convert. Can be int, float, str,
               datetime.time, or datetime.timedelta.

    Returns:
        The value as a float. For time-related inputs, this is the
        fraction of a 24-hour day (e.g., 12:00 PM = 0.5).

    Raises:
        TypeError: If the input value type is not supported.
        ValueError: If a string input cannot be parsed as a number or
            valid time format.
    """
    if isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, datetime.timedelta):
        # Convert timedelta to fraction of a day
        return value.total_seconds() / (24.0 * 60.0 * 60.0)
    elif isinstance(value, datetime.time):
        # Convert datetime.time to fraction of a day
        return (value.hour + value.minute/60.0 + value.second/3600.0
                + value.microsecond/3600000000.0) / 24.0
    elif isinstance(value, str):
        try:
            # Attempt to convert string to float directly first
            # (e.g., "0.5", "1.25")
            return float(value)
        except ValueError:
            # If not a float, try parsing as "HH:MM:SS" or "HH:MM"
            parts = value.split(':')
            if 1 < len(parts) < 4:  # Must be HH:MM or HH:MM:SS
                try:
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    seconds = int(parts[2]) if len(parts) == 3 else 0

                    # Validate minutes and seconds, hours can be >= 0
                    # (e.g., "25:00")
                    if not (hours >= 0 and 0 <= minutes < 60
                            and 0 <= seconds < 60):
                        raise ValueError(
                            "Time string components out of valid range "
                            "(minutes/seconds must be 0-59, hours >=0)."
                        )

                    # Calculate total seconds from HH:MM:SS and
                    # convert to fraction of a day
                    total_seconds_input = hours * 3600 + minutes * 60 + seconds
                    return total_seconds_input / (24.0 * 3600.0)
                # Catches non-integer parts or range errors
                except ValueError as e_parse:
                    raise ValueError(
                        f"Invalid time string format '{value}': {e_parse}. "
                        "Expected HH:MM, HH:MM:SS, or a numeric string."
                    ) from e_parse  # Keep original parsing error context
            else:
                # String is not a direct float and not in H:M(:S) format
                raise ValueError(
                    f"Invalid string format '{value}'. "
                    "Expected a numeric string, "
                    "or time in HH:MM or HH:MM:SS format."
                )
    else:
        raise TypeError(
            f"Unsupported type for MROUND input: {type(value)}. Must be  "
            "numeric, time string, datetime.time, or datetime.timedelta."
        )


def mround(
        number: Union[float, int, str, datetime.time, datetime.timedelta],
        multiple: Union[float, int, str, datetime.time, datetime.timedelta]
) -> float:
    """
    Replicates the behavior of MS Excel's MROUND function, including support
    for time values.
    Rounds 'number' to the nearest specified 'multiple'.

    'number' and 'multiple' can be:
    - Numeric (int, float).
    - Time strings (e.g., "10:35", "0:15:30", "26:00").
    - Numeric strings (e.g., "1.25", "0.5").
    - datetime.time objects.
    - datetime.timedelta objects.

    Args:
        number: The value to round.
        multiple: The multiple to which you want to round the number.

    Returns:
        The number rounded to the nearest multiple, as a float.
        If inputs were time-based, the float represents the fraction of a day
        (e.g., 0.5 for noon).

    Raises:
        TypeError: If number or multiple are of an unsupported type after
            conversion attempts.
        ValueError: If number and multiple have different signs
                    (and neither is zero)
                    after conversion to numeric, or if string parsing fails.
    """
    try:
        # Convert inputs to their numerical float representations
        num_float = _to_fractional_day(number)
        mult_float = _to_fractional_day(multiple)
    except (TypeError, ValueError) as e:
        # Propagate errors from the conversion helper
        raise e

    # Excel MROUND behavior for zero inputs:
    # MROUND(n, 0) is 0
    # MROUND(0, m) is 0
    if mult_float == 0.0:
        return 0.0
    if num_float == 0.0:  # This also covers MROUND(0,0)
        return 0.0

    # Check for different signs.
    # math.copysign(1.0, x) returns 1.0 if x is positive/zero,
    # -1.0 if x is negative.
    # This check applies after inputs are converted to floats.
    if math.copysign(1.0, num_float) != math.copysign(1.0, mult_float):
        raise ValueError(
            "MROUND arguments 'number' and 'multiple' must have the same sign "
            "after conversion to numeric values."
        )

    # Core rounding logic:
    # If signs are the same, the quotient (num_float / mult_float)
    # will be positive.
    quotient = num_float / mult_float

    # Round half away from zero. Since 'quotient' is positive here
    # if signs are same,
    # math.floor(quotient + 0.5) correctly implements "round half up"
    # for positive quotients.
    # If num_float and mult_float were negative, quotient is still positive,
    # and the result `rounded_quotient * mult_float` will correctly
    # be negative.
    rounded_quotient_val = math.floor(quotient + 0.5)

    result = rounded_quotient_val * mult_float
    return result


def format_excel_time_number(excel_time_number: float) -> str:
    """
    Helper function to format an Excel-style time number (fraction of a day)
    into a string representation like "HH:MM:SS" or "[H]:MM:SS" if >24h.
    Rounds to the nearest second for display.
    """
    if not isinstance(excel_time_number, (int, float)):
        return "Invalid input (not a number)"

    is_negative = excel_time_number < 0
    if is_negative:
        excel_time_number = -excel_time_number

    # Round to the nearest second before calculations
    total_seconds_rounded = round(excel_time_number * 86400.0)

    # Calculate total hours, minutes, and seconds from the
    # rounded total seconds
    display_hours = int(total_seconds_rounded // 3600)
    display_minutes = int((total_seconds_rounded % 3600) // 60)
    display_seconds = int(total_seconds_rounded % 60)

    sign = "-" if is_negative else ""
    return (f"{sign}{display_hours:02d}:{display_minutes:02d}"
            f":{display_seconds:02d}")


def _test():
    import doctest
    print("Doctest results:")
    print("===============")
    print("Test results:")
    print(doctest.testmod())


if __name__ == '__main__':
    _test()
    print("\nmlutils Test assertions:")
    print("======================")
    assert percent_change(100, 110) == 10.0, "percent_change(100, 110) failed"
    assert percent_change(
        100, 110, frac=True) == 0.1, \
        "percent_change(100, 110, frac=True) failed"
    assert percent_change(5, 7) == 40.0, "percent_change(5, 7) failed"

    # Using almost equal for floating point comparisons
    def assert_almost_equal(a, b, places=7):
        epsilon = 10**(-places)
        assert abs(a - b) < epsilon, f"{a} != {b} within {places} places"

    assert_almost_equal(percent_diff(5, 7), 33.33333333333333, places=4)
    assert_almost_equal(percent_diff(5, 7, frac=True),
                        0.3333333333333333, places=4)

    assert percent_error(100, 110) == 10.0, "percent_error(100, 110) failed"
    assert percent_error(
        100, 110, frac=True) == 0.1, \
        "percent_error(100, 110, frac=True) failed"
    assert percent_changefrom_target(
        5, 7) == -40.0, "percent_changefrom_target(5, 7) failed"
    assert percent_changefrom_target(
        5, 7, frac=True) == -0.4, \
        "percent_changefrom_target(5, 7, frac=True) failed"

    assert snake2camel_case(
        'team_member') == 'TeamMember', \
        "snake2camel_case('team_member') failed"
    assert snake2camel_case(
        'team_member', addspace=True) == 'Team Member', \
        "snake2camel_case('team_member', addspace=True) failed"
    assert camel2snake_case(
        'TeamMember') == 'team_member', \
        "camel2snake_case('TeamMember') failed"
    assert camel2snake_case(
        'TeamMemberID') == 'team_member_id', \
        "camel2snake_case('TeamMemberID') failed"
    assert camel2snake_case(
        'HTTPRequest') == 'http_request', \
        "camel2snake_case('HTTPRequest') failed"
    assert camel2snake_case(
        'APIEndpoint') == 'api_endpoint', \
        "camel2snake_case('APIEndpoint') failed"
    assert camel2snake_case(
        'NASAProgram') == 'nasa_program', \
        "camel2snake_case('NASAProgram') failed"
    assert camel2snake_case(
        'MyNASAProgram') == 'my_nasa_program', \
        "camel2snake_case('MyNASAProgram') failed"
    assert camel2snake_case(
        'SimpleXMLParser') == 'simple_xml_parser', \
        "camel2snake_case('SimpleXMLParser') failed"
    assert camel2snake_case('ABC') == 'abc', "camel2snake_case('ABC') failed"

    # Numeric Tests
    assert mround(10, 3) == 9.0, f"Expected 9.0, got {mround(10, 3)}"
    assert mround(11, 3) == 12.0, f"Expected 12.0, got {mround(11, 3)}"
    assert abs(mround(1.3, 0.2) -
               1.4) < 1e-10, f"Expected 1.4, got {mround(1.3, 0.2)}"
    assert mround(-10, -3) == -9.0, f"Expected -9.0, got {mround(-10, -3)}"
    assert mround(-11, -3) == -12.0, f"Expected -12.0, got {mround(-11, -3)}"
    assert abs(mround(6.25, 2.5) -
               7.5) < 1e-10, f"Expected 7.5, got {mround(6.25, 2.5)}"

    # Zero Value Tests
    assert mround(0, 5) == 0.0, f"Expected 0.0, got {mround(0, 5)}"
    assert mround(5, 0) == 0.0, f"Expected 0.0, got {mround(5, 0)}"
    assert mround(0, 0) == 0.0, f"Expected 0.0, got {mround(0, 0)}"

    # Mid-Point Value Tests
    assert mround(6.05, 0.1), f"Expected 6.1, got {mround(6.05, 0.1)}"
    assert mround(7.05, 0.1), f"Expected 7.1, got {mround(7.05, 0.1)}"

    # Time Rounding Tests
    def assert_time_mround(num, mult, expected_time_str, tolerance=1e-8):
        """Helper function to assert time mround results."""
        result = mround(num, mult)
        formatted_result = format_excel_time_number(result)
        assert formatted_result == expected_time_str, \
            f"mround({num}, {mult}) = {result} " \
            f"(formatted: {formatted_result}), expected {expected_time_str}"

    # Test 1: Round "10:35 AM" to nearest 15 minutes -> 10:30 AM
    assert_time_mround("10:35", "0:15", "10:30:00")

    # Test 2: Round "10:38 AM" to nearest 15 minutes -> 10:45 AM
    assert_time_mround("10:38:00", datetime.timedelta(minutes=15), "10:45:00")

    # Test 3: Round datetime.time object to nearest minute
    dt_time_obj = datetime.time(10, 37, 30)
    one_minute_td = datetime.timedelta(minutes=1)
    assert_time_mround(dt_time_obj, one_minute_td, "10:38:00")

    # Test 4: Round datetime.time object (10:37:29)
    # to nearest minute -> 10:37:00
    dt_time_obj_2 = datetime.time(10, 37, 29)
    assert_time_mround(dt_time_obj_2, "0:01:00", "10:37:00")

    # Test 5: Round float representing time to nearest 30 minutes
    assert_time_mround(0.44097222, "0:30", "10:30:00")

    # Test 6: Rounding time over 24 hours: "25:35" to nearest "0:15" -> "25:30"
    assert_time_mround("25:35", "0:15", "25:30:00")

    # Test 7: Rounding "25:38" to nearest "0:15" -> "25:45"
    assert_time_mround("25:38", "0:15", "25:45:00")

    # Test 8: Using numeric string for multiple
    assert_time_mround("10:35", "0.010416666666666666", "10:30:00")

    # Test 9: Negative time values
    assert_time_mround(-0.44097222,
                       datetime.timedelta(minutes=-15), "-10:30:00")

    # Error Handling Tests
    error_test_cases = [
        (10, -3, ValueError),
        ("text", 5, ValueError),
        (5, "text", ValueError),
        (datetime.time(10, 0), datetime.timedelta(minutes=-15), ValueError),
        ("10:00", "invalid_time_str", ValueError),
        ("10:70", "0:15", ValueError),
        ("abc:def", "0:15", ValueError),
        ("1.2.3", "0:15", ValueError)
    ]

    for num_err, mult_err, expected_error in error_test_cases:
        try:
            result = mround(num_err, mult_err)
            assert False, f"Expected {expected_error.__name__}"\
                f" for mround({num_err}, {mult_err}), but got {result}"
        except expected_error:
            pass  # Expected error occurred
        except Exception as e:
            assert False, f"Expected {expected_error.__name__}"\
                f" for mround({num_err}, {mult_err}),"\
                f" but got {type(e).__name__}: {e}"

    print("All assertions passed!")
