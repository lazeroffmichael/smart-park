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
from sklearn.metrics import classification_report, confusion_matrix


if __name__ == '__main__':
    # Open the data file
    df = pd.read_csv('../simulations/data/paths.csv')

    # Testing data file
    test_df = pd.read_csv('../simulations/data/test_paths.csv')

    # Get just the coordinate data for the x features
    x_train = df[df.columns[2:62]]

    # Y feature is whether the path enters the parking lot
    y_train = df['enter-parking'].values

    print(x_train)
    print(y_train)

    # Get the testing data from the testing data file
    x_test = test_df[test_df.columns[2:62]]

    y_test = test_df['enter-parking'].values

    # Scalar object
    scalar = MinMaxScaler()

    # Scale the data
    scalar.fit(x_train)
    x_train = scalar.transform(x_train)
    x_test = scalar.transform(x_test)

    # Early stop object - prevents initial overtraining from too many epochs
    early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=20)

    # Create model
    model = Sequential()

    # 60 neurons for the input layer
    model.add(Dense(60, activation='relu'))

    # Dropout layer 1
    model.add(Dropout(0.5))

    model.add(Dense(45, activation='relu'))

    # 1 inner layer
    model.add(Dense(30, activation='relu'))

    # Dropout layer 2
    model.add(Dropout(0.5))

    # Binary classifcation
    model.add(Dense(1, activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam')

    # Fit model
    model.fit(x=x_train,
              y=y_train,
              epochs=150,
              validation_data=(x_test, y_test),
              callbacks=early_stop)

    # model.fit(x=X_train,
    #           y=y_train,
    #           epochs=50,
    #           validation_data=(X_test, y_test))

    losses = pd.DataFrame(model.history.history)

    print(losses)

    print(losses.plot())

    predictions = (model.predict(x_test) > 0.5).astype("int32")

    # Print results
    print(classification_report(y_test, predictions))
    print(confusion_matrix(y_test, predictions))

    # Save the model
    model.save('saved_model')
