import re
import requests
import json


class Pincode:
    def __init__(self, pincode):
        self.pincode = pincode

    def validate_pincode(self):
        return bool(re.fullmatch("[1-9]\d{5}", self.pincode))

    def corresponding_pincode(self):
        if self.validate_pincode():
            return self.pincode