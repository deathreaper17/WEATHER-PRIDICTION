from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'weather_db'
app.config['MYSQL_HOST'] = 'rds-instance.amazonaws.com'
mysql = MySQL(app)

# Define endpoints for CRUD operations
@app.route('/weather/<city_name>', methods=['GET'])
def get_weather(city_name):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM weather WHERE city_name = %s', (city_name,))
    data = cur.fetchone()
    cur.close()
    if data is None:
        return jsonify({'error': 'City not found'}), 404
    else:
        return jsonify({
            'city_name': data[0],
            'temperature': data[1],
            'humidity': data[2],
            'wind_speed': data[3],
            'pressure': data[4],
            'description': data[5],
            'last_updated': data[6]
        })

@app.route('/weather', methods=['POST'])
def add_weather():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO weather VALUES (%s, %s, %s, %s, %s, %s, NOW())',
                (data['city_name'], data['temperature'], data['humidity'], data['wind_speed'], data['pressure'], data['description']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True})

@app.route('/weather/<city_name>', methods=['PUT'])
def update_weather(city_name):
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute('UPDATE weather SET temperature = %s, humidity = %s, wind_speed = %s, pressure = %s, description = %s, last_updated = NOW() WHERE city_name = %s',
                (data['temperature'], data['humidity'], data['wind_speed'], data['pressure'], data['description'], city_name))
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True})

@app.route('/weather/<city_name>', methods=['DELETE'])
def delete_weather(city_name):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM weather WHERE city_name = %s', (city_name,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True})
