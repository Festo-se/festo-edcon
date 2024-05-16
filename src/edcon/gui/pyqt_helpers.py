"""Helper functions used for PyQt interaction."""


def style_string(string, color="black", weight=400, font_size=8):
    """Adds a style to the provided string.

    Parameters:
            color (str): color of the font
            weight (int): weight of the font
    """
    return (
        '<span style=" '
        + f'font-size:{font_size}pt; font-weight:{weight}; color:{color};">{string}</span>'
    )


def bold_string(string, color="black", font_size=8):
    """Adds a bold style to the provided string.

    Parameters:
            color (str): color of the font
    """
    return style_string(string, color, weight=700, font_size=font_size)


def checkmark():
    """
    Returns:
        string: A bold green checkmark symbol.
    """
    return style_string("\u2714", "green", weight=700)


def ballot():
    """
    Returns:
        string: A bold red ballot symbol.
    """
    return style_string("\u2718", "red", weight=700)
