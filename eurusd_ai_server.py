import os
import csv
import pickle
import datetime
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression

LOG_CSV = 'analysis_log.csv'
MODEL_FILE = 'model.pkl'

def fetch_price():
    try:
        r = requests.get('https://api.exchangerate.host/latest?base=EUR&symbols=USD', timeout=5)
        r.raise_for_status()
        return round(r.json()['rates']['USD'], 5)
    except:
        return None

def log_data(timestamp, price, predicted):
    exists = os.path.isfile(LOG_CSV)
    with open(LOG_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(['timestamp','price','predicted'])
        writer.writerow([timestamp, price, predicted])

def train_model():
    if not os.path.isfile(LOG_CSV):
        return None
    df = pd.read_csv(LOG_CSV, parse_dates=['timestamp'])
    if len(df) < 6:
        return None
    prices = df['price'].values
    X, y = [], []
    for i in range(5, len(prices)):
        X.append(prices[i-5:i])
        y.append(prices[i])
    model = LinearRegression().fit(X, y)
    pickle.dump(model, open(MODEL_FILE, 'wb'))
    return model

def load_model():
    if os.path.isfile(MODEL_FILE):
        return pickle.load(open(MODEL_FILE, 'rb'))
    return None

def fetch_and_predict():
    price = fetch_price()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    model = load_model()
    if model is None:
        model = train_model()
    predicted = None
    trend = 'غير متاح'
    if model and price is not None:
        df = pd.read_csv(LOG_CSV) if os.path.isfile(LOG_CSV) else None
        if df is not None and len(df) >= 5:
            last = df['price'].values[-5:].tolist()
        else:
            last = [price]*5
        pred_price = round(model.predict([last])[0], 5)
        predicted = pred_price
        trend = '🔼 صاعد' if pred_price > price else '🔽 هابط'
    log_data(timestamp, price, predicted if predicted is not None else '')
    return {'price': price, 'predicted_price': predicted, 'trend': trend}