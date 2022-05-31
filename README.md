# JWT Api

## Description

This is a package providing an authorization module with an authenticate function.
This is meant to be used for example by APIs using hagstofan's kvörn jwt authorization/authentication.
It is assumed that the jwt or Bearer token will be in either the request headers under
Authentication, so:
```
Authentication: Bearer <token>
```
or in case of there not being anything there, this package will look for a cookie with
index auth_header, so:
```
auth_header: Bearer <token>
```
This is intended for the possible use-cases where a web based portal redirects to a web based service
using this package. In this instance the idea is that the portal sets the cookie before redirecting to the
service.

## Configuration

The Authoirizer object in this package only strictly needs one parameter, user_groups
everything else has defaults which will function in production.

The service using this module needs to set the environmental variable REQUESTS_CA_BUNDLE
e.g.
```
REQUESTS_CA_BUNDLE: /etc/ssl/certs/ca-certificates.crt
```
and then have the relevant certs in the specified place on the server.
This is all that is needed for this package to function.


| Parameter or Envar     | Default value                      | Description                                                                    | neccesary |
|------------------------|------------------------------------|--------------------------------------------------------------------------------|-----------|
| verify_jwt             | true                               | verify the jwt in production, in some cases in dev, maybe not                  |     no    |
| auth_on                | true                               | using our internal OIDC auth ?                                                 |     no    |
| REQUESTS_CA_BUNDLE     | /etc/ssl/certs/ca-certificates.crt | the certificates                                                               |    yes    |
| user_groups            | 'None'                             | OIDC AD usergroup with access (set to IT-web for development only)             |    yes    |
| provider          	 | 'https://oidc.prod.hagstofa.is'    | the url of the OIDC provider, for dev e.g. maybe http://localhost:8080         |     no    |
| audience               | 'innranet'                         | the oidc audience used by kvörn seems to be innranet, so use default           |     no    |


## Use
add this line to requirements.txt
```
git+https://code.hagstofa.local/ut/web/hagstofan_jwt
```
Then in your relevant code, where you want to authenticate via jwt ..
```
from auth_utils.auth import Authorizer

"""
# The groups are taken in as a set object, from a string.
# typically this string would originate from an environmental variable
# here below it is just a hardcoded string '["IT-web"]'.
# Your implementation will probably take this string from an
# environmental variable.
"""
user_groups = {group.lower() for group in json.loads(
    '["IT-web"]')
}

authorizer = Authorizer(user_groups)

"""
# here is a dummy route as in flask, the authenticate function
# could be used in something else the key is the
# authorizer.authenticate(request) line
"""
@app.route('/')
def base_route():

    if current_app.config['AUTH']:
        try:
            # using module
            user = authorizer.authenticate(request)  # <--- here
        except Exception as e:
            raise AuthBad(e.args[0])

    # your service here <--------------------
    response = jsonify({'data': 'you have access to this data'})
    response.status_code = 200
    return(response)

```
Optionally, you might also whant your service to provide a route showing what groups are meant to have access.
e.g.
```
@app.route('/.well-known/hagstofan')
def authorized_groups():
    return Response(
        json.dumps(
            {'roles': list(user_groups)}  #  <-- adding same groups list here as Authorizer is initialized with. (if you want to be nice)
        ),
        mimetype='application/json'
    )
```