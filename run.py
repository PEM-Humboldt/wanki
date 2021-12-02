"""

"""
import webbrowser
from threading import Timer

from utils.app import app
from utils.callbacks import generate_callbacks
from utils.layout import layout

port = 5000


def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))


if __name__ == "__main__":
    app.layout = layout
    generate_callbacks(app)
    Timer(1, open_browser).start()
    app.run_server(debug=False, port=port)
