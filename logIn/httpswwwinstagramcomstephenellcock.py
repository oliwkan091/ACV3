"""
Skrypt ten odpowiada za proces logowania się do instagrama i jest wywoływany przez prgoram główny
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def logIn(driver,pageLink):

    # Dane do zalogowania
    nanmeUsername = "username"
    namePassword = "password"
    cookieCssSelector = ".aOOlW:last-of-type"
    loginCssSelector = ".y3zKF:not(.yWX7d), a.y3zKF:not(.yWX7d), a.y3zKF:not(.yWX7d):visited"
    username = "LoginNiezbednyDoOffice123@gmail.com"
    password = "fg4tgasj578hw4t"

    driver.get(pageLink)
    time.sleep(5)
    # Niezbędne do wczytania wszystkich skryptów Java Script
    driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

    #Potwierdza cookies
    driver.find_element_by_css_selector(cookieCssSelector).click()
    time.sleep(5)

    driver.find_element_by_name(nanmeUsername).send_keys(username) 
    driver.find_element_by_name(namePassword).send_keys(password)
    driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

    driver.find_element_by_css_selector(loginCssSelector).click()
    time.sleep(5)

    # Zwraca pobraną stronę po zalogowaniu
    return driver


if __name__ == "__main__":
    
    print("Tego skryptu nie można włączyć z main")