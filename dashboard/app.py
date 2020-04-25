import dash

external_stylesheets = [
    # {
    #     "rel"         : "stylesheet",
    #     "href"        : "/css/style.css"
    # },
    {
        "rel"         : "stylesheet",
        "href"        : "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
        "integrity"   : "sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh",
        "crossorigin" : "anonymous"
    }
]

external_scripts = [
    {
        "src" : "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/js/all.min.js",
        "crossorigin" : "anonymous"
    },
    {
        "src" : "https://code.jquery.com/jquery-3.4.1.min.js",
        "crossorigin" : "anonymous"
    },
    # {
    #     "src"         : "https://code.jquery.com/jquery-3.4.1.slim.min.js",
    #     "integrity"   : "sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n",
    #     "crossorigin" : "anonymous"
    # },
    # {
    #     "src"         : "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js",
    #     "integrity"   : "sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo",
    #     "crossorigin" : "anonymous"
    # },
    {
        "src"         : "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js",
        "integrity"   : "sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6",
        "crossorigin" : "anonymous"
    }
]

app = dash.Dash(
    __name__,
    external_stylesheets = external_stylesheets,
    external_scripts = external_scripts,
    assets_folder="../assets",
    meta_tags=[{'charset' : "UTF-8"}]
)

server = app.server
app.config.suppress_callback_exceptions = True
