from behave import given, when, then
from flask import current_app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import shelve
import os

directoryName = os.path.dirname('sessions.db')
pathToSessionsDir = os.path.abspath(directoryName)
file = shelve.open(f"{pathToSessionsDir}/sessions")


@given("I opened the game in my browser")
def step_impl(context):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-setuid-sandbox")
    chromeOptions.add_argument('--profile-directory=Default')

    chromeOptions.add_argument("--remote-debugging-port=9222")
    chromeOptions.add_argument("--disable-dev-shm-using")
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument("--disable-gpu")
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("disable-infobars")
    # context.driver = webdriver.Remote(command_executor='http://172.17.0.2:4444/wd/hub', options=chromeOptions)
    #context.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    context.driver = webdriver.Remote(command_executor='http://172.17.0.2:4444/wd/hub', options=chromeOptions)
    context.driver.set_window_size(1920, 1080, context.driver.window_handles[0])
    context.action_chains = ActionChains(context.driver)

    context.driver.get("http://172.17.0.1:5000")
    time.sleep(1)


@when('I start a game in mode {mode}')
def step_menu(context, mode):
    new_game_button = context.driver.find_element(
        By.ID, "newGame"
    )
    new_game_button.click()
    time.sleep(1)
    mode_button = context.driver.find_element(
        By.ID, mode
    )
    mode_button.click()
    time.sleep(2)


@when('p click on a position ({col},{row})')
def step_impl(context, col, row):
    square = context.driver.find_element(
        By.CSS_SELECTOR, f"#col{col}-row{row}")

    square.click()
    time.sleep(2)


@when('I wait for {seconds} seconds')
def step_impl(context, seconds):
    time.sleep(int(seconds))


@then('compare if the output is correct')
def step_impl(context):
    session_num = context.driver.find_element(By.ID, f"sessionNum").get_attribute("value")
    # print(file)
    board = file[f"session{session_num}"].board
    for i in range(len(board)):
        for e in range(len(board[i])):
            if board[i][e] != ' ':
                if board[i][e] == 'p1':
                    assert context.driver.find_element(By.CSS_SELECTOR,
                                                       f"#col{str(i)}-row{str(e)}").value_of_css_property(
                        "Background-Color") == "rgb(216, 17, 89)"
                elif board[i][e] == 'p2':
                    assert context.driver.find_element(By.CSS_SELECTOR,
                                                       f"#col{str(i)}-row{str(e)}").value_of_css_property(
                        "Background-Color") == "rgb(255, 188, 66)"
    time.sleep(3)
