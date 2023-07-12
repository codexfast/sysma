import os
import configparser

dev_config = configparser.ConfigParser()
dev_config.read("dev.ini")

if "DEV" in dev_config:
    reopen = dev_config["DEV"].get("reopen", 3)