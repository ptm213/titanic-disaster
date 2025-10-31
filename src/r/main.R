# src/r/main.R
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
})

log <- function(msg) cat(paste0("[INFO] ", msg, "\n"))

# Where to find CSVs: default to "src/data" for local runs; allow override via env
DATA_DIR <- Sys.getenv("DATA_DIR", unset = "src/data")
train_path <- file.path(DATA_DIR, "train.csv")
test_path  <- file.path(DATA_DIR, "test.csv")

# --- Step 23: Load packages + train.csv ---
if (!file.exists(train_path)) {
  stop(paste("ERROR: train.csv not found at", train_path))
}
log(paste("Loading train.csv from:", train_path))
train <- read_csv(train_path, show_col_types = FALSE)
log(paste("Train shape:", nrow(train), "rows x", ncol(train), "cols"))

# --- Step 14 (R version): light exploration / adjustments ---
log("Preview (first 5 rows):")
print(utils::head(train, 5))

log("Missing values (top):")
print(sort(colSums(is.na(train)), decreasing = TRUE)[1:min(10, ncol(train))])

features <- c("Sex", "Age")
target   <- "Survived"
log(paste("Selected features:", paste(features, collapse = ", ")))
log(paste("Target:", target))

# Impute missing Age with median
if ("Age" %in% names(train)) {
  med_age <- median(train$Age, na.rm = TRUE)
  train$Age <- ifelse(is.na(train$Age), med_age, train$Age)
  log(paste("Imputed Age NAs with median:", round(med_age, 2)))
}

# Ensure Sex is a factor
if ("Sex" %in% names(train)) {
  train$Sex <- factor(train$Sex)
}

# --- Step 15: Logistic regression on training set (Sex + Age) ---
# Keep only needed columns and drop rows with any remaining NAs
train_use <- train %>%
  dplyr::select(all_of(c(features, target))) %>%
  tidyr::drop_na()

log(paste("Fitting logistic regression on", nrow(train_use), "rows"))
fit <- glm(Survived ~ Sex + Age, data = train_use, family = binomial())

# Print coefficients
log("Model coefficients (log-odds):")
print(coef(summary(fit)))

# --- Step 16: Training accuracy ---
train_probs <- predict(fit, newdata = train_use, type = "response")
train_pred  <- ifelse(train_probs >= 0.5, 1L, 0L)
train_acc   <- mean(train_pred == train_use$Survived)
log(sprintf("Training accuracy: %.4f", train_acc))

# --- Step 17: Load test.csv & predict ---
if (!file.exists(test_path)) {
  stop(paste("ERROR: test.csv not found at", test_path))
}
log(paste("Loading test.csv from:", test_path))
test <- read_csv(test_path, show_col_types = FALSE)
log(paste("Test shape:", nrow(test), "rows x", ncol(test), "cols"))

# Basic prep on test to align with train
if (!all(features %in% names(test))) {
  missing <- setdiff(features, names(test))
  stop(paste("ERROR: test.csv is missing required columns:", paste(missing, collapse = ", ")))
}

# Impute Age on test using train median
if ("Age" %in% names(test)) {
  test$Age <- ifelse(is.na(test$Age), med_age, test$Age)
}
# Match Sex levels to train (unseen values become NA → drop/handle)
test$Sex <- factor(test$Sex, levels = levels(train$Sex))

# Predict
test_use <- test %>% dplyr::select(all_of(features)) %>% tidyr::drop_na()
log(paste("Predicting on", nrow(test_use), "test rows"))
test_probs <- predict(fit, newdata = test_use, type = "response")
test_pred  <- ifelse(test_probs >= 0.5, 1L, 0L)

# --- Step 18: Test accuracy if labels exist ---
if ("Survived" %in% names(test)) {
  y_test <- test$Survived[!is.na(test$Sex) & !is.na(test$Age)]
  test_acc <- mean(test_pred == y_test)
  log(sprintf("Test accuracy: %.4f", test_acc))
} else {
  surv_rate <- mean(test_pred)
  log("Test accuracy: N/A (no Survived in test.csv).")
  log(sprintf("Predicted survival rate on test: %.3f", surv_rate))
  log(paste("First 10 predictions:", paste(head(test_pred, 10), collapse = ",")))
}

# Save a submission if PassengerId exists
if ("PassengerId" %in% names(test)) {
  out_path <- file.path(DATA_DIR, "submission_r.csv")
  subm <- data.frame(PassengerId = test$PassengerId[!is.na(test$Sex) & !is.na(test$Age)],
                     Survived    = test_pred)
  write.csv(subm, out_path, row.names = FALSE)
  log(paste("Saved predictions to:", out_path))
}

log("Done (R).")
