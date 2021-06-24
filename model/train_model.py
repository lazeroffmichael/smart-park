"""
Module for implementing and training the model
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


def main():
    # Get the data from the file
    paths = pd.read_csv('../simulations/csv_paths/cottage_grove_paths.csv')

    # Get the first coordinate pair
    pass


def split_data(data, start, end):
    """
    Splits and returns the data from the columns

    Parameters:
        data: The original dataframe
        start: Starting column (inclusive)
        end: Ending column (exclusive)

    Returns:
        The split up columns of the data frame
    """
    return data[data.columns[start, end]]


if __name__ == '__main__':
    # Open the data file
    df = pd.read_csv('../simulations/csv_paths/cottage_grove_paths.csv')

    # Get just the coordinate data for the x features
    X = df[df.columns[1:61]]

    # Y feature is whether the path enters the parking lot
    label = df['enter-parking'].values

    # Split the training and testing data
    X_train, X_test, y_train, y_test = train_test_split(X, label, test_size=0.25, random_state=101)

    # Scalar object
    scaler = MinMaxScaler()

    # Scale the data
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # Early stop object - prevents initial overtraining from too many epochs
    early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=25)

    # Create model
    model = Sequential()

    # 60 neurons for the input layer
    model.add(Dense(60, activation='relu'))

    # Dropout layer 1
    model.add(Dropout(0.5))

    # 1 inner layer
    model.add(Dense(30, activation='relu'))

    # Dropout layer 2
    model.add(Dropout(0.5))

    # Binary classifcation
    model.add(Dense(1, activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam')

    # Fit model
    model.fit(x=X_train,
              y=y_train,
              epochs=300,
              validation_data=(X_test, y_test),
              callbacks=early_stop)

    # Save the model
    model.save('saved_model')
