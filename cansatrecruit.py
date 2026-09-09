import csv
import math
from flask import Flask, jsonify, render_template

app = Flask(__name__)

telemetry = []

with open("Flight_1001 - Copy of Flight_1001_FINAL.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        time = float(row["TIMESTAMP"])
        pressure = float(row["PRESSURE"])

        gyro_x = float(row["GYRO_X"])
        gyro_y = float(row["GYRO_Y"])
        gyro_z = float(row["GYRO_Z"])

        accel_x = float(row["ACCEL_X"])
        accel_y = float(row["ACCEL_Y"])
        accel_z = float(row["ACCEL_Z"])

        voltage = float(row["VOLTAGE"])
        current = float(row["CURRENT"])

        gps_time = row["GPS_TIME"]
        gps_altitude = float(row["GPS_ALTITUDE"])
        gps_latitude = float(row["GPS_LATITUDE"])
        gps_longitude = float(row["GPS_LONGITUDE"])
        gps_sats = int(row["GPS_SATS"])

        acceleration_magnitude = math.sqrt(
            accel_x**2 +
            accel_y**2 +
            accel_z**2
        )

        sample = {
            "time": time,
            "pressure": pressure,

            "gyro_x": gyro_x,
            "gyro_y": gyro_y,
            "gyro_z": gyro_z,

            "accel_x": accel_x,
            "accel_y": accel_y,
            "accel_z": accel_z,

            "acceleration_magnitude": acceleration_magnitude,

            "voltage": voltage,
            "current": current,

            "gps_time": gps_time,
            "gps_altitude": gps_altitude,
            "gps_latitude": gps_latitude,
            "gps_longitude": gps_longitude,
            "gps_sats": gps_sats
        }

        telemetry.append(sample)


# Homepage
@app.route("/")
def index():
    return render_template("index.html")


# API
@app.route("/api/telemetry")
def get_telemetry():
    return jsonify(telemetry)


if __name__ == "__main__":
    app.run(debug=True)