from flask import Flask, jsonify, request, render_template
from RepositoryForObject import ObjectRepository
from Scrapper import Scrapper
from Pincode import Pincode

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
            if pc.pincode_check() and required_product != "":
                valid_pincode = pc.corresponding_pincode()
                dict1 = {"SearchedProduct": required_product, "Pincode": valid_pincode}
                p = Scrapper(executable_path=driver_path)
                pharmeasy = p.pharmeasy_result(product=required_product, pincode=pc.corresponding_pincode())
                netmeds = p.netmeds_result(product=required_product, pincode=pc.corresponding_pincode())
                dict1["pharmeasy"] = pharmeasy
                dict1["netmeds"] = netmeds
                return render_template('result.html', result=dict1)
            else:
                return render_template('invalid_input.html')
        except Exception as e:
            raise Exception(str(e))


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
