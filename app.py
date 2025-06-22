import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/',methods=['POST'] )
def index():
    data=request.get_json()
    source_currency=data['queryResult']['parameters']['unit-currency']['currency']
    amount=data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    cf=fetch_conversion_factor(source_currency, target_currency)
    final_amount=cf*amount
    response={
        'fulfillmentText':'{} {} is {} {}'.format(amount,source_currency,final_amount,target_currency)
    }
    print(final_amount)
    return jsonify(response)

def fetch_conversion_factor(source, target):
    url="https://v6.exchangerate-api.com/v6/edc0fcd814c28b607e72136c/pair/{}/{}".format(source,target)
    response=requests.get(url)
    response=response.json()
    return response["conversion_rate"]
if __name__ == "__main__":
    app.run(port=5000, debug=True)
