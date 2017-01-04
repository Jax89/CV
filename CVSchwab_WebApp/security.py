# -*- coding: utf-8 -*-
from flask_security import Security

def init_app(app):
    app.security = Security(app)
