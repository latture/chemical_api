# -*- coding: utf-8 -*-

"""
    Chemical API
    ~~~~~~~~~~~~
    A simple API to query a database of chemical data.
    Public GET access is provided. Authenticated users have full access to add, modify and delete chemical entries.

    :copyright: (c) 2018 by Ryan Latture.
    :license: MIT, see LICENSE for more details.
"""

import os
from eve import Eve
from eve.auth import BasicAuth
from eve_swagger import swagger, add_documentation

__all__ = ["app", "DoNotUseInProductionAuth"]


class DoNotUseInProductionAuth(BasicAuth):
    """
    The simplest of authentication classes. (Do not use this.)
    The provided username and password are compared to environment variables ``ADMIN_USERNAME`` and ``ADMIN_PASSWORD``, respectively.
    """
    def check_auth(self, username, password, allowed_roles, resource, method):
        return username == os.environ.get('ADMIN_USERNAME', 'admin') and password == os.environ.get('ADMIN_PASSWORD', 'admin')


app = Eve(auth=DoNotUseInProductionAuth)

# Setup required to document the API using swagger.
# See https://swagger.io/docs/ for more info.
app.register_blueprint(swagger)
app.config['SWAGGER_INFO'] = {
    'title': 'Chemical API',
    'version': '1.0',
    'description': 'A REST API to query chemical data',
    'contact': {
        'name': 'Ryan Latture',
        'url': 'https://latture.github.io'
    },
    'license': {
        'name': 'MIT',
    },
    'schemes': ['http', 'https'],
}
