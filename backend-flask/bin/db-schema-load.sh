#! /usr/bin/bash

echo -e "SCHEMA LOAD\n"

psql $CONNECTION_URL crudder < db/schema.sql

