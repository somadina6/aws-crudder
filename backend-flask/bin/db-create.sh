#! /usr/bin/bash

echo -e "db-create\n"

psql $CONNECTION_URL -c "CREATE DATABASE cruddur"