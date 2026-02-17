from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sos", methods=["POST"])
def sos():
    data = request.get_json()
    lat = data["lat"]
    lon = data["lon"]

    # Overpass API query to find nearest police station within 5km
    overpass_url = "http://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    node
      ["amenity"="police"]
      (around:5000,{lat},{lon});
    out;
    """

    response = requests.post(overpass_url, data={"data": query})
    result = response.json()

    if result["elements"]:
        station = result["elements"][0]
        name = station["tags"].get("name", "Police Station")
        phone = station["tags"].get("phone", "Not Available")

        # Google Maps location link
        map_link = f"https://www.google.com/maps?q={lat},{lon}"

        return jsonify({
            "status": "success",
            "station_name": name,
            "phone": phone,
            "map_link": map_link
        })
    else:
        return jsonify({
            "status": "not_found",
            "station_name": "Not Found",
            "phone": "Not Available",
            "map_link": f"https://www.google.com/maps?q={lat},{lon}"
        })

if __name__ == "__main__":
    app.run(debug=True)
