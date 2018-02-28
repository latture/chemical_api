"""
    Main
    ~~~~
    Entry point into the api.

    :copyright: (c) 2018 by Ryan Latture.
    :license: MIT, see LICENSE for more details.
"""


from chemical_api import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)