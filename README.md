[![pytest](https://github.com/Zirochkaa/medication-notification/actions/workflows/run_tests.yml/badge.svg?branch=master)](https://github.com/Zirochkaa/medication-notification/actions/workflows/run_tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Zirochkaa/medication-notification/badge.svg)](https://coveralls.io/github/Zirochkaa/medication-notification)

# Medication notification

## TODO Migrate to aiogram v3 using [Migration FAQ (2.x -> 3.0)](https://docs.aiogram.dev/en/dev-3.x/migration_2_to_3.html) guide.

This repository contains pet project - telegram bot designed for sending reminders (notifications) for taking medications :)

### Link to the working telegram bot here - [@medication_notification_bot](https://t.me/medication_notification_bot) (currently shut down).

## Run project locally

1. Setup and activate your local python environment. [Here](https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3) are few guides on how to do it.
2. Install requirements:
   ```shell 
   pip install -r requirements-ci.txt
   ```
3. Create `.env` file:
   ```shell 
   cp app/.env.template app/.env
   ```
4. Setup MongoDB. You have few options:

    4.1. you can use any already existing MongoDB (in docker, in any cloud provider, etc.):
      1. create new database;
      2. update `DATABASE_URL` in `.env` file;

    4.2. you can set up MongoDB locally. For example, you can use [this](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/) guide or any other guide.
5. Obtain Telegram Bot Token by creating Telegram Bot. 
[Here](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) (`Obtain Your Bot Token` section) is a guide on how to do it. 
Update `TELEGRAM_BOT_TOKEN` in `.env` file.
6. If you want to receive logs notifications (when user takes medication or when new user starts using bot) you need to fill `TELEGRAM_CHANNEL_ID` in `.env` file and you will receive logs notifications in telegram private channel.
[Here](https://stackoverflow.com/a/56546442/7365971) is guide on how to obtain telegram private channel id.
Update `TELEGRAM_CHANNEL_ID` in `.env` file.
7. This app uses a webhook approach to processing bot updates. 
In order to do it your localhost has to be put on the internet.
You can achieve this by using [ngrok](https://ngrok.com). You need to [install](https://ngrok.com/download) it and run:
   ```shell 
   ./ngrok http 8000
   ```
   After running above command you will see something like this: 
<img width="829" alt="image" src="https://github.com/airbytehq/airbyte/assets/19872253/b1afc285-4fff-4f7f-b6fd-f03a67655b4c">

   You will need to copy `Forwarding` part (for example, on the screenshot it will be `https://03d2-146-70-181-35.ngrok-free.app`) and update `APP_BASE_URL` in `.env` file.

8. It's time to run application:
   ```shell 
   uvicorn app.run:app --reload
   ```
9. Go to [127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

## Tests

To run tests use following command:
   ```shell 
   pytest tests/
   ```

If you want to check code coverage use following command:
   ```shell 
   pytest --cov-config=.coveragerc --cov=app tests/
   ```
