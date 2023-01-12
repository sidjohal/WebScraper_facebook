from creds import email, password, page_url
page_url  = page_url.rstrip("/")
if email.strip()=="":
    print("Enter an email in creds.py")
    s = input("Press any key to quit")
    quit()

if password.strip()=="":
    print("Enter the password in creds.py")
    s = input("Press any key to quit")
    quit()

if page_url.strip()=="":
    print("Enter a page url in creds.py")
    s = input("Press any key to quit")
    quit()

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import sys, time, os, wget
path = os.getcwd()

start = time.time()

# to disable the notifications
option = Options()
option.add_argument('--disable-notifications')

# open page
driver = webdriver.Chrome(path+"/chromedriver", chrome_options= option)
driver.maximize_window()
driver.get("https://facebook.com")

# create login crediantials
uname = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
pword = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

# enter login details
uname.clear()
pword.clear()
uname.send_keys(email)
pword.send_keys(password)

# log in
log_in = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
log_in.click()

#wait 5 seconds to allow your new page to load
time.sleep(5)

# redirect to photos the page 
driver.get(page_url+"/photos")
time.sleep(5)

#increase i to sroll more
i = 10
for j in range(0,i):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

# create list of the post URLs
post_urls = driver.find_elements(By.TAG_NAME, 'a')
post_urls = [a.get_attribute('href') for a in post_urls]
post_urls = [a for a in post_urls if str(a).startswith("https://www.facebook.com/photo")]

print('Found ' + str(len(post_urls)) + ' links to images')

images = []

# iterate through every post's page and get URL to image
for a in post_urls:
    driver.get(a) 
    time.sleep(5)
    temp = driver.find_elements(By.TAG_NAME, 'img')
    temp = [a.get_attribute('src') for a in temp][0]
    images.append(temp)

print('Scraped '+ str(len(images)) + ' images')

# create the directory to save the dataframe table
path = os.getcwd()
save = os.path.join(path, "FB_SCRAPED")

try:
    os.mkdir(save)
except:
    pass

# save csv
df = pd.DataFrame(list(zip(post_urls,images)),
             columns=["Page URL",'Image links']).to_csv(path+"/images.csv", index=False)

time = time.time() - start
if time<60:
    print("Time taken to scrape", len(post_urls), "images data =", time, "sec")
else:
    print("Time taken to scrape", len(post_urls), "images data =", round(time/60,2), "min")


s = input("Press any key to quit")
