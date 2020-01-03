from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


import re
import time

emailPattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
experanceLevelPattern = re.compile("^[JjMmSsLl]")
driver = webdriver.Firefox()
data = {}

username = "mortoncf17@gcc.edu"
passwd = "1Xd$6dnQsVli$4WBR*az9S*we03#BzHglqYQGEVc$th4vi74^c^dNpa9k"

searchTerm = "automotive engineer"
searchArea = "Worldwide"


wordsToAvoid = ["senior", "mastors"]


def scrape():
    driver.get("https://www.linkedin.com/")
    driver.find_element_by_class_name("nav__button-secondary").click()

    uNameBar = driver.find_element_by_id("username")
    uNameBar.clear()
    uNameBar.send_keys(username)

    time.sleep(1.67)

    passwdBar = driver.find_element_by_id("password")
    passwdBar.clear()
    passwdBar.send_keys(passwd)

    time.sleep(1.67)

    passwdBar.submit()

    WebDriverWait(driver, 100).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "ember-view")))

    driver.get("https://www.linkedin.com/jobs")

    WebDriverWait(driver, 100).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "jobs-search-box__text-input")))

    searchBar = driver.find_element_by_class_name("jobs-search-box__text-input")

    searchBar.clear()
    searchBar.send_keys(searchTerm)

    searchBarArea = driver.find_element_by_xpath('//input[contains(@id, "jobs-search-box-location-id-ember")]')

    searchBarArea.clear()
    searchBarArea.send_keys(searchArea)

    driver.find_element_by_class_name("jobs-search-box__submit-button").click()

    time.sleep(4)

    options = driver.find_elements_by_class_name("search-s-facet__form")
    options[1].click()
    driver.find_element_by_xpath('//label[@for="f_LF-f_AL"]').click()

    jobList = driver.find_element_by_class_name("jobs-search-results__list").find_elements_by_tag_name("li")
    jobList[0].find_element_by_class_name('job-card-search__time-badge').click()
    time.sleep(5)
    jobList = driver.find_element_by_class_name("jobs-search-results__list").find_elements_by_tag_name("li")

    for job in jobList:
        try:
            WebDriverWait(driver, 100).until(
                expected_conditions.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button")))
            job.find_element_by_class_name("jobs-apply-button").click()
            for word in wordsToAvoid:
                if word not in driver.find_element_by_id("job-details").text: break
            print("This is a valid job to apply to")
        except ElementClickInterceptedException as e:
            print(e)
        except NoSuchElementException as e:
            print(e)


scrape()
