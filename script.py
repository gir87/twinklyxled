import requests
from datetime import datetime
from polling2 import poll
import xled
from xled_plus.samples.sample_setup import *

# Connect to Twinkly
control_high = xled.HighControlInterface('192.168.xx.xx', '98:cd:ac:xx:xx:xx') # Insert IP and HW id of the Twinkly device here
print("Twinkly leds are on? " + str(control_high.is_on()))

# Store the last preset found
last_preset = None

# Preset names to class constructors
preset_classes = {
    'fire': Fire,
    'water': Water,
    'gold': Gold,
    'sparklestars' : SparkleStars,
    'looplightspectrum' : LooplightSpectrum,
    # Add more presets as needed
}

# Preset function
def set_preset(preset_name):
    global last_preset
    if last_preset != preset_name:
        print(f"{datetime.now()} | Preset set to: {preset_name.capitalize()}")
        ctr = setup_control()
        preset_classes[preset_name](ctr).launch_movie()
        last_preset = preset_name
    else:
        print(f"{datetime.now()} | Current preset: {preset_name.capitalize()}")

# Set up polling parameters
url = "https://example.com/data.txt"
polling_interval = 5  # in seconds

# Connect to URL
def fetch_content(url):
    response = requests.get(url)
    return response.text if response.status_code == 200 else print("Error: not 200")

# Check content of the url
def check_content(url):
    content = fetch_content(url)
    if content:
        found_preset = None
        for preset_name in preset_classes.keys():
            if preset_name in content:
                found_preset = preset_name
                break
        if found_preset:
            set_preset(found_preset)
        else:
            print(f"{datetime.now()} | No preset found")

# Use the polling2 library to poll the content
poll(
    lambda: check_content(url),
    step=polling_interval,
    ignore_exceptions=(requests.exceptions.ConnectionError,),
    poll_forever=True)
