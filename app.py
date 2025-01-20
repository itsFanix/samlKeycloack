import os

from flask import Flask, request, redirect, session, url_for
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from urllib.parse import urlparse







#SSO : Signle Sign on
#SLO : Single Log out
#ACS : Assertion Consumer Service


app = Flask(__name__)

app.config["SAML_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saml")



def init_saml_auth(req):
    #Initialize with settings.json & advanced_settings.json file
    auth = OneLogin_saml2_Auth(req, custom_base_path = app.config["SAML_PATH"])
    return auth
 


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
    if 'samlUserdata' not in session:
        return redirect(url_for('login'))
    
    return f"""

    <h2>Welcome, {session['samlUserdata'].get('username',  'User')}</h2>
    <a href="{url_for('logout')}">Logout</a>
    """


@app.route('/login')
def login():
    req = preprare_flask_request(request)
    auth = init_saml_auth()
    return redirect(auth.login())






@app.route('/acs', methods=['POST'])
def acs():
    req = preprare_flask_request(request)
    auth = init_saml_auth(req)
    auth.process_response()
    errors= auth.get_errors()


    if not errors:
        session['samlUserdata'] = auth.get_attributes()
        session['samlNameId'] = auth.get_nameid()
        
        if 'RelayState' in request.form and request.form['RelayState']:
            return redirect(auth.rediredt_to(request.form['RelayState']))
        return redirect(url_for('index'))
    
    return f"Error: {', '.join(errors)}"



@app.route('/logout')
def logout():
    req = preprare_flask_request(request)
    auth = init_saml_auth(req)
    name_id = session.Get('samlNameId')
    session.clear()
    return redirect(auth.logout(name_id=name_id))



@app.route('sls')
def sls():
    req = preprare_flask_request(request)
    auth = init_saml_auth(req)
    url = auth.process_slo()
    errors = auth.get_errors()

    if len(errors)==0:
        return redirect(url or url_for('index'))
    
    return f"Error: {','.join(errors)}"


@app.route("/attrs/")
def attrs():
    return




@app.route("/metadata/")
def metadata():
    return





