# README
This is ptm213's submission for MLDS400 homework #3.

It contains two logistic regression models (Python and R) that generate predictions for titanic passenger survival.

Anyone can use this repo to download the titanic-disaster data and run the logistic regression models for themselves. Here's how:

## Requirements
- Docker
- Python or R

## 1) Download the data
Download the three data sets about [passengers aboard the infamous Titanic disaster on April 15, 1912.](https://www.kaggle.com/competitions/titanic/data).
1. train.csv
2. test.csv
3. gender_submission.csv

## 2) Run the Python model
Build docker image with

`docker build -t titanic-py -f src/python/Dockerfile .`

Run docker image with

`docker run --rm -it -e DATA_DIR=/data -v "$PWD/src/data:/data" titanic-py`


## 3) Run the R model
Build docker image with

`docker build -t titanic-r -f src/r/Dockerfile .`

Run docker image with

`docker run --rm -it -e DATA_DIR=/data -v "$PWD/src/data:/data" titanic-r`