from fapp import app
from yattag import Doc
from flask import render_template, render_template_string

tpl = """
{{% extends 'index.html' %}}
{{% block content %}}
    {html}
{{% endblock %}}
"""


def page():

    doc, tag, text = Doc().tagtext()

    with tag("h1", klass = "mt-4"):
        text("Bem vindo ao Brasil em números")

    return tpl.format(html = doc.getvalue())


@app.route("/inicio")
def inicio():
    return render_template_string(page())
