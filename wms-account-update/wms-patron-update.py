import requests
import json
from base64 import b64encode
from datetime import datetime
import pytz
import dateutil.parser
import os

# Variables
worldcat_registry_id = "51807"
client_id = ""
client_secret = ""
token_file = "./token"

def read_credentials(fname):
    '''I'm storing the credentials in an offline file, but you could use environment variables, etc.'''
    file = open(fname, "r")
    wskeys = json.loads(file.read())
    global client_id
    global client_secret
    client_id = wskeys['client_id']
    client_secret = wskeys['client_secret']

def write_token_to_file(token, expires_at):
    token_data = {"token": token, "expires_at": expires_at}
    with open(token_file, "w") as f:
        f.write(json.dumps(token_data))

def create_auth_url(url_type, auth_code=None):
    '''Builds the appropriate URLs for getting an authorization code and an access token.'''
    authorization_base_url = "https://oauth.oclc.org"
    redirect_uri = "https://illrequest.webservices.library.uwinnipeg.ca/ill/PostOAuth"
    
    if url_type == "auth":
        return(f"{authorization_base_url}/auth/{worldcat_registry_id}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=SCIM&state=account")
    else:
        return(f"{authorization_base_url}/token?grant_type=authorization_code&code={auth_code}&redirect_uri={redirect_uri}")

def get_access_token():
    '''Gets an access token from OCLC's Oauth server. Client credentials can be found on OCLC's WSKEYS site.'''
    print("Open this link in browser: ")
    print(create_auth_url("auth"))
    auth_code = input("Enter auth code: ")
    response = json.loads(requests.post(create_auth_url("token", auth_code), auth=(client_id, client_secret)).content)
    write_token_to_file(response["access_token"], response["expires_at"])
    return response["access_token"]

def call_wms_api(method, access_token, payload=None, user_id=None):
    '''Call's the OCLC WMS Identity Management API. Takes a REST method (get or put), an access token, and an optional payload. If the user_id is not present, it prompts the user to supply one.'''
    if not user_id:
        user_id = input("Enter user id: ")  # user ID is a hex number taken from the Diagnostics section of the WMS account.
    header_string = f"Bearer {access_token}"
    headers={'Authorization': header_string, 'Content-Type': 'application/scim+json'}
    url = f"https://{worldcat_registry_id}.share.worldcat.org/idaas/scim/v2/Users/{user_id}"
    api_call = getattr(requests, method)
    response = api_call(url, data=payload, headers = headers)
    return response.content

if os.path.exists(token_file):
    file = open(token_file, "r")
    token_data = json.loads(file.read())
    access_token = token_data['token']
    expires_at = dateutil.parser.parse(token_data['expires_at']).replace(tzinfo=None)

#if expires_at < datetime.now():  # need to check on this - the token seems to expire unexpectedly.
#print(make_api_call(get_access_token()))
#else:
#    print(make_api_call(access_token))

read_credentials("oclc_wskeys.json")
access_token = get_access_token()

user_info = json.loads(call_wms_api("get", access_token))
print(user_info)

# user_info is a dict that contains sets. I recommend printing user_info to see which pieces of information you want to change. 
# e.g. user_info["name"] = {'familyName': 'newFamilyName', 'givenName': 'newGivenName'}
# to update network ID, you need to add the following:
# user_info["urn:mace:oclc.org:eidm:schema:persona:correlationinfo:20180101"] = {'correlationInfo'" [{'sourceSystem': 'newSourceSystemURN', 'idAtSource': 'network ID'}]}
# Note that this doesn't remove the old info, just adds a new Source System line. Not sure if that will prevent logins or not.

print(call_wms_api("put", access_token, json.dumps(user_info)))

