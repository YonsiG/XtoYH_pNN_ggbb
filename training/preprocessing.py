from unicodedata import numeric
from pandas import Categorical
from sklearn.compose import ColumnTransformer
from sklearn.datasets import fetch_openml
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer, QuantileTransformer

import numpy as np
import tracemalloc
get_memory = lambda: np.array(tracemalloc.get_traced_memory())/1024**3

import common

def autoDetermineFeatureTypes(df, train_features):
  #for each in df.columns:
  #  print(each, df[each].dtype)

  numeric_features = []
  categorical_features = []
  for feature in train_features:
    if "float" in str(df[feature].dtype):
      numeric_features.append(feature)
    elif "int" in str(df[feature].dtype):
      categorical_features.append(feature)
    elif df[feature].dtype == bool:
      categorical_features.append(feature)
    else:
      print(feature, df[feature].dtype)
      raise Exception("Unexpected dtype")

  return numeric_features, categorical_features

def getNTransformedFeatures(df, train_features):
  """Find out how many training features there will be after transformation"""
  num, cat = autoDetermineFeatureTypes(df, train_features)
  n_features = len(num)
  for feat in cat:
    print(feat, np.unique(df[feat]))
    n_features += len(np.unique(df[feat]))
  print(n_features)
  return n_features

class Transformer:
  def __init__(self, numeric_features, categorical_features):
    self.numeric_features = numeric_features
    self.categorical_features = categorical_features

    self.scaler = StandardScaler()
    self.onehot = OneHotEncoder(handle_unknown="ignore", sparse=False)
    self.nan_to_zero = SimpleImputer(fill_value=0)

  def fit_transform(self, X, y, w):
    print("fit transform 1", get_memory())
    X.replace(common.dummy_val, np.nan, inplace=True)

    w[y==1] *= w[y==0].sum() / w[y==1].sum()
    print("fit transform 2", get_memory())
    X_numeric = self.scaler.fit_transform(X[self.numeric_features], sample_weight=w)
    print("fit transform 3", get_memory())
    X_numeric = self.nan_to_zero.fit_transform(X_numeric)
    print("fit transform 4", get_memory())
    X_categorical = self.onehot.fit_transform(X[self.categorical_features])
    print("fit transform 5", get_memory())
    return np.concatenate((X_categorical, X_numeric), axis=1).astype("float32")
    #return np.concatenate((X_categorical, X_numeric), axis=1)

  def transform(self, X, y=None):
    X.replace(common.dummy_val, np.nan, inplace=True)

    X_numeric = self.scaler.transform(X[self.numeric_features])
    X_numeric = self.nan_to_zero.transform(X_numeric)

    X_categorical = self.onehot.transform(X[self.categorical_features])

    return np.concatenate((X_categorical, X_numeric), axis=1).astype("float32")
    #return np.concatenate((X_categorical, X_numeric), axis=1)


