import requests

import jwt
from urllib.parse import urljoin
from jose import jwk


class Authorizer(object):

    def __init__(self,
                 user_group,
                 provider='https://oidc.prod.hagstofa.is',
                 audience='innranet',
                 auth_on=True,
                 verify_jwt=True):
        self.provider = provider
        self.audience = audience
        self.auth_on = auth_on
        self.verify = verify_jwt
        self.user_group = user_group
        self.cache = dict()
        self.refresh_keys()

    def refresh_keys(self):
        try:
            get_url = urljoin(
                self.provider,
                '.well-known/jwks.json'
            )
            data = requests.get(
                get_url
            ).json()
            key = data['keys'][0]
            self.algorithm = key['alg']
            self.secret = jwk.construct(
                key
            ).public_key().to_pem()
            self.cache["JWT_KEY"] = self.secret
            self.cache["JWT_ALGO"] = self.algorithm

        except Exception:
            raise Exception("Upstream identity provider unavailable")



    def authenticate(self, request):
        
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise Exception("Authorization header is missing")
        key = auth_header[7:]
        if self.verify:
            try:
                payload = jwt.decode(
                    key,
                    self.secret,
                    algorithm=self.algorithm,
                    audience=self.audience
                    )
            except jwt.ExpiredSignatureError:
                raise Exception("Signature expired")
            except (jwt.InvalidTokenError, Exception):
                try:
                    self.refresh_keys()
                    payload = jwt.decode(
                        key,
                        self.secret,
                        algorithm=self.algorithm,
                        audience=audience
                    )
                except Exception:
                    raise Exception("Not authorized")
        else:
            payload = jwt.decode(
                key,
                verify=False
            )

        # Check if any user roles are in the allowed user groups
        # Return username if the user is in an allowed user group - else 401
        user_roles = {group.lower() for group in payload.get('roles', [])}
        if user_roles & self.user_group:
            return payload.get('sub')
        else:
            raise Exception("Not in the correct user group")

