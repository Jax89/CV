# -*- coding: utf-8 -*-

# This module is intended for development purposes ONLY! Do not use this in production!
# Executing this module will start the self hosted debugging server of Flask
from main import app
import logging
import sys

if __name__ == "__main__":
    # Setup logging to stdout
    h = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    h.setFormatter(formatter)

    # The Werkzeug module is logging some important info, like e.g. the debug PIN
    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.INFO)
    logger.addHandler(h)

    del app.logger.handlers[:]  # Warning: This gets rid of the annoying Flask logging handler!
    app.logger.addHandler(h)

    app.run(host="0.0.0.0", port=5000, debug=True, threaded=False)