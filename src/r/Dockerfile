# Dockerfile for R environment to run Titanic Disaster Analysis
# This file creates an isolated environment ("image") containing
# all the code and dependencies needed to run the Titanic Disaster analysis in R.
# On the Docker desktop app, it creates an image called "titanic-disaster-r" 
# that you can then activate to build a Docker container.

# Use an official R base image
FROM r-base:4.3.3 

# Set the default working directory inside the container.
WORKDIR /app 

# Install R packages separately for better build caching
COPY src/r/install_packages.R /app/install_packages.R

# RUN Rscript install_packages.R
RUN Rscript /app/install_packages.R

# Copy your R script
COPY src/r/main.R /app/main.R

# Point your script to data via env var (mount at /data when running)
ENV DATA_DIR=/data

CMD ["Rscript","/app/main.R"]