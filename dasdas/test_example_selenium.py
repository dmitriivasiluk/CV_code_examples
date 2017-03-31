# -*- coding: utf-8 -*-
""" Tests on Selenium WebDriver of school CRUD """

import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select


class SchoolCRUDTests(unittest.TestCase):
    """ Class with methods, for testing School CRUD """

    baseurl = "https://commercial-secret.com"
    username = "johndoe"
    password = "1111"
    warnings = {
        'incorrectName': u"Некоректно введено назву.",
        'incorrectAddress': u"Некоректно введено адресу.",
        'alreadyExistsName': u"Школа з такою назвою вже існує."
    }
    xpaths = {
        'inputUsername': "//input[@name='inputUsername']",
        'inputPassword': "//input[@name='inputPassword']",
        'submitButtonLogin': "button",
        'inputSchoolName': "//*[@id='inputSchoolName']",
        'inputSchoolAddress': "//*[@id='inputNumber']",
        'confirmAddEditButton': "//*[@id='add_button']",
        'buttonEditSchool': "//*[@id='5']/td[4]/a[1]",
        'selectionOfDiretor': "//select[@name='director']",
        'buttonDeleteSchool': "//*[@id='100']/td[4]/a[2]"

    }
    credentials = {
        'correctAddress': u'вул. Євгена Коновальця, 19',
        'correctName': u'Школа №28',
        'correctNameForRetest': u'Школа №80',
        'nameRoman': 'School #28',
        'addressRoman': 'Verbova Street, 35',
        'cyrrilicAddressWrong': u'Адреса 200',
        'cyrrilicNameWrong': u'Школа 100',
        'correctAddressForEdit': u'вул. Мельника, 67',
        'correctNameForEdit': u'Школа №25',
        'nameStartingLower': u'нвк "веселка"',
        'addressStartingUpper': u'ВУЛ. Макарова, 19',
        'schoolToDelete': u'вул. Тестова, 1'
    }

    def credetials_to_add_school(self, driver, school_name, address):
        """ Function to automate proccess of inserting the credentials """

        driver.find_element_by_link_text(u'+ Додати').click()
        driver.find_element_by_xpath(
            self.xpaths['inputSchoolName']).send_keys(
            school_name)
        driver.find_element_by_xpath(
            self.xpaths['inputSchoolAddress']).send_keys(
            address)

        driver.find_element_by_xpath(
            self.xpaths['confirmAddEditButton']).click()

    def credetials_to_edit_school(self,
                                  driver,
                                  school_name,
                                  address,
                                  xpath_of_school_to_edit,
                                  xpath_of_director):
        """ Function to automate proccess of inserting the credentials """

        driver.find_element_by_xpath(xpath_of_school_to_edit).click()
        input_name_area = driver.find_element_by_xpath(
            self.xpaths['inputSchoolName'])
        input_address_area = driver.find_element_by_xpath(
            self.xpaths['inputSchoolAddress'])
        input_name_area.clear()
        input_name_area.send_keys(school_name)
        input_address_area.clear()
        input_address_area.send_keys(address)

        driver.find_element_by_xpath(
            xpath_of_director).click()

        select = Select(driver.find_element_by_xpath(xpath_of_director))

        select.select_by_value('12')
        driver.find_element_by_xpath(
            self.xpaths['confirmAddEditButton']).click()

    def _check_for_element_existence(self, driver, warning):
        """ Function to check whether element exists on the web-page """

        self.page_content = driver.page_source
        if warning in self.page_content:
            warning_exists = True
        else:
            warning_exists = False

        return warning_exists

    def setUp(self):
        """ Fixture that creates all the preparations for tests """

        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.accept_next_alert = True
        self.driver.get(self.baseurl)
        self.driver.find_element_by_xpath(
            self.xpaths['inputUsername']).send_keys(
            self.username)

        self.driver.find_element_by_xpath(
            self.xpaths['inputPassword']).send_keys(
            self.password)

        self.driver.find_element_by_tag_name(
            self.xpaths['submitButtonLogin']).click()

    def tearDown(self):
        """ Fixture that deletes all the preparations for tests """

        self.driver.close()

    def test01_ui_to_add_schools_exists(self):
        """ Test to check whether windows to add school exists """

        self.driver.find_element_by_link_text(u'+ Додати').click()
        self.element = self.driver.find_element_by_tag_name('h3')

        self.assertEquals(u"Додати школу", self.element.text)

    def test02_cancel_button(self):
        """
        Fields to enter credentials should be empty after cancel and retry
        """

        link = self.driver.find_element_by_link_text(u'+ Додати')
        link.click()
        self.driver.find_element_by_xpath(
            self.xpaths['inputSchoolName']).send_keys(
            self.credentials['correctName'])
        self.driver.find_element_by_xpath(
            self.xpaths['inputSchoolAddress']).send_keys(
            self.credentials['correctAddress'])
        link2 = self.driver.find_element_by_link_text('x')
        link2.click()
        link.click()
        name_value = self.driver.find_element_by_xpath(self.xpaths[
                                                           'inputSchoolName'])
        address_value = self.driver.find_element_by_xpath(
            self.xpaths['inputSchoolAddress'])

        self.assertTrue(("" == name_value.get_attribute('value')) and
                        ("" == address_value.get_attribute('value')))

    def test03_add_school_with_correct_credentials_positive(self):
        """ New school should be added with correct credentials """

        self.credetials_to_add_school(self.driver,
                                      self.credentials['correctName'],
                                      self.credentials[
                                           'correctAddress'])
        self.driver.refresh()
        self.assertEqual(
            self._check_for_element_existence(
                self.driver, self.credentials['correctName']), True)

    def test04_add_school_with_roman_name_negative(self):
        """ Expected warning about incorrect name """

        self.credetials_to_add_school(self.driver,
                                      self.credentials['nameRoman'],
                                      self.credentials[
                                           'correctAddress'])

        self.assertEqual(
            self._check_for_element_existence(
                self.driver, self.warnings['incorrectName']), True)

    def test05_add_school_with_roman_address_negative(self):
        """ Expected warning about incorrect address """

        self.credetials_to_add_school(self.driver,
                                       "",
                                      self.credentials[
                                           'addressRoman'])
        self.assertEqual(
            self._check_for_element_existence(
                self.driver, self.warnings['incorrectAddress']), True)

    def test06_add_school_with_empty_name_negative(self):
        """ Expected warning about incorrect name """

        self.credetials_to_add_school(self.driver, "",
                                      self.credentials[
                                           'correctAddress'])
        self.assertEqual(
            self._check_for_element_existence(
                self.driver, self.warnings['incorrectName']), True)


if __name__ == "__main__":
    unittest.main(verbosity=2)

