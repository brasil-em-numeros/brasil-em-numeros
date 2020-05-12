from os import path


def page():

    loc = path.abspath(__file__)
    loc = path.dirname(loc)
    with open(path.join(loc, "ui.html"), "r") as f:
        txt = f.read()

    return txt
