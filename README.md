# messenger-chat-images

Use Selenium WebDriver and Python to download all images from a Messenger Chat Group.

## Introduction

To download images from a Messenger chat group, you can create an app and use the Messenger API.

This Python snippet is trying to do the same thing, but avoids using the Messanger API as new
requirements continuously makes it harder to use the tools from Meta.

Inspired by [leoguillaume/fbm-image-scraper](https://github.com/leoguillaume/fbm-image-scraper).

## Requirements

* Python 3.
* Selenium WebDriver 4 for Python.
* Microsoft Edge WebDriver 114.
* Membership of a Messenger Group Chat.

## Installation

1. Clone the Git repository [messenger-chat-images](https://github.com/jorn-hansen/messenger-chat-images).
2. Add the necessary Python package requirements as stated in `requirements.txt` to your virtual environment.
3. Download the Microsoft Edge
   WebDriver [msedgedriver.exe](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and add its
   location to your path.
4. Use the file `config-template.ini` as a template for creating a file `config.ini`.

## Contents of the configuration file

The configuration file nees to two entries:

1. The username (email address) of the Facebook account.
2. The URL of your Group Chat Media.
3. The location of your Microsoft Edge default download directory.

Please note: The configuration parser does not accept percent-signs '%'. Prepend any %-signs in the URL's with yet
another %-sign: '%%' instead of just '%'.

When the program runs, you will have 1 minute to enter password and login to your facebook account.

### How to get the URL of your Group Chat Media

1. Browse to [Messenger](https://www.messenger.com).
2. Choose the Chat.
3. Choose Media and Files.
4. Choose Media.
5. Choose the latest image.
6. Copy the URL.

The URL is of the form:

```commandline
https://www.messenger.com/messenger_media?attachment_id=999999999999999999&message_id=mid.AAAAAAAAAAAAAAAAAAA&thread_id=9999999999999
```

Add the URL from above as the `media_path` in your `config.ini` file.

## How to run

```commandline
$ python3 download_images
```

## Function

1. The program uses Selenium WebDriver to start Edge.
2. You will need to enter your Facebook account password and press the submit button.
3. After a minute, the program starts downloading the current image.
4. The program continues to second last image.
5. The images is downloaded.
6. And so the program continues until last image.

The downloaded images are downloaded to the default Downloads directory of Microsoft Edge.

