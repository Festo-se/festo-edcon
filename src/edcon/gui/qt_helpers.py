def style_string(string, color="black", weight=400):
    return f'<span style=" font-size:8pt; font-weight:{weight}; color:{color};">{string}</span>'


def bold_string(string, color="black"):
    return style_string(string, color, weight=700)


def checkmark():
    return style_string("\u2714", "green", weight=700)


def ballot():
    return style_string("\u2718", "red", weight=700)
