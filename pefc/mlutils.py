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

# NOTE: The percent_* formulas are based on the following references.
# https://www.calculatorsoup.com/calculators/algebra/percent-difference-calculator.php
# https://en.wikipedia.org/wiki/Relative_change_and_difference


def percent_change(value1: float, value2: float, frac: bool = False) -> float:
    """ Return the percentage change between two values. The denominator
        or base value is value1.
        Equation used is (value2 - value1)/value1. This is to check the
        material usage variance to a standard value, the value1 parameter.

        value1: float, base value

        value2: float, changed value

        frac: bool, Default is False. Set to True returns a fraction
            instead of percentages. This is useful for performing
            calculations on spreadsheets.

        return: float, percentage change value

        Example
        -------
        >>> percent_change(-10, -6)
        -40.0
        >>> percent_change(100, 110)
        10.0
        >>> percent_change(100, 110, frac=True)
        0.1

    """
    # don't use relative percentage change i.e (value2 - value1)/abs(value1)
    # use the same function as HP calculator's Δ% as per wikipedia
    # value1 ENTER value2 Δ% e.g. -10 ENTER -6 Δ% = -40
    perchg = (value2 - value1)/value1
    if frac is False:
        perchg *= 100
    return perchg


def percent_diff(value1: float, value2: float, frac: bool = False) -> float:
    """ Return the percentage difference between two values. The denominator
            is the average of value1 and value2.

            value1: float, first value

            value2: float, second value

            frac: bool, Default is False. Set to True returns a fraction
                instead of percentages. This is useful for performing
                calculations on spreadsheets.

            return: float, absolute value of the difference in percentages

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

        return: float, percentage change value

        Usage
        -----
        >>> percent_error(-10, -6)
        40.0
        >>> percent_error(100, 110)
        10.0
        >>> percent_error(100, 110, frac=True)
        0.1

    """
    # percent_error as per wikipedia article
    # percent_error = |experimental - theoretical| / |theoretical|
    pererr = abs(value2 - value1)/abs(value1)
    if frac is False:
        pererr *= 100
    return pererr


def percent_changefrom_target(target_val: float, actual_val: float,
                              frac: bool = False) -> float:
    """ Return the percentage change between target and actual values.
        The denominator is the target value.
        Equation used is (target_val - actual_val)/target_val

            target_val: float, target value

            actual_val: float, current actual value

            frac: bool, Default is False. Set to True returns a fraction
                instead of percentages. This is useful for performing
                calculations on spreadsheets.

            return: float, percentage difference or fraction

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


def snake2camel_case(label: str, addspace=False) -> str:
    """ Convert a snake case string to camel case. e.g. team_member becomes
        TeamMember and vice versa. If addspace is True, then the first letter
        of each word is capitalized and a space is added between words.

        label: str, input string

        addspace: bool, Default is False. Set to True adds a space between
            words.

        return: str, camel case string

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

        return: str, snake case string

        Example
        -------
        >>> camel2snake_case('TeamMember')
        'team_member'
    """
    return ''.join(['_' + i.lower() if i.isupper() else i
                    for i in label]).lstrip('_')


def _test():
    import doctest
    print(doctest.testmod())


if __name__ == '__main__':
    _test()
    print(percent_change(100, 110))
    print(percent_change(100, 110, frac=True))
    print(percent_diff(5, 7))
    print(percent_diff(5, 7, frac=True))
    print(percent_error(100, 110))
    print(percent_error(100, 110, frac=True))
    print(snake2camel_case('team_member'))
    print(snake2camel_case('team_member', addspace=True))
    print(camel2snake_case('TeamMember'))
