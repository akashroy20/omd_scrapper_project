from RepositoryForObject import ObjectRepository
from Scrapper import Scrapper
from Pincode import Pincode

delivery_pincode = "700034"
required_product = "calpol 650"
delivery_city = "kolkata"
obj = ObjectRepository()
driver_path = obj.getDriverPath()

p = Scrapper(executable_path=driver_path)
dict = {}
try:
    pin = Pincode(delivery_pincode)
    #pharmeasy = p.pharmeasy_result(product=required_product,pincode=pin.corresponding_pincode())
    #dict["pharmeasy"] = pharmeasy
    #dict["pharmeasy link"] = p.currentPageUrl()
    netmed = p.netmeds_result(product=required_product, pincode=pin.corresponding_pincode())
    #dict["netmeds"] = netmed
    #dict["netmeds link"] = p.currentPageUrl()
    print(netmed)
    #print(p.currentPageUrl())
except Exception as e:
    print(e)

if locator.pharmeasy_composition():
    product_composition = self.divText(pname=locator.pharmeasy_composition(),
                                       page_source=product_page_source)
else:
    product_composition = "Not Found"