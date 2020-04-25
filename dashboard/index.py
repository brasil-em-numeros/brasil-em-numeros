from fapp import app
from inicio import inicio

@app.route("/")
@app.route("/index.html")
def index():

    return inicio()


if __name__ == "__main__":
    app.run(debug=True)
