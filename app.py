from flask import Flask, jsonify, request, render_template
from RepositoryForObject import ObjectRepository
from Scrapper import Scrapper
from Pincode import Pincode
import threading

app = Flask(__name__)

obj = ObjectRepository()
driver_path = obj.getDriverPath()


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
                p = Scrapper(executable_path=driver_path)
                # t1 = threading.Thread(target=p.pharmeasy_result(product=required_product, pincode=delivery_pincode))
                # t2 = threading.Thread(target=p.netmeds_result(product=required_product, pincode=delivery_pincode))
                # t1.start()
                # t2.start()
                # t1.join()
                # t2.join()
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
