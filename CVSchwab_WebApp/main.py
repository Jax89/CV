import CVSchwab_WebApp.custom_navbar
import CVSchwab_WebApp.security

import flask
import flask_bootstrap
import flask_mail
import flask_login
from flask import send_from_directory, request


# setup app
app = flask.Flask(__name__)
mail = flask_mail.Mail(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
flask_bootstrap.Bootstrap(app)

CVSchwab_WebApp.security.init_app(app)

app.extensions['bootstrap']['cdns']['jquery'] = flask_bootstrap.StaticCDN()

CVSchwab_WebApp.custom_navbar.init_app(app)


@app.route('/')
def view_personal_information():
    return flask.render_template('personal_information.html')


@app.route('/education_work')
def view_education_work():
    return flask.render_template('education.html')


@app.route('/publications')
def view_publications():
    return flask.render_template('publications.html')


@app.route('/it_language')
def view_it_language():
    return flask.render_template('it_language.html')


@app.route('/references')
def view_references():
    return flask.render_template('references.html')

@app.route('/imprint')
def view_imprint():
    return flask.render_template('imprint.html')

@app.route('/further_information')
def view_further_information():
    return flask.render_template('further_information.html')

    ########################################
    # Download links


@app.route('/download_cv', methods=['GET', 'POST'])
def download_cv():
    filename = "CV_schwab.pdf"
    return send_from_directory("downloads/", filename, as_attachment=True)


