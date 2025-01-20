import os

from flask import Flask, request
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils







app = Flask(__name__)



def init_saml_auth(req):
    #Initialize with settings.json & advanced_settings.json file
    auth = OneLogin_saml2_Auth(req)
    return auth
    #auth
 


def preprare_flask_request(request):
    return {
        "https": "on" if request.scheme == "https" else "off",
        "http_host" : request.host,
        "script_name": "request.path",
        "get_data": request.args.copy(),
        "post_data": request.form.copy()
    }
    


@app.route("/", methods=["GET", "POST"])
def index():
    req = preprare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []
    error_reason = None
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False
    return


@app.route("/attrs/")
def attrs():
    return




@app.route("/metadata/")
def metadata():
    return





