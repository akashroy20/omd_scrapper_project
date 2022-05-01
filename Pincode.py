import requests
import json


class Pincode:
    def __init__(self, pincode):
        self.pincode = pincode

    def pincode_text(self):
        pincode_api = "https://api.postalpincode.in/pincode/"
        response = requests.get(pincode_api + self.pincode)
        response1 = json.loads(response.text)
        return response1

    def pincode_check(self):
        if bool(self.pincode_text()[0]['Status'] == "Success"):
            return True
        else:
            return False

    def corresponding_pincode(self):
        if self.pincode_check():
            return self.pincode

    def corresponding_city(self):
        if self.pincode_check():
            return self.pincode_text()[0]['PostOffice'][0]['District']