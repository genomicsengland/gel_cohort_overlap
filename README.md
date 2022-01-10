# GEL Overlapping Cohorts

The purpose of this repo is to :

* Gather demographic data for participants in a given GEL cohort
* Maintain the utilities to format, filter and generate hashes based on a defined algorithm

## Demographic Data

* Demographic data is pulled using the query defined in the **/sql** folder. This query is run against the Patient Master Index (PMI)

| File Name | Description |
|---|---|
| `pmi_demographics.sql`| `Gathers nhs_number and date_of_birth for all participants in the 100k study that are within the PMI` |


## DotEnv

* A **.env** file (part of gitignore, so is local to the running machine) is required in the root of the repo. The structure of this file is available in the *dotenv.tmpl* file

## Usage

* A */data* folder should be created in the root of the repo to store output data
* `main.py` - Collates all utilities and runs in the required order
