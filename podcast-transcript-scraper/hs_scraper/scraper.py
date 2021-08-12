# modify these values
# filename = "happy_scribe_podcast_list.csv"  # filname with happy transcripts episodes
# colname = "podcastSeriesName"  # column storing video ids
# delimiter = ","  # delimiter, e.g. ',' for CSV or '\t' for TAB
from dotenv import load_dotenv
import os
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
import logging
import boto3
import os.path
import csv
waittime = 10  # seconds browser waits before giving up
sleeptime = [5, 15]  # random seconds range before loading next video id
# select True if you want the browser window to be invisible (but not inaudible)
headless = True

load_dotenv()

# do not modify below

logging.getLogger().setLevel(logging.INFO)

# Uploads folder files to S3 Bucket


def upload_file(file_path, filename):
    logging.info("S3 Put: {} {}".format(file_path, filename))
    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_SECRET_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION_NAME')
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket('podcast-transscripts')

    bucket.upload_file(file_path, filename)


def scrape_from_hs(podcast_series_name, folder_path):

    # Prepare metadata file
    metadata_filename = folder_path + "metadata.csv"
    meta_file_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', metadata_filename))

    addHeader = False
    if not os.path.exists(meta_file_path):
        logging.info("path doesn't exist")
        addHeader = True
    else:
        logging.info("path does already exist")

    metadata_file = open(meta_file_path, "a", newline="\n")

    writer = csv.writer(metadata_file)

    if addHeader:
        writer.writerow(["episodeId", "title", "publishedAt",
                         "channelTitle", "fileName"])

    logging.info(podcast_series_name)

    options = Options()
    options.add_argument("--headless")

    # Create a new instance of the Firefox driver
    if headless:
        driver = webdriver.Firefox(firefox_options=options)
    else:
        driver = webdriver.Firefox()

    # navigate to happy scribe webpage
    driver.get("https://www.happyscribe.com/public/" + podcast_series_name)

    # Check how many transcripts are available and calc pagination
    try:
        el = WebDriverWait(driver, waittime).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(@class, 'last')]/a")))
        elUrl = el.get_attribute("href")
        splittedUrl = elUrl.split("page=")
        pages_count = int(splittedUrl[1])
        episode_count = int(pages_count * 6)

        logging.info("Pages count: {}".format(pages_count))
        logging.info("Num of episodes: {}".format(episode_count))
    except:
        msg = "could not find number of episodes"
        driver.quit()
        logging.info(msg)

    page = 0
    while page < pages_count:
        page += 1
        driver.quit()
        # Create a new instance of the Firefox driver
        if headless:
            driver = webdriver.Firefox(firefox_options=options)
        else:
            driver = webdriver.Firefox()

        try:
            driver.get("https://www.happyscribe.com/public/" +
                       podcast_series_name + "?sort=all&page={}".format(page))

            event = driver.find_elements_by_class_name("hsp-card-episode")
            logging.info(
                "Page: {} - Num of episodes: {}".format(page, len(event)))

        except Exception as e:
            logging.info(
                "Driver failed navigating to next page with error: {}".format(e))
            page -= 1
            continue

        i_temp = -1
        try:
            for i in range(1, len(event)+1):
                text = ""
                n = i_temp + 2
                i_temp = n
                try:
                    logging.info("n: {}".format(n))
                    element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".hsp-card-episode:nth-child({})".format(n))))
                    element.click()
                except:
                    msg = "could not click on episode"
                    logging.info(msg)
                    episode_count -= 1
                    continue

                title = driver.find_element_by_css_selector(
                    "h1#episode-title").text

                # check if transcript file already exists
                filename = (
                    folder_path + "episode_" + str(episode_count) + ".txt"
                )
                episode_count -= 1
                writefilename = os.path.abspath(os.path.join(
                    os.path.dirname(__file__), '..', filename))
                if os.path.isfile(writefilename):
                    msg = "transcript file already exists"
                    logging.info(msg)
                    continue

                # Write to metadata csv
                published_at = driver.find_element_by_css_selector(
                    ".hsp-episode-stats > .date").text

                writer.writerow([episode_count + 1, title,
                                 published_at, podcast_series_name, filename])
                logging.info("wrote row!!! {}".format(filename))

                paragraphs = driver.find_elements_by_class_name(
                    "hsp-paragraph")

                for paragraph in paragraphs:
                    timestamp = paragraph.find_element_by_class_name(
                        "hsp-paragraph-timestamp")
                    text += timestamp.text[1:-1]
                    text += '\n'
                    content = paragraph.find_element_by_class_name(
                        "hsp-paragraph-words")
                    text += content.text
                    text += '\n'

                # Copy transscript to txt file
                file = open(writefilename, "w+")
                file.write(text)
                file.close()

                # Upload file to S3
                upload_file(writefilename, filename)
                upload_file(meta_file_path, metadata_filename)

                driver.back()
                driver.implicitly_wait(2)
        except Exception as e:
            logging.info("{}".format(e))
            continue

    driver.quit()

    upload_file(meta_file_path, metadata_filename)
    metadata_file.close()
