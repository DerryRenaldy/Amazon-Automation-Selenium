import time
import csv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

arr = list()

class AmazonAutomation:
    def searching(self):

        url = "https://www.amazon.com/s?k="

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)
        driver.implicitly_wait(5)
        assert "Amazon" in driver.title
        driver.set_page_load_timeout(60)

        try:
            # Selecting Button
            select_sidebar_menu = driver.find_element(By.ID, 'nav-hamburger-menu')
            select_sidebar_menu.click()
            # 2. select for products by department “electronics”
            time.sleep(1)
            select_cat_elec = driver.find_element(By.XPATH, '//div[contains(text(),"Electronics")]')
            select_cat_elec.click()
            # 3. “television & video” Categories
            time.sleep(2)
            select_cat_tel = driver.find_element(By.LINK_TEXT, "Television & Video")
            select_cat_tel.click()
            # 4. Select the “televisions”
            time.sleep(1)
            select_tel = driver.find_element(By.XPATH, '(//a[@class="a-link-normal s-navigation-item"])[13]')
            select_tel.click()
            # 5. Select “32 inches & under” from left side refinery
            time.sleep(1)
            select_tel_size = driver.find_element(By.XPATH, '//span[contains(text(),"32 Inches & Under")]')
            select_tel_size.click()
            # 6. Sort the items by price descending
            # Select by visible text
            time.sleep(1)
            select_sort = Select(driver.find_element(By.ID, 's-result-sort-select'))
            select_sort.select_by_index(2)

            # ==================================================================
            # ==================== LOOPING PRODUCT FUNCTION ====================
            # ==================================================================
            def looping_product(n):
                # ==================== START FOR LOOP ====================
                for i in range(1, n + 1, 1):
                    # ========== TITLE ==========
                    try:
                        time.sleep(1)
                        xPathTitle = '(//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"])[{}]'.format(
                            i)
                        driver.find_element(By.XPATH, xPathTitle).click()
                    except NoSuchElementException:
                        break

                    title = driver.find_element(By.XPATH, '//span[@id="productTitle"]').text
                    title = title.strip('0 1 2 3 4 5 6 7 8 9 \"')[0:title.index(" ")]

                    # ========== PRICE ==========
                    time.sleep(1)
                    try:
                        # exist
                        price = driver.find_element(By.XPATH, '(//span[@class="a-price-whole"])[1]')
                        priceText = price.text
                        time.sleep(1)
                    except NoSuchElementException:
                        try:
                            idUnavaliable = 'outOfStock'
                            driver.find_element(By.ID, idUnavaliable)

                            priceText = driver.find_element(By.XPATH, '//span[@class="a-color-price a-text-bold"]').text
                        except NoSuchElementException:
                            priceText = 'No Prices Avaliable'

                    driver.back()
                    arr.append([title, priceText])
                # ==================== END FOR LOOP ====================

            # ==============================================================
            # ==================== CREATE LIST FUNCTION ====================
            # ==============================================================
            def create_list(items):
                # ========== CALLING LOOPING PRODUCT FUNCTION ==========
                looping_product(items)

                driver.find_element(By.XPATH, '(//a[@class="a-link-normal s-navigation-item"])[29]').click()
                time.sleep(1)
                driver.find_element(By.ID, 'high-price').send_keys(150)
                driver.find_element(By.XPATH, '//input[@class="a-button-input"]').click()

                # ========== CALLING LOOPING PRODUCT FUNCTION ==========
                looping_product(items)

            # ==================== CALLING CREATE LIST FUNCTION ====================
            time.sleep(1)
            create_list(15)

            # ==================== SELECTING FIRST PRODUCT IN SEARCH RESULT ====================
            time.sleep(1)
            xPathTitle = '(//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"])[1]'
            xPathH1Login = '//h1[normalize-space()="Sign in"]'
            xPathInputEmailLogin = 'ap_email'
            xPathButtonSubmitLogin = '//input[@id="continue"]'
            nameAddTooList = 'submit.add-to-registry.wishlist.unrecognized'
            classNameError = 'a-alert-heading'

            driver.find_element(By.XPATH, xPathTitle).click()
            driver.find_element(By.NAME, nameAddTooList).click()

            # ========== VERIFYING SIGN IN ==========
            time.sleep(2)
            assert "Sign in" in driver.find_element(By.XPATH, xPathH1Login).text
            driver.find_element(By.ID, xPathInputEmailLogin).send_keys('testeremail1@gmail.com')
            driver.find_element(By.XPATH, xPathButtonSubmitLogin).click()

            # ========== VERIFYING ERROR ==========
            time.sleep(2)
            assert "There was a problem" in driver.find_element(By.CLASS_NAME, classNameError).text

            # ========== PRINT OUTPUT ==========
            panjangArray = str(len(arr))
            print("Array dengan panjang " + panjangArray + ": " + str(arr))
            time.sleep(10)

            #  ========== CLOSING BROWSER ==========
            driver.close()

        # ========== ERROR HANDLING ==========
        except Exception as e:
            print("Exception", e)
            print('SERVER DID NOT RESPONSE...')


# ========== RUNNING MAIN FUNCTION ==========
fetcher = AmazonAutomation()
fetcher.searching()

f = open('result.csv', 'a', newline='', encoding='utf-8')
writer = csv.writer(f)
for article in arr:
    writer.writerow(article)

