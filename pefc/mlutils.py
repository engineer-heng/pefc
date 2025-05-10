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
import numpy as np


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


def mround(x, base=5):
    """ Similar to Excel mround function

        x: numpy.darray of values to be rounded

        base: int or float specifying multiples of the base value.
        Default is 5.

        return: numpy.darray rounded to the required base value

        Example
        -------
        >>> mround(3332)
        3330
        >>> mround(3335)
        3335
        >>> mround(3338)
        3340
        >>> mround(2.332, .005)
        2.33
        >>> mround(2.335, .005)
        2.335
        >>> mround(2.338, .005)
        2.34
        >>> arr = np.array([1006, 987, 1024, 1023, 978])
        >>> mround(arr)
        array([1005.,  985., 1025., 1025.,  980.])
    """
    ret = None
    if isinstance(x, np.ndarray):
        ret = base * np.around(x/base)
    elif isinstance(x, list) or isinstance(x, tuple):
        raise ValueError("x should be a 1D numpy array")
    else:
        try:
            ret = base * round(x/base)
        except Exception as ex:
            print(ex)
    return ret


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

    # Test mround function
    assert mround(3332) == 3330, "mround(3332) failed"
    assert mround(3335) == 3335, "mround(3335) failed"
    assert mround(3338) == 3340, "mround(3338) failed"
    assert mround(0) == 0, "mround(0) failed"

    # Test with float values and custom base
    assert abs(mround(2.332, 0.005) -
               2.33) < 1e-10, "mround(2.332, 0.005) failed"
    assert abs(mround(2.335, 0.005) -
               2.335) < 1e-10, "mround(2.335, 0.005) failed"
    assert abs(mround(2.338, 0.005) -
               2.34) < 1e-10, "mround(2.338, 0.005) failed"

    # Test with numpy array
    arr = np.array([1006, 987, 1024, 1023, 978])
    np.testing.assert_array_equal(
        mround(arr),
        np.array([1005., 985., 1025., 1025., 980.]),
        "mround(numpy array) failed"
    )

    print("All assertions passed!")
