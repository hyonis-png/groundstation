import csv
import math
from flask import Flask, jsonify, render_template


app = Flask(__name__)

telemetry = []


def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None



with open("Flight_1001 - Copy of Flight_1001_FINAL.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        time = safe_float(row["TIMESTAMP"])
        pressure = safe_float(row["PRESSURE"])
        estimated_altitude = 44330 * (1 - (pressure / 101325.0) ** (1 / 5.255))
        if pressure is not None:
            estimated_altitude = 44330 * (
              1 - (pressure / 101325.0) ** (1 / 5.255)
    )
        else:
            estimated_altitude = None
        gyro_x = safe_float(row["GYRO_X"])
        gyro_y = safe_float(row["GYRO_Y"])
        gyro_z = safe_float(row["GYRO_Z"])

        accel_x = safe_float(row["ACCEL_X"])
        accel_y = safe_float(row["ACCEL_Y"])
        accel_z = safe_float(row["ACCEL_Z"])

        voltage = safe_float(row["VOLTAGE"])
        current = safe_float(row["CURRENT"])

        gps_time = row["GPS_TIME"]

        gps_altitude = safe_float(row["GPS_ALTITUDE"])
        gps_latitude = safe_float(row["GPS_LATITUDE"])
        gps_longitude = safe_float(row["GPS_LONGITUDE"])

        gps_sats = safe_int(row["GPS_SATS"])


        # ---------------------------------
        # Acceleration magnitude
        # ---------------------------------

        if (
            accel_x is not None and
            accel_y is not None and
            accel_z is not None
        ):
            acceleration_magnitude = math.sqrt(
                accel_x**2 +
                accel_y**2 +
                accel_z**2
            )

        else:
            acceleration_magnitude = None


        # ---------------------------------
        # Gyroscope magnitude
        # ---------------------------------

        if (
            gyro_x is not None and
            gyro_y is not None and
            gyro_z is not None
        ):
            gyro_magnitude = math.sqrt(
                gyro_x**2 +
                gyro_y**2 +
                gyro_z**2
            )

        else:
            gyro_magnitude = None


        # ---------------------------------
        # Create telemetry sample
        # ---------------------------------

        sample = {

            "time": time,
            "pressure": pressure,
            "altitude": estimated_altitude,
            "gyro_x": gyro_x,
            "gyro_y": gyro_y,
            "gyro_z": gyro_z,

            "accel_x": accel_x,
            "accel_y": accel_y,
            "accel_z": accel_z,

            "acceleration_magnitude": acceleration_magnitude,
            "gyro_magnitude": gyro_magnitude,

            "voltage": voltage,
            "current": current,

            "gps_time": gps_time,
            "gps_altitude": gps_altitude,
            "gps_latitude": gps_latitude,
            "gps_longitude": gps_longitude,
            "gps_sats": gps_sats
        }

        telemetry.append(sample)


# ---------------------------------
# Homepage
# ---------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------
# Telemetry API
# ---------------------------------

@app.route("/api/telemetry/<int:index>")
def get_telemetry(index):

    if index < len(telemetry):
        return jsonify(telemetry[index])

    return jsonify({"finished": True})


# ---------------------------------
# Start Flask
# ---------------------------------

if __name__ == "__main__":
    app.run(debug=True)