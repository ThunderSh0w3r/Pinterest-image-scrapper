import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time

def download_image(image_url, save_dir):
    try:
        response = requests.get(image_url)  # Correct way to get content
        response.raise_for_status()  # Raise an error for bad responses
        
        # Get the image name from the URL
        image_name = os.path.basename(urlparse(image_url).path)
        # Create the save path
        save_path = os.path.join(save_dir, image_name)

        # Save the image to the specified directory
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Could not download {image_url}: {e}")

def find_external_images(webpage_url, save_dir):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    driver.get(webpage_url)
    time.sleep(5)  # Wait for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    os.makedirs(save_dir, exist_ok=True)
    img_tags = soup.find_all('img')

    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            img_url = urljoin(webpage_url, img_url)
            print(f"Checking URL: {img_url}")
            if urlparse(img_url).netloc != urlparse(webpage_url).netloc:
                download_image(img_url, save_dir)

    driver.quit()

if __name__ == "__main__":
    url_to_scrape = 'url_here'  # Replace with the target webpage
    download_directory = 'downloaded_images'  # Directory to save images
    find_external_images(url_to_scrape, download_directory)
