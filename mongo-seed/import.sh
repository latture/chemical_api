#!/bin/bash

# This command simply imports our seed data (data.json) into the chemicals collection of the eve database.
# The database is hosted in our MongoDB container. 
# If the database exists, we delete the data and replace it with the data from our JSON file.

mongoimport --host mongo --db eve --collection chemicals --type json --drop --file /mongo-seed/data.json --jsonArray