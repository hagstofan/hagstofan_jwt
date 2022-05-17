# JWT Api

## Description

This is a package providing an authorization module with an authenticate function.
This is meant to be used by APIs using hagstofan's kvörn jwt authorization/authentication
## Configuration

| Environmental variable | Default value                      | Description                                                                    | neccesary |
|------------------------|------------------------------------|--------------------------------------------------------------------------------|-----------|
| JWT_VERIFY             | true                               |                                                                                |     no    |
| AUTH_ON                | true                               | using our internal OIDC auth ?                                                 |     no    |
| REQUESTS_CA_BUNDLE     | /etc/ssl/certs/ca-certificates.crt | the certificates                                                               |    yes    |
| USER_GROUP             | 'None'                             | OIDC AD usergroup with access (set to IT-web for development only)             |    yes    |
| OIDC_PROVIDER       	 | 'https://oidc.prod.hagstofa.is'    | the url of the OIDC provider, for dev e.g. maybe http://localhost:8080         |     no    |
| OIDC_AUDIENCE          | 'innranet'                         | the audience used by kvörn seems to be innranet, so use default                |     no    |


## use
add this line to requirements
```
git+https://code.hagstofa.local/BergurTh/hagstofan_jwt
```
```
from auth_utils.auth import Authorizer

user_group = '["IT-web"]'

authorizer = Authorizer(user_group)

# here is a dummy route as in flask, the authenticate function
# could be used in something else the key is the
# authorizer.authenticate(request) line
@app.route('/')
def base_route():

    if current_app.config['AUTH']:
        # the old way
        #user = authenticate(request)
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