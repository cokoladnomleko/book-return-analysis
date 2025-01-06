# book-return-analysis
Prediction of late book returns at the time of checkout.

### This repo contains the analysis and modelling process for predicting late returns
Notebooks are to be run in the following order:

1. **data_cleaning.ipynb**
   - Contains code for cleaning messy data.
2. **data_analysis.ipynb**
   - Contains analysis and graphs of the library data, along with explanations.
3. **feature_engineering.ipynb**
   - Notebook for creating modelling features.
4. **modelling.ipynb**
   - Notebook for modelling and comparing models.

## Results

### Data Cleaning
Cleaning had to be done before any further analysis.<br/>
Numerical columns contained a mixture of characters and numbers - these were cleaned using regex.<br/>
Date columns contained dates in the future (book checkout time is considered current time), and these columns were removed from checkouts table.<br/>
Categorical columns had different formats for the same category and they were normalized.

## Data Analysis
The analysis pointed to some factors contributing to late returns.<br/>
The main one seems to be the *lenght of the books*, suggesting patrons simply need more time to read long books.<br/>
Another important effect is the *library and customers location* - the harder it is to get to the library the less likely a book is to be returned on time.
> [!NOTE]
> Long books could have longer return times. Customers that live far away could be allowed to return their books to a closer library.

## Feature Engineering
For categorical features, one-hot encoding is used.<br/>
Distance-based features are generated using openstreetmaps, overpass and geopy - distances from libraries to the nearest public transport station and the number of stations in walking distance.<br/>
Further work:
- Feature selection can be performed to exclude non-useful features
- Missing values in numerical columns can be imputed or missing indicators added
- More features could be generated, like customers distance to the chosen library

## Modelling
This is taken as a classification problem, with likelihood of late returns being estimated as prediction probability.<br/>
Models that will be tested are **XGBoost**, **RandomForestClassifier** and **SVM**.<br/>

Metrics used for model comparison are *accuracy*, *balanced accuracy*, *roc auc score* and *precision-recall curve*.<br/>
Best results are achieved with using XGBoost with the following parameters:
```
{'colsample_bytree': 0.7, 'learning_rate': 0.01, 'max_depth': 3, 'n_estimators': 300, 'scale_pos_weight': 5, 'subsample': 1.0}
```
