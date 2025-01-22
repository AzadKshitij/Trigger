from configparser import ConfigParser

config_object = None
theme_dark = None

def read_config():
    # Create a ConfigParser object
    config_object = ConfigParser()

    # Read the configuration from the 'config.ini' file
    config_object.read("config.ini")
    # Access the USERINFO section
    theme_dark = config_object["THEME_DARK"]
