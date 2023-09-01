import os
import random as r
import regex as re
from time import sleep
import requests
import shutil

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def random_user_agent():
    agents = open("agents.txt", "r")
    agent = r.choice(agents.readlines())
    agents.close()
    return agent

def get_book_data(url):

    driver.get(url)
    driver.refresh()
    sleep(3)
    wrapper = driver.find_element(By.CLASS_NAME, "bookinfo_sectionwrap")
    info = wrapper.find_elements(By.TAG_NAME, "div")
    author = info[0].find_element(By.TAG_NAME, "span").text
    title = info[1].find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME,"span").text
    page_count = info[1].find_elements(By.TAG_NAME, "span")[2].text

    return author+":"+title+":"+page_count.split(" ")[0]

def find_button():
	for i in driver.find_elements(By.TAG_NAME, "div"):
		if i.get_attribute("style") == 'position: absolute; cursor: pointer; background-image: url("https://www.google.com/googlebooks/images/right_btn.png"); background-position: left top; background-repeat: no-repeat; background-color: transparent; border-width: 0px; border-style: none; border-color: currentcolor; color: rgb(0, 0, 0); font-family: Arial, sans-serif; font-size: 13.28px; font-weight: normal; line-height: 1; margin: 0px; padding: 0px; text-align: left; text-decoration: none; vertical-align: middle; left: 1230px; top: 6px; width: 22px; height: 22px;':
			return i


url = input("googlebooks url: ")
id_part = re.findall(r"id=[A-Za-z0-9]+", url)[-1]

options = webdriver.FirefoxOptions().set_preference("general.useragent.override", random_user_agent())
#options.headless = True
driver = webdriver.Firefox(options=options)

page_url = str("https://books.google.com/books?"+id_part+"&pg=1&hl=en&f=false&output=embed&source=gbs_embed")

data = get_book_data(url).split(":")

driver.get(page_url)
driver.refresh()
sleep(2)
important = driver.find_element(By.CLASS_NAME, "scroll-background")
button = find_button()

srcs = []
ite = 0
imgs = []

while True:
	imgs = important.find_elements(By.TAG_NAME, "img")
	for i in imgs:
		bing = i.get_attribute("src")
		if bing not in srcs:
			srcs.append(bing)
	ite+=1
	if ite == len(srcs):break

	button.click()
	sleep(.2)

print("Finished finding links")
driver.close()

try:
	os.mkdir("./"+data[1])
except FileExistsError:
	pass
os.chdir("./"+data[1])

images = open("images.txt", "w+")
ite = 0

for src in srcs:#issue here
	ite+=1
	images.write(src+"\n")
	try:
		with open(str(ite)+".png", "wb+") as f:
			f.write(requests.get(src).content)
	except Exception as e:
		print(e)

images.close()
