# README
## Context
This is Paul Miyashita's submission for MLDS400 homework #3.

It contains two logistic regression models (Python and R) that generate predictions for titanic passenger survival.

Anyone can use this repo to download the titanic-disaster data and run the logistic regression models for themselves. Here's how:

## Requirements
- Docker
- Python or R

## Download the data first
Download the three data sets about [passengers aboard the infamous Titanic disaster on April 15, 1912.](https://www.kaggle.com/competitions/titanic/data).
1. train.csv
2. test.csv
3. gender_submission.csv

## How to to run the Python model
Build docker image.
`docker build -t titanic-py -f src/python/Dockerfile .`

Run docker image
(mount local data; or omit -e/-v if you baked data while testing)
`docker run --rm -it -e DATA_DIR=/data -v "$PWD/src/data:/data" titanic-py`


## How to to run the R model
Build docker image.
`docker build -t titanic-r -f src/r/Dockerfile .`

Run docker image.
`docker run --rm -it -e DATA_DIR=/data -v "$PWD/src/data:/data" titanic-r`