# -*- coding: utf-8 -*-

"""
    Settings
    ~~~~~~~~
    This file contains the settings required to setup the REST API that will allow us to query the chemicals database.

    :copyright: (c) 2018 by Ryan Latture.
    :license: MIT, see LICENSE for more details.
"""

import os

# Setup variable need to connect to the database
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongo')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'eve')

MONGO_QUERY_BLACKLIST = ['$where']

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# Allow pubic GET method for resource endpoints
PUBLIC_METHODS = ['GET']

# Allow public Get method for item endpoints
PUBLIC_ITEM_METHODS = ['GET']

# Enable standard client cache directives for all resources exposed by the API.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

chemicals = {
    # 'title' tag used in item links.
    'item_title': 'chemical',

    # Allows requests at '/chemicals/<formula>/' in addition to '/chemicals/<ObjectId>/'.
    # 'additional_lookup': {
    #     'url': 'regex("[\w]+")',
    #     'field': 'formula'
    # },

    'transparent_schema_rules': True,

    'description': 'A store of chemical data.',

    'schema': {
        'formula': {
            'description': 'Chemical formula',
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,
            # 'unique': True,
        },
        'band_gap': {
            'description': 'Band gap of the chemical.',
            'type': 'float',
            'required': True,
        },
        'color': {
            'description': 'Observed color of the chemical.',
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,
        },
    },
}

DOMAIN = {
    'chemicals': chemicals,
}
