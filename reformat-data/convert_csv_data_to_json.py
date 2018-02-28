"""
    Convert chemicals CSV to JSON
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This script converts the provided data from CSV to JSON.
    This could be incorporated into our deployment (if we needed to retain data.csv as the canonical data source),
    Since the data is constant, however, I've elected to run this once before the first deployment.

    :copyright: (c) 2018 by Ryan Latture.
    :license: MIT, see LICENSE for more details.
"""
import json
import os
import sys
import pandas as pd


def _row_to_chemical(row):
    """
    Helper function to translate from a row in a pandas data frame to a dictionary with the desired schema.

    Parameters
    ----------
    row : :class:`pd.Series`
      Row from pandas dataframe. Must have entries for ``'Chemical Formula'``,``'Property 1 value'`` and ``'Property 2 value'``.
    
    Returns
    -------
    dict
      Dictionary containing chemical data in a more convient format, i.e.
      ``{'formula': ..., 'band_gap': ..., 'color': ...}``.

    """
    return {
        'formula': row['Chemical formula'],
        'band_gap': row['Property 1 value'],
        'color': row['Property 2 value'],
    }


def convert_data():
    """
    Converts ``data.csv`` into JSON and store the result in ``mongo-seed/data.json``
    """
    # Hard coded input and output filename
    filename_in = 'data.csv'
    filename_out = os.path.join('..', 'mongo-seed', 'data.json')

    # Read the data from disk
    data = pd.read_csv(filename_in)

    # convert to a list of dictionaries
    chemicals = [_row_to_chemical(row) for _, row in data.iterrows()]

    with open(filename_out, 'w') as f:
        json.dump(chemicals, f)


if __name__ == '__main__':
    # set working directory to location of this script:
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    convert_data()
