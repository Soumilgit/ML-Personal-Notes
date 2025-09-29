import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

n_samples = 1500

x = np.random.uniform(-10, 10, n_samples)
y = np.random.uniform(-10, 10, n_samples)

def complex_paraboloid(x, y):
    return 0.1 * (x - 2)**2 + 0.05 * (y + 3)**2 + 5

z_true = complex_paraboloid(x, y)

noise_level = 5.0
z_noisy = z_true + noise_level * np.random.randn(n_samples)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z_noisy, c=z_noisy, cmap='viridis', alpha=0.6)
ax.set_title("Generated Noisy Paraboloid Data")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
plt.show()

X = np.vstack((x, y)).T
y_target = z_noisy

X_train, X_test, y_train, y_test = train_test_split(X, y_target, test_size=0.2, random_state=42)

models = {
    "Linear Regression": LinearRegression(),
    "Polynomial Regression (Degree 2)": Pipeline([
        ("poly_features", PolynomialFeatures(degree=2, include_bias=False)),
        ("lin_reg", LinearRegression())
    ]),
    "Neural Network (MLP)": MLPRegressor(hidden_layer_sizes=(64, 32),
                                         max_iter=1000,
                                         activation='relu',
                                         solver='adam',
                                         random_state=42,
                                         early_stopping=True),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100,
                                                 learning_rate=0.1,
                                                 max_depth=4,
                                                 random_state=42)
}

trained_models = {}
model_scores = {}

print("--- Training and Evaluating Models ---")
for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    trained_models[name] = model
    model_scores[name] = mse
    print(f"  -> Test MSE: {mse:.4f}\n")

x_grid, y_grid = np.meshgrid(np.linspace(-10, 10, 30), np.linspace(-10, 10, 30))
X_grid = np.vstack([x_grid.ravel(), y_grid.ravel()]).T

fig = plt.figure(figsize=(16, 12))
fig.suptitle('Comparison of ML Models Learning a Paraboloid', fontsize=20)

ax = fig.add_subplot(2, 3, 1, projection='3d')
ax.scatter(x, y, z_noisy, c=z_noisy, cmap='viridis', alpha=0.3, label='Original Data')
ax.set_title("1. Original Noisy Data")
ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")

plot_index = 2
for name, model in trained_models.items():
    z_pred_grid = model.predict(X_grid).reshape(x_grid.shape)
    
    ax = fig.add_subplot(2, 3, plot_index, projection='3d')
    ax.plot_surface(x_grid, y_grid, z_pred_grid, cmap='viridis', alpha=0.8)
    
    mse = model_scores[name]
    ax.set_title(f"{plot_index}. {name}\nMSE: {mse:.2f}")
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    plot_index += 1

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
