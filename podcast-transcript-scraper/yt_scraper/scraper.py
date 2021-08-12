from .playlist2videoids import retrieve_videoids_from_playlist, upload_file
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
import logging
import os.path
import random
import csv
from time import sleep
waittime = 10														# seconds browser waits before giving up
# random seconds range before loading next video id
sleeptime = [5, 15]
# select True if you want the browser window to be invisible (but not inaudible)
headless = True

# do not modify below


logging.getLogger().setLevel(logging.INFO)


def scrape_from_yt(playlist_id, folder_path):
    # Open metadata file or if not existant, create new one
    meta_filename = folder_path + 'metadata.csv'
    meta_file_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', meta_filename))
    metadata_file = open(meta_file_path, 'a', newline='\n')
    writer = csv.writer(metadata_file)
    if not os.path.exists(meta_file_path):
        writer.writerow(["episodeId", "title", "publishedAt",
                         "channelTitle", "channelId"])
    with open(meta_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        videos = retrieve_videoids_from_playlist(playlist_id, folder_path)

        i = 0
        for item in reversed(videos):
            video_id = item[0]
            try:
                for line in csv_reader:
                    if line[0] == video_id:
                        raise Exception
            except Exception:
                i += 1
                continue

            # check if transcript file already exists
            filename = (
                folder_path + "episode_" + str(i) + ".txt"
            )
            i += 1
            writefilename = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', filename))
            if os.path.isfile(writefilename):
                msg = "transcript file already exists"
                logging.info(msg)
                continue

            options = Options()
            options.add_argument("--headless")

            # Create a new instance of the Firefox driver
            if headless:
                driver = webdriver.Firefox(firefox_options=options)
            else:
                driver = webdriver.Firefox()

            # navigate to video
            driver.get("https://www.youtube.com/watch?v="+video_id)

            try:
                element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "yt-icon-button.dropdown-trigger > button:nth-child(1)")))
            except:
                msg = 'could not find options button'
                driver.quit()
                logging.info(msg)
                continue

            try:
                element.click()
            except:
                msg = 'could not click'
                driver.quit()
                logging.info(msg)
                continue

            try:
                # items > ytd-menu-service-item-renderer:nth-child(2) > yt-formatted-string
                element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ytd-menu-service-item-renderer.style-scope:nth-child(2) > paper-item:nth-child(1) > yt-formatted-string:nth-child(2)")))
            except:
                msg = 'could not find transcript in options menu'
                driver.quit()
                logging.info(msg)
                continue

            try:
                element.click()
            except:
                msg = 'could not click'
                driver.quit()
                logging.info(msg)
                continue

            try:
                element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ytd-transcript-body-renderer.style-scope")))
            except:
                msg = 'could not find transcript text'
                driver.quit()
                logging.info(msg)
                continue

            file = open(writefilename, "w+")
            file.write(element.text)
            file.close()

            upload_file(writefilename, filename)
            writer.writerow([item[0], item[1], item[2], item[3], item[4]])

            driver.quit()

    upload_file(meta_file_path, meta_filename)
