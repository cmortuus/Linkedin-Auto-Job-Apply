from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchWindowException

import re
import os
import time
emailPattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
experanceLevelPattern = re.compile("^[JjMmSsLl]")
driver = webdriver.Firefox()
data = {}
f = open('log', 'a+')
f.write('\n\n\n\n')


def getUserData():
    if not os.path.isfile('metadata'):
        f = open("metadata", "w+")
        email = input('What is the email associated with your Linkedin account?')
        while not emailPattern.match(email):
            email = input('That is not a valid email address')
        f.write(email + '\n')

        password = input(
            'What is the password you use to log into Linkedin. Note this is stored in the metadata file and not '
            'put anywhere else.\nFeel free to valadate that.')
        f.write(password + '\n')
        return open('metadata', 'r').readlines()
    else:
        return open('metadata', 'r').readlines()


def login():
    driver.get('https://www.linkedin.com/login')
    driver.find_element_by_id('username').clear()
    driver.find_element_by_id('username').send_keys(data[0][:-1])
    time.sleep(1)
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('password').send_keys(data[1][:-1])
    driver.find_element_by_class_name('btn__primary--large').click()


# TODO close other links
def recursiveApply(linkNum = 0):
    time.sleep(5)
    if linkNum != 10:
        # TODO get back to the jobs listing without going back to page 0
        # TODO allow for senior if there is junior as well
        # TODO this is the class for the title "fc-black-900"
        driver.get('https://www.linkedin.com/jobs/')
        # driver.find_element_by_class_name('test-pagination-next').click()
        site = driver.find_elements_by_class_name('job-card__link-wrapper')[linkNum + 5]
        try:
            site.click()
        except ElementClickInterceptedException:
            print('It failed to click on a new job link')
            f.write('It failed to click on a new job link\n')
            driver.get('https://www.linkedin.com/jobs/')
            recursiveApply(linkNum + 1)
        # jobInfo = driver.find_element_by_tag_name('body').text
        # moveOn = False
        #
        # # Things you want in every posting
        # for qualitiy in data[2].split(','):
        #     if qualitiy.replace(' ', '') in jobInfo:
        #         moveOn = True
        # # Things to avoid in a posting
        # for qualitiy in data[3].split(','):
        #     if qualitiy.replace(' ', '') in jobInfo:
        #         moveOn = False
        # if not moveOn:
        #     print('The listing did not contain the experience level preference of the user')
        #     f.write('The listing did not contain the experience level preference of the user')
        #     driver.get('https://www.linkedin.com/jobs/')
        #     recursiveApply(linkNum + 1)
        try:
            driver.find_element_by_xpath('xpath=//').click()
            driver.find_element_by_class_name('continue-btn').click()
            print('We applied to a job')
            f.write('We applied to a job')
            recursiveApply(linkNum + 1)
        except NoSuchElementException:
            print('It was not a proper form easy apply site')
            f.write('It was not a proper form easy apply site\n')
            time.sleep(1.123)
            recursiveApply(linkNum + 1)
    else:
        driver.get('https://www.linkedin.com/jobs/')
        recursiveApply(0)


data = getUserData()
login()
recursiveApply()