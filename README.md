# Titanic – Reproducible Logistic Regression (Python & R)
This is ptm213's submission for MLDS400 homework #3.

It contains two Dockerized logistic regression models (Python and R) that generate predictions for titanic passenger survival.

Anyone can use this repo to download the titanic-disaster data and run the logistic regression models for themselves. No datasets are committed; follow the steps below to run reproducibly.

## Requirements
- Docker Desktop (Linux/macOS/Windows)
- (Optional) Python/R locally if you want to peek, not required to run

## 0) Clone this repo
```bash
git clone https://github.com/ptm213/titanic-disaster.git
cd titanic-disaster
```

## 1) Download the data
Download three data sets from [Kaggle (Titanic)](https://www.kaggle.com/competitions/titanic/data).

Create src/data/ folder and upload all three files:
1. src/data/train.csv
2. src/data/test.csv
3. src/data/gender_submission.csv

Note: Data is ignored by .gitignore and not baked into images via .dockerignore.


## 2) Run the Python model
Build docker image with

`docker build -t titanic-py -f src/python/Dockerfile .`

Run docker image (macOS/Linux) with

`docker run --rm -it -e DATA_DIR=/data -v "$PWD/src/data:/data" titanic-py`

Run docker image (Windows PowerShell) with

`docker run --rm -it -e DATA_DIR=/data -v "${PWD}\src\data:/data" titanic-py`


## 3) Run the R model
Build docker image with

`docker build -t titanic-r -f src/r/Dockerfile .`

Run docker image (macOS/Linux) with

`docker run --rm -it -e DATA_DIR=/data -v "$PWD/src/data:/data" titanic-r`

Run docker image (Windows PowerShell) with

`docker run --rm -it -e DATA_DIR=/data -v "${PWD}\src\data:/data" titanic-r`

## What you’ll see:
- Printed steps: load → preview → missing values → model fit → training accuracy → test predictions.
- Files written (if PassengerId exists):
    - Python: src/data/submission.csv
    - R: src/data/submission_r.csv

## Troubleshooting
- Cache error during build:
    - `docker build --no-cache -t titanic-r -f src/r/Dockerfile .`
    - or `docker builder prune -af` then rebuild.
- R build is slow the first time: CRAN packages install; subsequent builds are fast if install_packages.R hasn’t changed.
- Running via Docker Desktop GUI: set env var DATA_DIR=/data and mount host …/src/data → container /data.
