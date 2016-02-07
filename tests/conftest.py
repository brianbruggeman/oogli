import pytest


@pytest.fixture(scope="module")
def options():
    '''Captures configuration data from config file and validates that
    data is available'''

    green = (0.2, 1.0, 0.2)

    options = {
        'width': 100,
        'height': 100,
        'triangle': [
            (0.0, 0.5),
            (0.5, -0.5),
            (-0.5, -0.5)
        ],
        'colors': [green, green, green],
        'color': green,
        'checksum': 0,
    }

    return options
