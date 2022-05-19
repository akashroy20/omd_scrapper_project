from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from RepositoryForObject import ObjectRepository
import time


class Scrapper:

    def __init__(self, executable_path):
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path)
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initializing the webdriver object.\n" + str(e))

    def getLocatorObject(self):
        try:
            locators = ObjectRepository()
            return locators
        except Exception as e:
            raise Exception(f"(getLocatorObject) - Could not find locators.\n" + str(e))

    def findElementByXpath(self, xpath):
        if self.driver.find_elements_by_xpath(xpath=xpath):
            return self.driver.find_element_by_xpath(xpath)
        else:
            return "Try after sometime"

    def netmeds_pageSource(self, product, pincode):
        try:
            locator = self.getLocatorObject()
            self.driver.get(locator.NetmedsUrl())
            self.driver.implicitly_wait(10)
            search = self.findElementByXpath(locator.NetmedsSearchXpath())
            search.send_keys(product, Keys.ENTER)
            self.driver.implicitly_wait(10)
            product = self.findElementByXpath(locator.NetmedsProductXpath())
            product.click()
            self.driver.implicitly_wait(10)
            pincode_click = self.findElementByXpath(locator.NetmedsPincodeXpath())
            pincode_click.clear()
            pincode_click.send_keys(pincode, Keys.ENTER)
            time.sleep(2)
            page = self.driver.page_source
            page_soup = bs(page, 'html.parser')
            return page_soup

        except Exception as e:
            print(f"(netmeds_pageSource): Something went wrong while parsing data.\n" + str(e))
            page_soup = "Try after sometime for more option"
            return page_soup

    def netmeds_result(self, product, pincode):
        locator = self.getLocatorObject()
        r = self.netmeds_pageSource(product=product, pincode=pincode)
        if r != "Try after sometime for more option":
            product_page_source = r
            product_name = self.h1text(pname=locator.netmeds_product_name(),
                                       page_source=product_page_source)
            product_mrp = self.spanText(pname=locator.netmeds_mrp(),page_source=product_page_source)
            product_price =self.spanText(pname=locator.netmeds_product_price(), page_source=product_page_source).split()[-1]
            product_delivery = self.spanText(pname=locator.netmeds_delivery(),
                                             page_source=product_page_source)
            product_expiry = self.spanText(pname=locator.netmeds_expiry(), page_source=product_page_source)
            product_composition = self.adotText(pname=locator.netmeds_composition(),page_source=product_page_source)
            if product.lower() in product_name.lower():
                if product.lower() == product_name.lower():
                    search_status = "Exact match"
                else:
                    search_status = "Partial match, please check strength before ordering."
            else:
                search_status = "Not matched, please check strength before ordering."

        else:
            search_status = "Try after sometime for more option"
            product_name = "NA"
            product_composition = "NA"
            product_mrp = "NA"
            product_price = "NA"
            product_delivery = "NA"
            product_expiry = "NA"

        return {"Search status": search_status,
                "Product found": product_name,
                "Composition":product_composition,
                "MRP": product_mrp,
                "Best-price": product_price,
                "Estimated_delivery_time": product_delivery,
                "Expiry": product_expiry,
                "purchase link": self.currentPageUrl()}

    def pharmeasy_pageSource(self, product, pincode):
        try:
            locator = self.getLocatorObject()
            self.driver.get(locator.PharmeasyUrl())
            self.driver.implicitly_wait(10)
            search = self.findElementByXpath(locator.PharmeasySearchXpath())
            search.send_keys(product, Keys.ENTER)
            self.driver.implicitly_wait(10)
            product = self.findElementByXpath(locator.PharmeasyProductXpath())
            product.click()
            self.driver.implicitly_wait(10)
            address = self.findElementByXpath(locator.PharmeasyAddressXpath())
            address.click()
            self.driver.implicitly_wait(10)
            pincode_click = self.findElementByXpath(locator.PharmeasyPincodeXpath())
            pincode_click.send_keys(pincode, Keys.ENTER)
            time.sleep(2)
            page = self.driver.page_source
            page_soup = bs(page, 'html.parser')
            return page_soup


        except Exception as e:
            print(f"(pharmeasy_pageSource): Something went wrong while parsing data.\n" + str(e))
            page_soup = "Try after sometime for more option"
            return page_soup

    def pharmeasy_result(self, product, pincode):
        locator = self.getLocatorObject()
        r = self.pharmeasy_pageSource(product=product, pincode=pincode)
        if r != "Try after sometime for more option":
            product_page_source = r
            searched_name = product.split()[0].lower()
            if product_page_source.find_all("div", {"class": locator.pharmeasy_product_name()}):
                resulted_product_name = product_page_source.find_all("div",
                                                                     {"class": locator.pharmeasy_product_name()})
                resulted_product_name = resulted_product_name[0].h1.text.split()[0].lower()
                product_name = self.divText(pname=locator.pharmeasy_product_name(),
                                            page_source=product_page_source)
                product_mrp = self.spanText(pname=locator.pharmeasy_mrp(),page_source=product_page_source)
                product_price = self.divText(pname=locator.pharmeasy_price(), page_source=product_page_source)
                product_delivery = self.pharmeasy_delivery(d=locator.pharmeasy_delivery(),
                                                           page_source=product_page_source)
                product_composition = self.pharmeasyComposition(pname=locator.pharmeasy_composition(),
                                                                page_source=product_page_source)
                product_expiry = self.pharmeasy_expiry(e=locator.pharmeasy_expiry(),
                                                       page_source=product_page_source)
                if product.lower() in product_name.lower():
                    if product.lower() == product_name.lower():
                        search_status = "Exact match"
                    else:
                        search_status = "Partial match, please check strength before ordering."
                else:
                    search_status = "Not matched, please check strength before ordering."

            else:
                search_status = "OTC product!"
                product_name = self.h1text(pname=locator.pharmeasy_otc_product_name(),
                                           page_source=product_page_source)
                product_mrp = self.spanText(pname=locator.pharmeasy_mrp(),page_source=product_page_source)
                product_price = self.divText(pname=locator.pharmeasy_otc_price(), page_source=product_page_source)
                product_delivery = self.pharmeasy_delivery(d=locator.pharmeasy_delivery(),
                                                           page_source=product_page_source)
                product_composition = "Details not found"
                product_expiry = "Details not found"

        else:
            search_status = "Try after sometime for more option"
            product_name = "NA"
            product_composition = "NA"
            product_mrp = "NA"
            product_price = "NA"
            product_delivery = "NA"
            product_expiry = "NA"

        return {"Search status": search_status,
                "Product found": product_name,
                "Composition": product_composition,
                "MRP":product_mrp,
                "Best-price": product_price,
                "Estimated_delivery_time": product_delivery,
                "Expiry": product_expiry,
                "purchase link": self.currentPageUrl()}


    def h1text(self, pname, page_source):
        if page_source.find_all("div", {"class": pname}):
            obj = page_source.find_all("div", {"class": pname})
            Obj = obj[0].h1.text
        else:
            Obj = ["Details not found !!"]
        return Obj

    def spanText(self, pname, page_source):
        if page_source.find_all("span", {"class": pname}):
            obj = page_source.find_all("span", {"class": pname})
            Obj = obj[0].text
        else:
            Obj = ["Details not found !!"]
        return Obj

    def divText(self, pname, page_source):
        if page_source.find_all("div", {"class": pname}):
            obj = page_source.find_all("div", {"class": pname})
            Obj = obj[0].text
        else:
            Obj = "Details not found !!"
        return Obj

    def pharmeasyComposition(self, pname, page_source):
        if page_source.find_all("td", {"class": pname}):
            obj = page_source.find_all("td", {"class": pname})
            Obj = obj[3].text
        else:
            Obj = "Details not found !!"
        return Obj

    def adotText(self, pname, page_source):
        if page_source.find_all("div", {"class": pname}):
            obj = page_source.find_all("div", {"class": pname})
            Obj = obj[0].a.text
        else:
            Obj = "Details not found !!"
        return Obj

    def pharmeasy_delivery(self, d, page_source):
        if page_source.find_all("div", {"class": d}):
            delivery = page_source.find_all("div", {"class": d})
            delivery = delivery[0].span.text
        else:
            delivery = "Details not found !!"
        return delivery

    def pharmeasy_expiry(self, e, page_source):
        if page_source.find_all("div", {"class": e}):
            expiry = page_source.find_all("div", {"class": e})
            for i in range(len(expiry)):
                if bool(re.match("\d{2}", expiry[i].text)):
                    expiry_date = expiry[i].text
                else:
                    expiry_date = "Details not found !!"
        else:
            expiry_date = "Details not found !!"
        return expiry_date

    def currentPageUrl(self):
        current_url = self.driver.current_url
        return current_url
