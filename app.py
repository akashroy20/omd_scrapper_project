from flask import Flask, jsonify, request, render_template
from RepositoryForObject import ObjectRepository
from Scrapper import Scrapper
from Pincode import Pincode
from selenium import webdriver
import os

app = Flask(__name__)

obj = ObjectRepository()
driver_path = obj.getDriverPath()
op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=op)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def search_result():
    if request.method == 'POST':
        try:
            required_product = request.form['requiredmedicine']
            delivery_pincode = request.form['pinc']
            pc = Pincode(delivery_pincode)
            if pc.pincode_check():
                valid_pincode = pc.corresponding_pincode()
            else:
                valid_pincode = "Invalid pincode!!"
            dict1 = {"SearchedProduct": required_product, "Pincode": valid_pincode}
            p = Scrapper(executable_path=driver_path)
            pharmeasy = p.pharmeasy_result(product=required_product, pincode=pc.corresponding_pincode())
            dict1["pharmeasy"] = pharmeasy
            netmed = p.netmeds_result(product=required_product, pincode=pc.corresponding_pincode())
            dict1["netmeds"] = netmed
            return render_template('result.html', result=dict1)
        except Exception as e:
            print(e)
    else:
        return render_template('index.html')


@app.route('/via_postman', methods=['GET', 'POST'])
def via_postman():
    if request.method == 'POST':
        delivery_pincode = request.json['pincode']
        required_product = request.json['product']
        dict = {}
        try:
            pc = Pincode(delivery_pincode)
            dict["Searched Product"] = required_product
            if pc.pincode_check():
                dict["Pincode"] = pc.corresponding_pincode()
                p = Scrapper(executable_path=driver)
                pharmeasy = p.pharmeasy_result(product=required_product, pincode=pc.corresponding_pincode())
                netmeds = p.netmeds_result(product=required_product, pincode=pc.corresponding_pincode())
                dict["pharmeasy"] = pharmeasy
                dict["netmeds"] = netmeds
            else:
                dict["Pincode"] = "Enter valid pincode!!"
            return jsonify(dict)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    app.run(debug=True)
