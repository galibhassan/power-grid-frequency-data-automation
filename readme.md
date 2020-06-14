# Automation to generate JSON for download-tables

## Requirement

Install Node.js

## Steps

0. execute `npm install` in this directory. This command needs only to be executed for the first run to install dependencies (just like `pip install` in python).

1. Every time a new data is uploaded with an extension `.zip`, execute: `npm run build`. This will generate or update the contents in the `./output` directory.

The json file: `./powerGridDataTableInfo.json` is the desired json from which the html tables can be generated dynamically.
