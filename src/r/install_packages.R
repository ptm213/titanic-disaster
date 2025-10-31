# Install required R packages for the Titanic Disaster Analysis Project
pkgs <- c("readr","dplyr","stringr", "tidyr")  # add what you actually use
# "glmnet", 
install.packages(pkgs, repos = "https://cloud.r-project.org")
