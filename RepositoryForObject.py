
class ObjectRepository:

    def __init__(self):
        pass

    def getDriverPath(self):
        return r"D:\python\pythonProject\chromedriver.exe"

    def PharmeasyUrl(self):
        return "https://pharmeasy.in/online-medicine-order?src=homecard"

    def PharmeasySearchXpath(self):
        return '//*[@id="__next"]/div[2]/div[2]/section[1]/div[1]/div/div/div[3]/div/div[2]/div[1]/div/input'

    def PharmeasyProductXpath(self):
        return '//*[@id="content-container"]/div[1]/div[1]/div/div[1]/div/div/a'

    def PharmeasyAddressXpath(self):
        return '//*[@id="__next"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div'

    def PharmeasyPincodeXpath(self):
        return '//*[@id="drawers-portal"]/div/div[2]/div[2]/div[1]/div[2]/div/div/input'

    def pharmeasy_delivery(self):
        return 'Edd_eddDetails__2PyAJ'

    def pharmeasy_composition(self):
        return 'MedicineMolecules_text__22hJW'

    def pharmeasy_price(self):
        return "PriceInfo_ourPrice__P1VR1"

    def pharmeasy_otc_price(self):
        return "ProductPriceContainer_mrp__pX-2Q"

    def pharmeasy_expiry(self):
        return "ProductDescription_tableValue__GBKiQ"

    def pharmeasy_mrp(self):
        return "PriceInfo_striked__1nHfC"

    def pharmeasy_product_name(self):
        return "MedicineOverviewSection_nameContainer__1sGfc"

    def pharmeasy_otc_product_name(self):
        return "OverviewSection_nameContainer__NK33_"

    def NetmedsUrl(self):
        return "https://www.netmeds.com/"

    def NetmedsSearchXpath(self):
        return'//*[@id="search"]'

    def NetmedsProductXpath(self):
        return '//*[@id="algolia_hits"]/li[1]/div/div/div[2]/a/div'

    def NetmedsPincodeXpath(self):
        return '//*[@id="pincode"]'

    def netmeds_product_name(self):
        return "product-detail"

    def netmeds_product_price(self):
        return "final-price"

    def netmeds_mrp(self):
        return "price"

    def netmeds_delivery(self):
        return "pin-expiry exp_del"

    def netmeds_expiry(self):
        return "pin-expiry expiry-date"

    def netmeds_composition(self):
        return "drug-manu"

    def OnemgUrl(self):
        onemg_url = "https://www.1mg.com/"
        return onemg_url

    def onemgProductPrice(self):
        return "style__price-tag___B2csA"

    def onemgSerachXpath(self):
        return '//*[@id="srchBarShwInfo"]'

    def ApolloUrl(self):
        apollo_url = ""
        return apollo_url

    def FlipkartHealthPlusUrl(self):
        flipkar_url = ""
        return flipkar_url

    def MedplusmartUrl(self):
        medplus_url = ""
        return medplus_url
