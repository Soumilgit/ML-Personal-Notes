import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

a = 5
b = 3

x_positive_branch = np.linspace(a, a + 20, 200)
x_negative_branch = np.linspace(-a - 20, -a, 200)

y_pos_upper = b * np.sqrt((x_positive_branch**2 / a**2) - 1)
y_pos_lower = -b * np.sqrt((x_positive_branch**2 / a**2) - 1)

y_neg_upper = b * np.sqrt((x_negative_branch**2 / a**2) - 1)
y_neg_lower = -b * np.sqrt((x_negative_branch**2 / a**2) - 1)

X_data = np.concatenate([
    x_positive_branch, x_positive_branch,
    x_negative_branch, x_negative_branch
])

y_data = np.concatenate([
    y_pos_upper, y_pos_lower,
    y_neg_upper, y_neg_lower
])

noise_level = 0.5
y_data_noisy = y_data + np.random.normal(0, noise_level, y_data.shape[0])

X_data_reshaped = X_data.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(
    X_data_reshaped, y_data_noisy, test_size=0.2, random_state=42
)

ml_model = MLPRegressor(
    hidden_layer_sizes=(50, 25),
    activation='relu',
    solver='adam',
    max_iter=1000,
    random_state=42,
    learning_rate_init=0.01
)

print("Training the model...")
ml_model.fit(X_train, y_train)
print("Training complete.")

score = ml_model.score(X_test, y_test)
print(f"Model R^2 score on test data: {score:.4f}")

x_plot = np.linspace(-a-20, a+20, 1000).reshape(-1, 1)

y_predicted = ml_model.predict(x_plot)

plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(12, 8))

plt.scatter(X_train, y_train, color='dodgerblue', s=15, alpha=0.6, label='Noisy Training Data')

plt.plot(X_data, y_data, 'k--', lw=2, label='Original Hyperbola (Ground Truth)')

sort_indices = np.argsort(x_plot.flatten())
plt.plot(x_plot.flatten()[sort_indices], y_predicted[sort_indices], color='red', lw=3, label='ML Model Simulation')

plt.title('Machine Learning Simulation of a Hyperbola', fontsize=16)
plt.xlabel('X-axis', fontsize=12)
plt.ylabel('Y-axis', fontsize=12)
plt.axhline(0, color='grey', lw=0.5)
plt.axvline(0, color='grey', lw=0.5)
plt.legend(fontsize=10)
plt.grid(True)
plt.axis('equal')
plt.savefig('hyperbola_simulation.png')
