from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from re import sub
from decimal import Decimal
import warnings

class Data_Extraction:
    chrome_driver_path = "chromedriver.exe"
    URL = "https://www.flipkart.com/"
    warnings.filterwarnings("ignore")

    def  __init__(self):
        self.browser_option = webdriver.ChromeOptions()
        # self.browser_option.add_argument("headless")
        self.driver = webdriver.Chrome(executable_path= Data_Extraction.chrome_driver_path, options= self.browser_option)
        self.driver.set_window_size(720, 480)
        # self.driver.maximize_window()
        self.driver.get(Data_Extraction.URL)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class = '_2KpZ6l _2doB4z']")))
        self.driver.find_element(By.CSS_SELECTOR, "button[class = '_2KpZ6l _2doB4z']").click()
    

    def get_data_2(self, general_products, page_count):
        self.driver.find_element(By.CSS_SELECTOR, "img[title= 'Flipkart']").click()
        # data_list = []
        # for product in general_products:
        self.driver.find_element(By.CSS_SELECTOR, "input[type = 'text']").send_keys(general_products)
        self.driver.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()

        self.products_info = [["Product", "Price", "Rating(stars)", "Warranty"]]

        wait = WebDriverWait(self.driver, 6)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_1YokD2 _3Mn1Gg']/div/div/div/div")))

        for i in range(page_count):
            self.items = self.driver.find_elements(By.XPATH, "//div[@class='_1YokD2 _3Mn1Gg']/div/div/div/div")
            for i in range(2, len(self.items)):
                self.items[i].click()
                self.parent = self.driver.window_handles[0]
                self.child = self.driver.window_handles[1]
                self.driver.switch_to.window(self.child)
                self.products_info += self.gather_info()
                self.driver.close()
                self.driver.switch_to.window(self.parent)
            self.driver.find_element(By.XPATH, "//span[text() = 'Next']").click()
            sleep(1)
            print(i+1, "Page scanned")

        
        # print(self.products_info)
        return self.products_info


    def gather_info(self):
        self.name = self.driver.find_element(By.XPATH, "//div[@class= 'aMaAEs']/div[1]/h1/span[@class= 'B_NuCI']").text
        self.price = self.driver.find_element(By.XPATH, "//div[@class = 'CEmiEU']/div/div[1]").text
        self.value = Decimal(sub(r'[^\d.]', '', self.price))
        try:
            self.rating = float(self.driver.find_element(By.XPATH, "//div[@class = '_3_L3jD']/div/span[1]/div").text)
        except Exception as e:
            self.rating = float(0.00)
        
        try:
            self.warranty = self.driver.find_element(By.XPATH, "//div[@class = '_1UdlE-']/div[2]/div").text
        except Exception as e:
            self.warranty = "Not Applicable"

        return [[self.name, self.value, self.rating, self.warranty]]

    def get_data(self, general_products, page_count):
        self.driver.find_element(By.CSS_SELECTOR, "img[title= 'Flipkart']").click()
        self.driver.find_element(By.CSS_SELECTOR, "input[type = 'text']").send_keys(general_products)
        self.driver.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()

        self.layout = ""
        
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class ='_3pLy-c row']/div[1]/div[1]")))
            self.driver.find_element(By.XPATH, "//div[@class ='_3pLy-c row']/div[1]/div[1]").text
            self.layout = "list"
        except Exception as e:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_1YokD2 _3Mn1Gg']/div/div/div/div/a[2]")))
            self.layout = "grid"



        products_info = []
        if self.layout == "list":
            products_info = [["product", "price", "memory", "display", "camera", "battery", "processor"]]
            for i in range(page_count):
                products_info += self.list_layout()
                self.driver.find_element(By.XPATH, "//span[text() = 'Next']").click()
                sleep(3)
                print(i+1, "Page scanned")
        elif self.layout == "grid":
            products_info = [["product", "price"]]
            for i in range(page_count):
                products_info += self.grid_layout()
                self.driver.find_element(By.XPATH, "//span[text() = 'Next']").click()
                sleep(3)
                print(i+1, "Page scanned")
        else:
            products_info = ["unable to locate page"]


        return products_info

    def new_page_data(self):
        self.names = self.driver.find_elements(By.XPATH, "//div[@class='_2B099V']/a[1]")
        self.prices = self.driver.find_elements(By.XPATH, "//div[@class='_2B099V']/a[2]/div[1]/div[1]")
        for i in range(len(self.names)):
            value = Decimal(sub(r'[^\d.]', '', self.prices[i].text))
            self.data.append([self.names[i].text, value])
        
        return self.data



    def list_layout(self):
        self.data = []
        self.wait = WebDriverWait(self.driver, 10)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_3pLy-c row']/div[1]/div[1]")))
        self.names = self.driver.find_elements(By.XPATH, "//div[@class='_3pLy-c row']/div[1]/div[1]")
        self.prices = self.driver.find_elements(By.XPATH, "//div[@class='_3pLy-c row']/div[2]/div[1]/div[1]/div[1]")
        self.memory = self.driver.find_elements(By.XPATH, "//div[@class='_3pLy-c row']/div[1]/div[3]/ul/li[1]")
        self.display = self.driver.find_elements(By.XPATH, "//div[@class='_3pLy-c row']/div[1]/div[3]/ul/li[2]")
        self.camera = self.driver.find_elements(By.XPATH, "//div[@class='_3pLy-c row']/div[1]/div[3]/ul/li[3]")
        self.battery = self.driver.find_elements(By.XPATH, "//div[@class='_3pLy-c row']/div[1]/div[3]/ul/li[4]")
        self.processor = self.driver.find_elements(By.XPATH, "//div[@class='_3pLy-c row']/div[1]/div[3]/ul/li[5]")

        for i in range(len(self.names)):
            # print(self.prices[i].text, i+1)
            value = Decimal(sub(r'[^\d.]', '', self.prices[i].text))
            self.data.append([self.names[i].text, value, self.memory[i].text, self.display[i].text, self.camera[i].text, self.battery[i].text, self.processor[i].text])

        return self.data
    
    def grid_layout(self):
        self.data = []
        self.wait = WebDriverWait(self.driver, 10)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_1YokD2 _3Mn1Gg']/div/div/div/div/a[2]")))
        self.names = self.driver.find_elements(By.XPATH, "//div[@class='_1YokD2 _3Mn1Gg']/div/div/div/div/a[2]")
        self.prices = self.driver.find_elements(By.XPATH, "//div[@class='_1YokD2 _3Mn1Gg']/div/div/div/div/a[3]/div[1]/div[1]")
        for i in range(len(self.names)):
            value = Decimal(sub(r'[^\d.]', '', self.prices[i].text))
            self.data.append([self.names[i].text, value])
        
        return self.data
    
    def close_browser(self):
        self.driver.close()