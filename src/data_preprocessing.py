# data_preprocessing.py
import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    features = ['src_ip', 'dst_ip', 'src_port', 'dst_port', 'protocol', 'packet_length']
    X = data[features]
    y = data['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    file_path = '../data/westermo_traffic.csv'
    X_train, X_test, y_train, y_test = load_and_preprocess_data(file_path)
