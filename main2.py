from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd

# Initialize Selenium WebDriver

driver = webdriver.Chrome()

# Facebook login credentials
# Facebook login credentials
username = '@gmail.com'
password = ''
group_url = 'https://www.facebook.com/groups/sdkians/members'


def login_facebook():
    driver.get('https://www.facebook.com/')
    time.sleep(2)

    # Log in to Facebook
    email_input = driver.find_element(By.ID, 'email')
    email_input.send_keys(username)
    password_input = driver.find_element(By.ID, 'pass')
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)


def navigate_to_group():
    driver.get(group_url)
    time.sleep(5)


def extract_members():
    members_list = []

    # Scroll to load all members
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Wait for the page to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Assuming members' names are in 'span' tags within a specific class
        members = soup.find_all('span', {'class': 'fwb'})
        for member in members:
            member_name = member.text
            if member_name not in members_list:  # Avoid duplicates
                members_list.append(member_name)

    return members_list


def save_to_csv(members_list):
    df = pd.DataFrame(members_list, columns=['Member Name'])
    df.to_csv('members_list.csv', index=False)


if __name__ == "__main__":
    login_facebook()
    navigate_to_group()
    members_list = extract_members()
    save_to_csv(members_list)
    driver.quit()
