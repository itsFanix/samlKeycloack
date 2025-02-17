import os

from flask import Flask, request, redirect, session, url_for
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from urllib.parse import urlparse
import json


#SSO : Signle Sign on
#SLO : Single Log out
#ACS : Assertion Consumer Service


app = Flask(__name__)

# Clé cryptographique utilise pour ssigner les sessions utilisateur
# Proteger contre les attaques csrf
# Securiser les cookies
# Pour la production utiliser une clé  fixe stockée dans une variable d'environnement

app.secret_key = os.urandom(32)

app.config["SAML_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saml")



def init_saml_auth(req):
    #Initialize with settings.json & advanced_settings.json file


    with open('saml/settings.json', 'r') as f : 
        main_settings = json.load(f)
    
    with open("saml/advanced_settings.json") as f :
        advanced_settings= json.load(f)

    
    saml_settings ={**main_settings, **advanced_settings}

    
    with open('saml/certs/idp-certificate.pem', 'r') as   idp_cert_file :
        idp_cert = idp_cert_file.read()
    
    with open('saml/certs/sp-certificate.pem', 'r') as   sp_cert_file :
        sp_cert = sp_cert_file.read()
    
    with open('saml/certs/sp-private-key.pem', 'r') as   sp_key_file :
        sp_key = sp_key_file.read()

    saml_settings["sp"]["x509cert"] = sp_cert.strip()
    saml_settings["sp"]["privateKey"] = sp_key.strip()
    saml_settings["idp"]["x509cert"] = idp_cert.strip()


    auth = OneLogin_Saml2_Auth(req, saml_settings)
    
    return auth



# This function is crutial for translating Flask's reauest object into a format that python3-saml understand
# python3-saml expects reauest data in a speific dictionary format
# Flask reauest object has different structures
# this function bridges that  gaps by converting Flask's format to what SAML needs

# Common scenarios where it's used:

    # Initial login request
    # Processing SAML response
    # Logout request
    # Single Logout Service (SLS) handling

def prepare_flask_request(request):
    print(request)
    return {
        "https": "on" if request.scheme == "https" else "off",  # Indicate if request is secure
        "http_host" : request.host,                             # Server hostname
        "server_port" : request.environ.get("SERVER_PORT"),                       # Port number
        "script_name": request.path,                            # URL path
        "get_data": request.args.copy(),                        # GET parameters
        "post_data": request.form.copy(),                       # POST parameters
        "query_string": request.query_string                    # Raw query string
    }
    





@app.route("/", methods=["GET", "POST"])
def index():
    if 'samlUserdata' not in session:
        return redirect(url_for('login'))
    
    return f"""

    <h2>Welcome, {session['samlUserdata']}</h2>
    <a href="{url_for('logout')}">Logout</a>
    """


@app.route('/login')
def login():
    
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())





# Assertion Consumer Service ACS
# One of the most important endpoint in SAML
# SAML response are always sent via POST due to their size
# SAML response contains encrypted?signed data that shouldn't be in URL
@app.route('/acs', methods=['POST'])
def acs():

    # Convert Flask reauest to SAML-compatible format
    req = prepare_flask_request(request)

    # Initialize SAML auth with the request
    auth = init_saml_auth(req)

    # Process the SAML response from IDP (Keycloak)
    auth.process_response()

    # Check for any errors during processing
    errors= auth.get_errors()


    if not errors:

        # Store user data in session
        session['samlUserdata'] = auth.get_attributes()  # User attributes (email, groups, etc)
        session['samlNameId'] = auth.get_nameid()        # Unique user identifier
        

        # Handle RelayState (Where to redirect after login)
        # if 'RelayState' in request.form and request.form['RelayState']:
            #  return redirect(auth.redirect_to(request.form['RelayState']))
        # else :
        return redirect(url_for('index'))
    
    return f"Error: {', '.join(errors)}"


# The logout process invloves two main part

# Local Logout 
    # Clear the FLask session (Session.clear())
    # Removes all stored SAML data
    # Cleans up local application

# Single Logout (SLO)
    # Uses name_id to identify which user is logging out
    # Redirects to IDP (Keycloak)'s logout endpoint
    # IDP (Keycloak) then terminates the user's session
@app.route('/logout')

 
def logout():

    # Convert Flask request to SAML for format 
    req = prepare_flask_request(request)

    # Initialize SAML auth object 
    auth = init_saml_auth(req)

    # Get the user's Name ID from session
    name_id = session.get('samlNameId')
    
    # Clear the Flask session
    session.clear()

    # Redirect to IDP (keycloack)'s logout  URL
    return redirect(auth.logout(name_id=name_id))  #auth.logout can take several parameters


#Single Logout Service (SLS)
# Handles IDP (Keycloak) response from 

# Processes Logout Responses:

    # When you initiated the logout
    # Confirms the logout was successful
    # Final step in SP-initiated logout

# Processes Logout Requests:
    # When Keycloak initiates the logout
    # Tells your app to end the user's session
    # Part of IdP-initiated logout
@app.route('/sls')
def sls():

    # Convert Flask request to SAML for format 
    req = prepare_flask_request(request)

    # Initialize SAML auth object 
    auth = init_saml_auth(req)
    
    # Process the Single Logout response/request
    url = auth.process_slo()

    # Check for any errors during logout 
    errors = auth.get_errors()

    # Handle the result
    if len(errors)==0:
        return redirect(url or url_for('index'))
    
    return f"Error: {','.join(errors)}"


@app.route("/attrs/")
def attrs():
    return




@app.route("/metadata/")
def metadata():
    return





