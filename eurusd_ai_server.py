from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = 'xDvsubbu4sYZ9W5R2XSfCWxVUZc4JSlK'
API_URL = f'https://api.apilayer.com/exchangerates_data/latest?base=USD&symbols=EUR'

headers = {
    "apikey": API_KEY
}

@app.route('/eurusd', methods=['GET'])
def get_eurusd_rate():
    try:
        response = requests.get(API_URL, headers=headers)
        data = response.json()

        if 'error' in data:
            return jsonify({"error": data["error"]["info"]}), 503

        eurusd = data['rates']['EUR']
        return jsonify({
            "success": True,
            "pair": "EUR/USD",
            "price": eurusd
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5005)
