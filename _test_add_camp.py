import urllib.parse, urllib.request

data = urllib.parse.urlencode({
    "camp_id": "CAMP_TEST_1",
    "location": "Test Location",
    "max_capacity": "10",
    "available_food_packets": "5",
    "available_medical_kits": "3",
    "volunteers": "A,B",
}).encode("utf-8")

req = urllib.request.Request("http://127.0.0.1:5000/camps/add", data=data, method="POST")
resp = urllib.request.urlopen(req, timeout=5)
print("POST /camps/add", resp.status, "->", resp.getheader("Location"))
