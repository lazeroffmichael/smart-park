"""
Displays metrics for the trained model
"""

import tensorflow as tf
import pandas as pd

if __name__ == '__main__':
    # Load the model
    model = tf.keras.models.load_model('saved_model')

    # Get losses
    losses = pd.DataFrame(model.history.history)

    losses.plot()

    predictons = model.predict_classes(X_test)