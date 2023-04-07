CREATE TABLE weather (
    city_name VARCHAR(255) PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    pressure FLOAT,
    description VARCHAR(255),
    last_updated TIMESTAMP
);
