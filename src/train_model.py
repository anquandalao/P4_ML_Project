# train_model.py
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from data_preprocessing import load_and_preprocess_data

def train_and_save_models(X_train, y_train):
    dt_model = DecisionTreeClassifier()
    dt_model.fit(X_train, y_train)
    rf_model = RandomForestClassifier(n_estimators=100)
    rf_model.fit(X_train, y_train)
    joblib.dump(dt_model, '../models/decision_tree_model.pkl')
    joblib.dump(rf_model, '../models/random_forest_model.pkl')

def evaluate_models(X_test, y_test):
    dt_model = joblib.load('../models/decision_tree_model.pkl')
    rf_model = joblib.load('../models/random_forest_model.pkl')
    dt_predictions = dt_model.predict(X_test)
    rf_predictions = rf_model.predict(X_test)
    print("Decision Tree Accuracy:", accuracy_score(y_test, dt_predictions))
    print("Random Forest Accuracy:", accuracy_score(y_test, rf_predictions))

if __name__ == "__main__":
    file_path = '../data/westermo_traffic.csv'
    X_train, X_test, y_train, y_test = load_and_preprocess_data(file_path)
    train_and_save_models(X_train, y_train)
    evaluate_models(X_test, y_test)
