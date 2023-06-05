from flask import Flask, request, Response, jsonify, make_response
import datetime
from edit_data import get_drs_object, get_drs_access_url, get_drs_object_passport
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
from helper import parse_args
import json

app = Flask(__name__)
args = parse_args()
app.config["auth_type"] = args.auth_type
users = {
    "username": generate_password_hash("password")
}
tokens = {
    "secret-bearer-token-1": "user-1"
}

auth_basic = HTTPBasicAuth()
auth_bearer = HTTPTokenAuth(scheme="Bearer")

@auth_bearer.error_handler
@auth_basic.error_handler
def unauthorized():
    return make_response(jsonify({
        "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status_code": 401,
        "error": "Request is unauthorized",
        "msg": "Invalid Credentials"}), 401)

def conditional_auth(auth_config):
    def decorator(func):
        if auth_config == "none":
            # Return the function unchanged, not decorated.
            return func
        elif auth_config == "basic":
            return auth_basic.login_required(func)
        elif auth_config == "bearer":
            return auth_bearer.login_required(func)
        elif auth_config == "passport":
            return func #TODO: FAIL!!!
        return func
    return decorator

@auth_bearer.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@auth_basic.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

'''
HTTP codes
200: "Retrieve info about the DRS service"
500: "An unexpected error occured"
'''

# Get service info
@app.route('/ga4gh/drs/v1/service-info', methods=['GET'])
@conditional_auth(app.config["auth_type"])
def get_service_info():
    header_content = request.headers
    accept_type = "application/json"

    # validate the accept header
    if "accept" in header_content and header_content["accept"] not in [accept_type, "*/*"]:
        return Response(status=406)

    service_info_resp = {
        "id": "org.ga4gh.starterkit.drs",
        "name": "GA4GH Starter Kit DRS Service",
        "description": "An open source, community-driven implementation of the GA4GH Data Repository Service (DRS) API specification.",
        "contactUrl": "mailto:info@ga4gh.org",
        "documentationUrl": "https://github.com/ga4gh/ga4gh-starter-kit-drs",
        "environment": "test",
        "version": "0.3.1",
        "type": {
            "group": "org.ga4gh",
            "artifact": "drs",
            "version": "1.2.0"
        },
        "organization": {
            "name": "Global Alliance for Genomics and Health",
            "url": "https://ga4gh.org"
        }
    }

    return Response(response=json.dumps(service_info_resp), status=200, mimetype=accept_type)

'''
HTTP codes
200: "The DRS object was found successfully"
202: "The operation is delayed and will continue asynchronously"
400: "The request is malformed",
401: "The request is unauthorized",
403: "The requestor is not authorized to perform this action",
404: "The requested DRS object was not Found",
500: "An unexpected error occured"
'''

# GET Info about a DRS Object or
# GET Info about a DRS Object through POST'ing a Passport
@app.route('/ga4gh/drs/v1/objects/<obj_id>', methods=['GET','POST'])
@conditional_auth(app.config["auth_type"])
def get_object(obj_id):
    expand = request.args.get('expand', "False")

    # convert param to bool
    if expand.lower() == "true": 
        expand = True
    else:
        expand = False
    accept_type = "application/json"
    drs_obj = get_drs_object(obj_id, expand)
    if request.method == "GET" and app.config["auth_type"]!="passport":
        if not drs_obj: # Object not found
            error_obj = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status_code": 404,
                "error": "Not Found",
                "msg": "No DrsObject found by id: " + obj_id
            }
            return Response(response=json.dumps(error_obj), status=404, mimetype=accept_type)
        return Response(response=json.dumps(drs_obj), status=200, mimetype=accept_type)

    elif request.method == "POST" and app.config["auth_type"]=="passport":
        header_content = request.headers
        accept_type = "application/json"

        if not drs_obj: # Object not found
            error_obj = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status_code": 404,
                "error": "Not Found",
                "msg": "No DrsObject found by id: " + obj_id
            }
            return Response(response=json.dumps(error_obj), status=404, mimetype=accept_type)

        if app.config["auth_type"]=="passport" and ("accept" in header_content and header_content["accept"] in [accept_type, "*/*"]):
            try:
                request_body = request.get_json()

                if "expand" in request_body:
                    if isinstance(request_body["expand"], bool):                    
                        expand = request_body["expand"]
                    elif isinstance(request_body["expand"], str):
                        if request_body["expand"].lower() == "true": 
                            expand = True
                        else:
                            expand = False 
                    else:
                        expand = False
                
                drs_obj = get_drs_object(obj_id, expand)

                drs_obj_passport = get_drs_object_passport(obj_id)
                if not request_body["passports"]:
                    error_obj = {
                        "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "status_code": 401,
                        "error": "Request is unauthorized",
                        "msg": "A passport is required to authorize the request"
                    }
                    return Response(response=json.dumps(error_obj), status=401, mimetype=accept_type)
                elif drs_obj_passport in request_body["passports"]:
                    return Response(response=json.dumps(drs_obj), status=200, mimetype=accept_type)
                else:
                    error_obj = {
                        "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "status_code": 403,
                        "error": "The requestor is not authorized to perform this action",
                        "msg": "The passport provided does not grant access to the requested resource"
                    }
                    return Response(response=json.dumps(error_obj), status=403, mimetype=accept_type)
            except Exception as ex:
                error_obj = {
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "status_code": 500,
                    "error": "An unexpected error occured",
                    "msg": "An unexpected error occured. Exception: " + str(ex) +
                           ". POST method can be used only if the app is running with auth_type as 'passport'. "
                           "Content-Type must be 'application/json"
                }
            return Response(response=json.dumps(error_obj), status=500, mimetype=accept_type)

        else:
            error_obj = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status_code": 500,
                "error": "An unexpected error occured",
                "msg": "An unexpected error occured. POST method can be used only if the app is running with auth_type as 'passport'. "
                       "Content-Type must be 'application/json'"
            }
            return Response(response=json.dumps(error_obj), status=500, mimetype=accept_type)
    else:
        error_obj = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status_code": 400,
            "error": "The request is malformed",
            "msg": "HTTP Method Not Allowed"
        }
        return Response(response=json.dumps(error_obj), status=400, mimetype=accept_type)


# Get a URL for fetching bytes or
# Get a URL for fetching bytes through POST'ing Passport
@app.route('/ga4gh/drs/v1/objects/<obj_id>/access/<access_id>', methods=['GET', 'POST'])
@conditional_auth(app.config["auth_type"])
def get_access_url(obj_id, access_id):
    accept_type = "application/json"
    access_url_obj = get_drs_access_url(obj_id, access_id)

    if request.method == "GET" and app.config["auth_type"]!="passport":
        if access_url_obj:
            # Object found
            return Response(response=json.dumps(access_url_obj), status=200, mimetype=accept_type)
        else:
            # Object not found
            error_obj = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status_code": 404,
                "error": "Not Found",
                "msg": "The requested access url wasn't found"
            }

            return Response(response=json.dumps(error_obj), status=404, mimetype=accept_type)
    elif request.method == "POST" and app.config["auth_type"]=="passport":
        header_content = request.headers
        accept_type = "application/json"

        if not access_url_obj: # Object not found
            error_obj = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status_code": 404,
                "error": "Not Found",
                "msg": "No access url found for drs id: " + obj_id + " and access_id: " + access_id
            }
            return Response(response=json.dumps(error_obj), status=404, mimetype=accept_type)

        if app.config["auth_type"]=="passport" and ("accept" in header_content and header_content["accept"] in [accept_type, "*/*"]):
            try:
                request_body = request.get_json()
                drs_obj_passport = get_drs_object_passport(obj_id)
                if not request_body["passports"]:
                    error_obj = {
                        "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "status_code": 401,
                        "error": "Request is unauthorized",
                        "msg": "A passport is required to authorize the request"
                    }
                    return Response(response=json.dumps(error_obj), status=401, mimetype=accept_type)
                elif drs_obj_passport in request_body["passports"]:
                    return Response(response=json.dumps(access_url_obj), status=200, mimetype=accept_type)
                else:
                    error_obj = {
                        "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "status_code": 403,
                        "error": "The requestor is not authorized to perform this action",
                        "msg": "The passport provided does not grant access to the requested resource"
                    }
                    return Response(response=json.dumps(error_obj), status=403, mimetype=accept_type)
            except Exception as ex:
                error_obj = {
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "status_code": 500,
                    "error": "An unexpected error occured",
                    "msg": "An unexpected error occured. Exception: " + str(ex) +
                           ". POST method can be used only if the app is running with auth_type as 'passport'. "
                           "Content-Type must be 'application/json"
                }
            return Response(response=json.dumps(error_obj), status=500, mimetype=accept_type)
        else:
            error_obj = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status_code": 500,
                "error": "An unexpected error occured",
                "msg": "An unexpected error occured. POST method can be used only if the app is running with auth_type as 'passport'. "
                       "Content-Type must be 'application/json'"
            }
            return Response(response=json.dumps(error_obj), status=500, mimetype=accept_type)
    else:
        error_obj = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status_code": 400,
            "error": "The request is malformed",
            "msg": "HTTP Method Not Allowed"
        }
        return Response(response=json.dumps(error_obj), status=400, mimetype=accept_type)

if __name__=="__main__":
    app.run(host=args.app_host,port=args.app_port)