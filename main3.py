from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Initialize Selenium WebDriver
driver = webdriver.Chrome()

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
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(5)  # Wait for the page to load
        #
        # new_height = driver.execute_script("return document.body.scrollHeight")
        # if new_height == last_height:
        #     break
        # last_height = new_height

        members = driver.find_elements(By.CLASS_NAME, 'xt0psk2')
        print(f"Members {members}")

        for member in members:
            try:
                name_element = member.find_element(By.XPATH, '//*[@id=":r2c:"]/span[1]/span/a')
                print(name_element)
                profile_link_element = member.find_element(By.XPATH, ".//a[@href]")

                member_name = name_element.text
                profile_url = profile_link_element.get_attribute('href')

                if (member_name, profile_url) not in members_list:  # Avoid duplicates
                    members_list.append((member_name, profile_url))
            except Exception as e:
                # Handle or log the exception if needed
                print(f"An error occurred: {e}")

    return members_list

def save_to_csv(members_list):
    df = pd.DataFrame(members_list, columns=['Member Name', 'Profile URL'])
    df.to_csv('members_list.csv', index=False)

if __name__ == "__main__":
    login_facebook()
    navigate_to_group()
    members_list = extract_members()
    save_to_csv(members_list)
    driver.quit()
