from account_details import *
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


class CheckOutBot:
    def __init__(self):
        self.driver = webdriver.Chrome(PATH)
        self.driver.get("https://www.mediaexpert.pl/")
        self.accept_cookies()

    def accept_cookies(self):
        button = self.driver.find_element_by_css_selector("a[data-component='triggerClick']")
        self.driver.execute_script("arguments[0].click();", button)

    def login(self, email, password):
        self.driver.get("https://www.mediaexpert.pl/login")
        #time.sleep(5)
        email_input = self.driver.find_element_by_id("enp_customer_form_login_username")
        email_input.clear()
        email_input.send_keys(email)
        pass_input = self.driver.find_element_by_id("enp_customer_form_login_password")
        pass_input.clear()
        pass_input.send_keys(password)
        self.driver.find_element_by_css_selector("input[type='submit']").click()

    def add_product_to_chart(self, link):
        self.driver.get(link)
        #time.sleep(1)
        while True:
            try:
                add_to_cart_button = self.driver.find_element_by_css_selector("a[data-label='Do koszyka']")
                self.driver.execute_script("arguments[0].click();", add_to_cart_button)
                time.sleep(3)

                break

            except NoSuchElementException:
                self.driver.refresh()

    def checkout(self):
        act_url = self.driver.current_url
        print(act_url)
        self.driver.get("https://www.mediaexpert.pl/koszyk/lista")

        #time.sleep(1)
        payment_method = self.driver.find_element_by_css_selector("input[data-payment-name='Karta płatnicza przez Internet']")
        self.driver.execute_script("arguments[0].click();", payment_method)
        #time.sleep(2)
        save_payment = self.driver.find_element_by_css_selector("a[data-label='Dalej']")
        self.driver.execute_script("arguments[0].click();", save_payment)


        address = self.driver.find_element_by_css_selector("div[role='listbox']")
        self.driver.execute_script("arguments[0].click();", address)

        action = ActionChains(self.driver)
        address_box = self.driver.find_element_by_css_selector("div[data-id='1']")
        action.move_to_element(address_box).perform()
        action.click().perform()

        consent_Form = self.driver.find_element_by_css_selector("input[id='cart_flow_address_step_consentForm_consent_332']")
        self.driver.execute_script("arguments[0].click();", consent_Form)
        time.sleep(1)

        self.driver.find_element_by_css_selector("button[data-label='Dalej']").click()

        """
        #this is an instruction to confirm shopping and order. Uncomment it to perform payment
        order = self.driver.find_element_by_css_selector("a[data-label='Zamawiam i płacę']")
        self.driver.execute_script("arguments[0].click();", order)
        """

    def __del__(self):
        self.driver.close()


if __name__ == "__main__":
    checkout_bot = CheckOutBot()
    checkout_bot.login(email, password)
    checkout_bot.add_product_to_chart(link)
    checkout_bot.checkout()
    time.sleep(60)

