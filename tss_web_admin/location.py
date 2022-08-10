
import requests
response = requests.get(f'https://ipapi.co/1.39.78.40/json/').json()
location_data = {
        "ip": '103.70.199.235',
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
}

print("location data:::::")
print(response)
# print(location_data)