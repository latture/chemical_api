"""
    Sample client
    ~~~~~~~~~~~~~
    A simple client to demonstrate a few capabilities of the API.

    :copyright: (c) 2018 by Ryan Latture.
    :license: MIT, see LICENSE for more details.
"""
import json
import os
import warnings
import requests


def endpoint(resource, ip='0.0.0.0', port=5000):
    """
    Defines the endpoint URL for the resource.

    Parameters
    ----------
    resource : string
      Resource to access.
    ip : string, optional
      IP address of the serer. Default is ``'0.0.0.0'``
    port : int, optional
      Port the server is listening on. Default is ``5000``
    """
    return f'http://{ip}:{port}/{resource}'


def perform_post(resource, data, username, password):
    """
    Posts data using the provided credentials.

    Parameters
    ----------
    resource : string
      Name of the resource/collection.
    data : dict
      Data to post.
    username : string
      Valid username required to access resource.
    password : string
      Valid password required to access resource.
    
    Returns
    -------
    :class:`requests.response`
        Response of POST request.
    """
    headers = {'Content-Type': 'application/json'}
    return requests.post(endpoint(resource), data, headers=headers, auth=(username, password))


def format_mongo_query(key, op, value):
    """
    Format a mongo-style JSON query parameter.

    Parameters
    ----------
    key: str
        Key to compare against within each item in the resource, e.g. ``formula``, ``band_gap`` or ``color``.
    op: str
        MongoDB operation, e.g. ``'$gt'``.
    value: Any
        Value associated with operation. Must be able to cast as a string.
    
    Returns
    -------
    str
        MongoDB query
    """
    return f'{{"{key}":{{"{op}":{value}}}}}'


def get_total(response):
    """
    Gets the total number of items found in the current response.

    Parameters
    ----------
    response : :class:`requests.response`
        Reponse from the server.
    
    Returns
    -------
    int:
        The number of items found.
    """
    return response.json()['_meta']['total']


def format_single_query(query):
    """
    Formats the query parameters from a single query.

    Parameters
    ----------
    query : str
        MongoDB-stype query.
    
    Returns
    -------
    str
        Query parameters.
    """
    return f'?where={query}' 


def combine_queries(queries):
    """
    Creates a set of query parameters that evaluate to ``True`` if individual queries are satified.

    Parameters
    ----------
    queries : List[str]
        List of MongoDB-style queries.
    
    Returns
    -------
    str
        Combined query.
    """
    if not queries:
        warnings.warn('Attempted to combined queries, but none were provided.')
        return ''

    if len(queries) == 1:
        return format_single_query(queries[0])

    comma_sep_queries = ','.join(queries)
    return f'?where={{"$and":[{comma_sep_queries}]}}'


def create_band_gap_queries(min_band_gap=None, max_band_gap=None):
    """
    Creates the queries to find all chemicals with a band gap within the given range.

    Parameters
    ----------
    min_band_gap : float, optional
        Minimum allowed band gap. Default is ``None``.
    max_band_gap : float, optional
        Maximum allowed band gap. Default is ``None``.
    
    Returns
    -------
    List[str]
        List of queries.
    """
    if min_band_gap is None and max_band_gap is None:
        warnings.warn('No bounds provided for band gap.')
        return None

    key = 'band_gap'
    if max_band_gap is None:
       return [format_mongo_query(key, '$gt', min_band_gap)]

    if min_band_gap is None:
       return [format_mongo_query(key, '$lt', max_band_gap)]
    
    min_band_gap_query = format_mongo_query(key, '$gt', min_band_gap) 
    max_band_gap_query = format_mongo_query(key, '$lt', max_band_gap) 
    return [min_band_gap_query, max_band_gap_query]


def query_by_band_gap(min_band_gap=None, max_band_gap=None):
    """
    Find all chemicals with a band gap within the specified range.

    Parameters
    ----------
    min_band_gap : float, optional
        Minimum allowed band gap. Default is ``None``.
    max_band_gap : float, optional
        Maximum allowed band gap. Default is ``None``.
    """
    queries = create_band_gap_queries(min_band_gap=min_band_gap, max_band_gap=max_band_gap)
    params = combine_queries(queries)
    url = endpoint('chemicals') + params
    r = requests.get(url)
    total_matches = get_total(r)
    print(f'Found {total_matches} items with a band gap between {min_band_gap} and {max_band_gap}.')


def create_formula_query(element):
    """
    Creates a query that evaluates to ``True`` when the chemical formula contains the given element.

    Parameters
    ----------
    element : str
        Element to search for.
    
    Returns
    -------
    str
        MongoDB-syle query.
    """
    return format_mongo_query('formula', '$regex', f'\"{element}\"')


def query_by_element(element):
    """
    Find all chemicals containing the given element.
    
    Parameters
    ----------
    element: str
        Element to search for in each formula.
    """
    formula_query = create_formula_query(element)
    params = format_single_query(formula_query)
    url = endpoint('chemicals') + params
    r = requests.get(url)
    total_matches = get_total(r)
    print(f'Found {total_matches} containing the element {element}.')


def query_by_element_and_band_gap(element, min_band_gap, max_band_gap):
    """
    Find all chemicals that contain the given element and that have a band gap within the given range.
    
    Parameters
    ----------
    min_band_gap : float, optional
        Minimum allowed band gap. Default is ``None``.
    max_band_gap : float, optional
        Maximum allowed band gap. Default is ``None``.
    element: str
        Element to search for in each formula.
    """
    band_gap_queries = create_band_gap_queries(min_band_gap=min_band_gap, max_band_gap=max_band_gap)
    formula_query = create_formula_query(element)
    all_queries = band_gap_queries + [formula_query]
    params = combine_queries(all_queries)
    url = endpoint('chemicals') + params
    r = requests.get(url)
    total_matches = get_total(r)
    print(f'Found {total_matches} items that contain {element} and also have a band gap between {min_band_gap:.1f} and {max_band_gap:.1f}.')


def post_chemical(chemical, username, password):
    """
    Add a chemical to the database and print the response.

    Parameters
    ----------
    chemical: dict
        New chemical to post.
    username: str
        Valid username for the administrator.
    password: str
        Valid password for the administrator.
    """
    r = perform_post('chemicals', json.dumps(new_chemical), username, password)
    if r.status_code == requests.codes.created:
        print("POST of {} successfull.".format(new_chemical['formula']))
    else:
        print("Error posting data. request returned code {}".format(r.status_code))


if __name__ == '__main__':
    min_band_gap = 0.0
    max_band_gap = 3.0
    element = 'Ga'
    new_chemical = {
        'formula': 'Kr1Pt0N1T3',
        'band_gap': 1.e6,
        'color': 'Green'
    }
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    password = os.environ.get('ADMIN_PASSWORD', 'secret')

    query_by_band_gap(min_band_gap, max_band_gap)
    query_by_element(element)
    query_by_element_and_band_gap(element, min_band_gap, max_band_gap)
    post_chemical(new_chemical, username, password)
