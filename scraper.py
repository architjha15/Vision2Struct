"""
scraper.py
----------
Downloads images from Unsplash based on a search query.

Workflow:
1. Create filesystem-safe folder
2. Launch headless browser
3. Scroll to collect image URLs
4. Download images locally
"""

import os
import requests
import time
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def download_bulk_images(query: str, total_limit: int = 10) -> str:
    """
    Scrapes images from Unsplash based on search query
    and stores them in a dedicated folder.

    Args:
        query (str): Search keyword
        total_limit (int): Number of images to download

    Returns:
        str: Path to folder containing downloaded images
    """

    # ---------------------------------------------------------
    # 1. Create filesystem-safe directory
    # ---------------------------------------------------------
    folder_name = query.replace(" ", "_").lower()
    base_dir = "downloads"
    target_dir = os.path.join(base_dir, folder_name)

    os.makedirs(target_dir, exist_ok=True)

    # ---------------------------------------------------------
    # 2. Configure headless Chrome
    # ---------------------------------------------------------
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        # URL-encode query to avoid malformed URLs
        encoded_query = quote(query)
        search_url = f"https://unsplash.com/s/photos/{encoded_query}"

        driver.get(search_url)
        time.sleep(3)

        image_urls = set()
        previous_count = 0
        stagnation_rounds = 0

        print(f"Searching for '{query}' images...")

        # ---------------------------------------------------------
        # 3. Scroll and collect image URLs
        # ---------------------------------------------------------
        while len(image_urls) < total_limit and stagnation_rounds < 3:

            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)

            thumbnails = driver.find_elements(By.TAG_NAME, "img")

            for img in thumbnails:
                src = img.get_attribute("src")

                if (
                    src
                    and "images.unsplash.com" in src
                    and "profile" not in src
                ):
                    clean_url = src.split("?")[0] + "?q=80&w=1000"
                    image_urls.add(clean_url)

                if len(image_urls) >= total_limit:
                    break

            # Detect stagnation (no new images found)
            if len(image_urls) == previous_count:
                stagnation_rounds += 1
            else:
                stagnation_rounds = 0

            previous_count = len(image_urls)

        print(f"Collected {len(image_urls)} image URLs.")

        # ---------------------------------------------------------
        # 4. Download images
        # ---------------------------------------------------------
        for i, url in enumerate(list(image_urls)[:total_limit]):
            try:
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    file_path = os.path.join(
                        target_dir, f"img_{i+1}.jpg"
                    )
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                else:
                    print(f"Skipping image {i+1}: HTTP {response.status_code}")

            except Exception as e:
                print(f"Download failed for image {i+1}: {e}")

        print(f"Download complete. Images saved to '{target_dir}'")

        return target_dir

    finally:
        driver.quit()


# ---------------------------------------------------------
# Standalone Testing
# ---------------------------------------------------------
if __name__ == "__main__":
    user_query = input("Enter search keyword: ")
    user_limit = int(input("How many images to download: "))
    download_bulk_images(user_query, user_limit)
