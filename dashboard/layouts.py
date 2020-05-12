import os
from yattag import Doc, indent
from flask import render_template_string
from . import provedores as prv

loc = os.path.abspath(
    os.path.dirname(__file__)
)


def create_feeder_menu(feeder):

    name  = feeder['name']
    title = feeder['aka']
    icon  = feeder.get('icon')

    doc, tag, text = Doc().tagtext()
    href = "/{}".format(name)

    with tag("a", klass = "nav-link", href = href):
        if icon is not None:
            with tag("div", klass = "sb-nav-link-icon"):
                with tag("i", klass = icon):
                    pass

        text(title)

    return indent(
        doc.getvalue(),
        indentation = " " * 4,
        indent_text = True
    )


def update_template():

    path = os.path.join(
        loc, "templates", "index.html"
    )

    feeders = prv.implemented_feeders()
    if feeders:
        src = map(create_feeder_menu, feeders.values())
    else:
        src = ""

    tpl = """
    {{% extends 'base.html' %}}
    {{% block feeders %}}
    {feeders}
    {{% endblock %}}
    """

    tpl = tpl.format(
        feeders = "\n".join(src)
    )

    with open(path, "w") as f:
        f.write(tpl)


def create_route_for_feeder(feeder):

    tpl = """
    {{% extends 'index.html' %}}
    {{% block content %}}
    {html}
    {{% endblock %}}
    """

    fun = feeder['page']

    def view_fun():
        return render_template_string(
            tpl.format(html = fun())
        )

    return view_fun


def route_feeder_pages(app):

    feeders = prv.implemented_feeders()
    if not feeders:
        return None

    # feeders = {k : v['page'] for k, v in feeders.items()}
    for k, v in feeders.items():

        app.add_url_rule(
            "/" + k,
            endpoint  = k,
            view_func = create_route_for_feeder(v)
        )
