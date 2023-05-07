import os
import time
import requests
from bs4 import BeautifulSoup

# scrape all images and title from this website https://www.etsy.com/market/moroccan_carpet?ref=pagination&page=1 with the pagination and save them in a folder called "data" in the same directory

# 1. get the html of the website
# 2. parse the html to get the images and title
# 3. save the images and title in a folder called "data"

# 1. get the html of the website
j = 0
for i in range(1, 10):
    url = f"https://www.etsy.com/search?q=moroccan+carpet&ref=pagination&page={i}"
    print(f"Scraping page {i}")
    response = requests.get(url)
    html = response.text

    # 2. parse the html to get the images and title
    soup = BeautifulSoup(html, "html.parser")

    # get all the images
    images = soup.find_all("img", class_="wt-width-full", alt=True)

    # 3. save the images and title in a folder called "data"

    os.makedirs("data", exist_ok=True)

    for image in images:
        # save the images
        print(image["alt"])
        image_url = image["src"]
        image_response = requests.get(image_url)
        try:
            with open(f"data/{j}.jpg", "wb") as f:
                f.write(image_response.content)
            with open("data/descriptions.txt", "a") as f:
                f.write(f"\'{image['alt']}\',\n")
            with open("data/link.txt", "a") as f:
                f.write(f"'{image_url}',\n")
        except:
            print(f"Could not save {j}")
        j += 1
        time.sleep(1)
    print(f"Done with page {i}")
