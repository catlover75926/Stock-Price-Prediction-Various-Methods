import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, accuracy_score, confusion_matrix
from scipy.stats import fisher_exact
import tensorflow as tf

# Step 1: Data Preparation
# Load the training data
train_data = pd.read_csv('../example_data/train.csv', header=None)
X_train = train_data.iloc[:, :-1]
Y_train = train_data.iloc[:, -1]

# Scale the feature data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

# Step 2: Model Creation
# Create a classification model
input_features = X_train.shape[1]
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(input_features,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Step 3: Training the Model
# Train the model
model.fit(X_train, Y_train, epochs=10, batch_size=32)

# Step 4: Testing the Model
# Load the test data
test_data = pd.read_csv('../example_data/test.csv', header=None)
X_test = test_data.iloc[:, :-1]
Y_test = test_data.iloc[:, -1]

# Scale the feature data
X_test = scaler.transform(X_test)

# Get predictions
Y_pred = (model.predict(X_test) > 0.5).astype(int).flatten()

# Calculate metrics
precision = precision_score(Y_test, Y_pred)
accuracy = accuracy_score(Y_test, Y_pred)
tn, fp, fn, tp = confusion_matrix(Y_test, Y_pred).ravel()

# Step 5: Statistical Analysis
# Perform Fisher's exact test
table = [[tp, fp], [fn, tn]]
_, p_value = fisher_exact(table)

# Step 6: Output
# Print the required information
print(f'Precision: {precision}')
print(f'Accuracy: {accuracy}')
print(f'P-value of precision: {p_value}')
