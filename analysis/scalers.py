import numpy as np

def min_max_scaler(X, feature_range=(0, 1)):
    min_ = X.min(axis=0)
    max_ = X.max(axis=0)
    X_std = (X - min_) / (max_ - min_)
    X_scaled = X_std * (feature_range[1] - feature_range[0]) + feature_range[0]
    return X_scaled

def robust_scaler(X):
    median = np.median(X, axis=0)
    quartile_1 = np.percentile(X, 25, axis=0)
    quartile_3 = np.percentile(X, 75, axis=0)
    IQR = quartile_3 - quartile_1
    X_scaled = (X - median) / IQR
    return X_scaled