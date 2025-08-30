from selenium import webdriver
from selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class WikipediaScraper():
    driver: webdriver.Chrome
    BIO_CONTAINER_SELECTORS = [
        "table.infobox.biography.vcard", "table.infobox.vcard"]

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def find_bio_container_wrapper(self):
        for selector in self.BIO_CONTAINER_SELECTORS:
            try:
                return WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
        return None

    def find_bio_image_url(self, bio_container_wrapper):

        try:
            img = bio_container_wrapper.find_element(
                By.CSS_SELECTOR, "img"
            )
            return img.get_attribute("src")
        except Exception:
            return None
