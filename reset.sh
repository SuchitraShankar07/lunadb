#!/bin/bash

mysql -u root -p < create.sql
mysql -u root -p < insert.sql
mysql -u root -p < operations.sql
