import os

from selenium import webdriver
import yaml


cur_dir = os.path.dirname(os.path.realpath(__file__))
secret_path = os.path.join(cur_dir, 'secrets.yml')

with open(secret_path, 'r') as stream:
    data = yaml.load(stream)
    FIRST_NAME = data.get('first_name', '')
    LAST_NAME = data.get('last_name', '')
    FULL_NAME = FIRST_NAME + LAST_NAME
    ADDRESS = data.get('address', '')
    CITY = data.get('city', '')
    STATE = data.get('state', '')
    ZIP = data.get('zip', '')
    EMAIL = data.get('email', '')
    PHONE = data.get('phone', '')
    CARD_NO = data.get('44444444', '')


driver = webdriver.Firefox()


def select_in_dropdown(select, key):
    for option in select.find_elements_by_tag_name('option'):
        if option.get_attribute('value') == key:
            option.click()
            return


def accept_terms():
    driver.get('https://www.cityofmadison.com'
               '/epayment/metro/busPass/index.cfm')
    checkbox = driver.find_element_by_id('acceptTerms')
    checkbox.click()
    submit = driver.find_element_by_id('submit')
    submit.click()


def fill_out_quantity():
    quantity_text = driver.find_element_by_id('product_62')
    quantity_text.send_keys('1')


def fill_out_contact_info():
    fields = {'name': FULL_NAME,
              'Address': ADDRESS,
              'City': CITY,
              'State': STATE,
              'Zip': ZIP,
              'email': EMAIL}

    for name, value in fields.items():
        if name == 'State':
            elem = driver.find_element_by_name(name)
            select_in_dropdown(elem, STATE)
        else:
            driver.find_element_by_name(name).send_keys(value)

    driver.find_element_by_name('notice').click()  # same as billing address...
    driver.find_element_by_id('submit').click()


def proceed_to_payment():       # TODO: Validate payment information
    driver.find_element_by_id('paymentProcessing').submit()


def fill_out_payment_info():
    fields = {'firstName': FIRST_NAME,
              'lastName': LAST_NAME,
              'address.street1': ADDRESS,
              'address.city': CITY,
              'address.state': STATE,
              'address.zip5': ZIP,
              'phone': PHONE,
              'email': EMAIL}

    for name, value in fields.items():
        if name == 'address.state':
            elem = driver.find_element_by_name('contactInformation.{}'
                                               .format(name))
            select_in_dropdown(elem, STATE)
        else:
            driver.find_element_by_id('contactInformation.{}'.format(name)) \
                  .send_keys(value)


def select_payment_method():
    elem = driver.find_element_by_id('paymentMethodRef')
    select_in_dropdown(elem, '2')  # TODO: Validate option


def fill_out_card_info():
    elem = driver.find_element_by_id('creditCardPaymMethod.creditCardNumber')
    elem.send_keys(CARD_NO)


if __name__ == '__main__':
    accept_terms()
    fill_out_quantity()
    fill_out_contact_info()
    proceed_to_payment()
    fill_out_payment_info()
    select_payment_method()
    fill_out_card_info()
