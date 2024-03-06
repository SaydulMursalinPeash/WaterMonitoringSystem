from flask import Flask, jsonify

app = Flask(__name__)

# Route for handling GET request
@app.route('/api/sensors', methods=['GET'])
def get_sensor_data():
    # Logic to fetch sensor data (replace this with your data fetching logic)
    sensor_data = {'temperature': 25.5, 'humidity': 50.0}  # Replace with actual data
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run Flask app on port 5000
