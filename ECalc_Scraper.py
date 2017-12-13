#Created by Kyle Wadell of Cornell Design/Build/Fly Project Team 2017
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time

def login(username,password):
    """
    Opens Ecalc Login Page
    Inputs the specified Username and Password
    Hits Enter
    """
    browser.get("http://www.ecalc.ch/calcmember/login.php?http://www.ecalc.ch/")
    user_box= browser.find_element_by_name('username')
    password_box=browser.find_element_by_name('password')
    user_box.send_keys(username)
    password_box.send_keys(password + Keys.RETURN)

    pass

def SetUp():
    """
    Navigates to Ecalc (including login)
    """
    login("designbuildfly@cornell.edu","TakeFlight")
    try:
    WebDriverWait(browser, 3).until(EC.alert_is_present())
    alert = browser.switch_to.alert
    alert.accept()
    print("alert accepted")
    except TimeoutException:
    print("no alert")

    browser.find_element_by_xpath('/html/body/center/table/tbody/tr/td[1]/div[3]/div/div[2]/center[1]/table/tbody/tr[1]/td[1]/a').click()

    pass

def full_scrape():
    """
    Iterate through all motors from all manufacturers, record data
    """
    man_drop=browser.find_element_by_id('inMManufacturer')
    mot_drop=browser.find_element_by_id('inMType')
    man_sel=Select(man_drop)
    mot_sel=Select(mot_drop)
    file = open('Motor_Data.txt','w')
    for option in man_drop.find_elements_by_tag_name('option'):
    if option.get_attribute('text')=='select...':
    pass
    pull_motors(option.get_attribute('text'),file)

def pull_motors(manuf,file):
    """
    Given a manufacturer, navigate through all listed motors,and record
    the motor data
    """
    man_drop=browser.find_element_by_id('inMManufacturer')
    mot_drop=browser.find_element_by_id('inMType')
    man_sel=Select(man_drop)
    mot_sel=Select(mot_drop)
    man_sel.select_by_visible_text(manuf)

    for option in mot_drop.find_elements_by_tag_name('option'):
    if option.get_attribute('text')[0] == '-':
    break

    Motor_Name = option.get_attribute('text')
    mot_sel.select_by_visible_text(Motor_Name)
    time.sleep(.5)
    if Motor_Name != 'custom':
    print(Motor_Name +"," + motor_dat())
    file.write(manuf+"," + Motor_Name +"," + motor_dat() + '\n')

    pass

def motor_dat():
    """
    While a motor is selected, output its displated parameters
    """
    Kv = browser.find_element_by_id('inMKv').get_attribute('value')
    No_Load_Current= browser.find_element_by_id('inMIo').get_attribute('value')
    N_L_V=browser.find_element_by_id('inMVIo').get_attribute('value')
    Limit_W=browser.find_element_by_id('inMLimit').get_attribute('value')
    Resist=browser.find_element_by_id('inMRi').get_attribute('value')
    Length_In=browser.find_element_by_id('inMLengthInch').get_attribute('value')
    Mag_Poles=browser.find_element_by_id('inMPoles').get_attribute('value')
    Weight_g=browser.find_element_by_id('inMWeight').get_attribute('value')

    return Kv + "," + No_Load_Current + "," + N_L_V + "," + Limit_W + "," + Resist + "," + Length_In+"," +
    Mag_Poles + "," + Weight_g
