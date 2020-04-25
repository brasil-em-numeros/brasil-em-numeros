import os
from flask import Flask, render_template, url_for


app = Flask(
    __name__,
    static_url_path = "/assets",
    static_folder = "assets"
)
