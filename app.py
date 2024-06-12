from flask import Flask, request, jsonify

app = Flask(__name__)

# Data structures to store visits
customers_visits = {}
website_visits = {}

@app.route('/VisitWebsite', methods=['POST'])
def visit_website():
    data = request.get_json()
    customer_id = data['customerId']
    device_id = data['deviceId']
    website_id = data['websiteId']
    
    if customer_id not in customers_visits:
        customers_visits[customer_id] = {}
    
    if website_id not in customers_visits[customer_id]:
        customers_visits[customer_id][website_id] = set()
    
    customers_visits[customer_id][website_id].add(device_id)
    
    if website_id not in website_visits:
        website_visits[website_id] = set()
    
    website_visits[website_id].add(customer_id)
    
    return jsonify({"message": "Visit tracked successfully"}), 200

@app.route('/GetWebsiteVisitCountForCustomer', methods=['GET'])
def get_website_visit_count_for_customer():
    customer_id = request.args.get('customerId')
    website_id = request.args.get('websiteId')
    
    if customer_id in customers_visits and website_id in customers_visits[customer_id]:
        visit_count = len(customers_visits[customer_id][website_id])
    else:
        visit_count = 0
    
    return jsonify({"customer_id": customer_id, "website_id": website_id, "visit_count": visit_count}), 200

@app.route('/GetOverallWebsiteHitCount', methods=['GET'])
def get_overall_website_hit_count():
    website_id = request.args.get('websiteId')
    
    if website_id in website_visits:
        hit_count = len(website_visits[website_id])
    else:
        hit_count = 0
    
    return jsonify({"website_id": website_id, "hit_count": hit_count}), 200

if __name__ == '__main__':
    app.run(debug=True)
