#!/usr/bin/env python3
import os
import sys
import pandas
import requests
import argparse

# usage
parser = argparse.ArgumentParser(
    description="""Script that enables a quick, API-based export from HackerOne to a compatible .csv format for fast upload to ThreadFix."""
)
parser.add_argument("h1_program_handle", help="your HackerOne program handle")
args = parser.parse_args()

# API variables
headers = {"Accept": "application/json"}
url = "https://api.hackerone.com/v1/"

# get H1 API creds from OS variables
user = os.environ.get("H1_IDENTIFIER")
token = os.environ.get("H1_TOKEN")
program = os.environ.get("H1_PROGRAM")

# create .csv file
df = pandas.DataFrame()

# add columns
df.insert(0, "LineText", "")
df.insert(0, "ColumnNumber", 1)
df.insert(0, "LineNumber", 1)
df.insert(0, "SourceFileName", "")
df.insert(0, "Date", "")
df.insert(0, "IssueID", "")
df.insert(0, "LongDescription", "")
df.insert(0, "ShortDescription", "")
df.insert(0, "NativeID", "")
df.insert(0, "parameter", "")
df.insert(0, "url", "")
df.insert(0, "Source", "HackerOne")
df.insert(0, "CWE", "")
df.insert(0, "Severity", "")

# fix severity values
df.replace(to_replace="critical", value="Critical", inplace=True)
df.replace(to_replace="high", value="High", inplace=True)
df.replace(to_replace="medium", value="Medium", inplace=True)
df.replace(to_replace="low", value="Low", inplace=True)
df.replace(to_replace="none", value="Info", inplace=True)

# pull all program reports
response = requests.get(
    "https://api.hackerone.com/v1/reports/",
    auth=(user, token),
    params={"filter[program][]": [sys.argv[1]]},
    headers=headers,
).text

# write file
df.to_csv("h1-export.csv", index=False)
# print(df)