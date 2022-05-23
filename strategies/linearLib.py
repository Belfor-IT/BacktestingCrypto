from tti.utils import linear_regression_slope


def LinearRegressionSlope(input_data, period=14, fill_missing_values=True):
    """
    Linear regression of y on x.
    :param x: list of x values
    :param y: list of y values
    :return: slope, intercept
    """

    return linear_regression_slope(x, y), 0
