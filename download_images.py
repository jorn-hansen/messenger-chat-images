import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import configparser


def get_config():
    """
    Read from file 'config.ini' the email-address of the facebook account,
    the URL of the Media files on the Messenger Group Chat, and the downloads
    directory.

    :return: A dict containing the Facebook information from the config-file
    """

    config = configparser.ConfigParser()
    config.read('config.ini')
    email = config.get('Facebook', 'email')
    media_path = config.get('Facebook', 'media_path')
    download_path = config.get('Local', 'download_path')

    return {"email": email, "media_path": media_path, "download_path": download_path}


def goto_messenger_images():
    """
    Use the URL from the Facebook context to open a Web browser. Ask user to login.

    :return: None
    """
    media_path = facebook_config["media_path"]
    email = facebook_config["email"]

    # Open Edge browser and navigate to Messenger Group Chat Images URL
    driver.get(media_path)

    # Locate text item and set email-address on the login page
    element_email = driver.find_element(By.ID, "email")
    element_email.send_keys(email)

    # Ask user to enter password and press the submit button on the browser. When done, press enter here.
    input("Please go to the browser, enter your password, submit, return here and press the return key...")


def add_start_marker_file(download_path):
    """
    Add or modify a file to mark start of downloading.
    :param download_path: The location of downloaded images.
    :return: The name of the current last modified file of the folder.
    """
    file_name = "download_images_start.txt"
    with open(os.sep.join([download_path, file_name]), "w") as f:
        f.write("Download of images has started")
    return file_name


def get_last_modified_file(download_path):
    path = Path(download_path)
    latest_jpg_file = max(path.glob('*.jpg'), key=lambda f: f.stat().st_ctime)
    latest_mp4_file = max(path.glob('*.mp4'), key=lambda f: f.stat().st_ctime)
    return max([latest_jpg_file, latest_mp4_file], key=lambda f: f.stat().st_ctime).name


def same_file_was_downloaded(last_modified_file, current_modified_file):
    # In case of a real doublet, it must be excempted
    if "359961622_6480373652012446_436942704694269333_n" in current_modified_file:
        return False
    if " " in current_modified_file:
        before_space = current_modified_file[:current_modified_file.find(" ")]
        if before_space in last_modified_file:
            return True
    return False


def wait_for_download_to_end(download_path):
    time.sleep(1)
    current_modified_file = get_last_modified_file(download_path)
    while current_modified_file.endswith(".crdownload"):
        print(f"Waiting for download of file {current_modified_file[:-11]} to end.")
        time.sleep(1)
        current_modified_file = get_last_modified_file(download_path)
    return current_modified_file


def get_groupchat_images(download_path):
    """
    Push the Download-button. Press the left-arrow-key. Repeat until failure.

    :param download_path: The location of the downloaded images.
    :return: None
    """
    last_modified_file = add_start_marker_file(download_path)
    more_files_to_download = True
    while more_files_to_download:
        element_download = driver.find_element(By.XPATH, "//a[contains(@aria-label,'Download')]")
        element_download.click()
        more_files_to_download = False
        counter = 5
        while counter > 0:
            counter -= 1
            current_modified_file = wait_for_download_to_end(download_path)
            if not same_file_was_downloaded(last_modified_file, current_modified_file):
                print(f"Downloaded {current_modified_file}")
                last_modified_file = current_modified_file
                more_files_to_download = True
                break
            else:
                more_files_to_download = False
        ActionChains(driver).send_keys(Keys.LEFT).perform()
        time.sleep(1)
    # Clean up redundant download of last image
    # os.remove(os.sep.join([download_path, current_modified_file]))


if __name__ == "__main__":
    facebook_config = get_config()

    driver = webdriver.Edge()

    goto_messenger_images()

    # Downloaded images go to the default downloads directory of the PC.
    # We need the location to check if we are downloading doublet files.
    dwnpath = facebook_config["download_path"]
    get_groupchat_images(dwnpath)

    driver.quit()
