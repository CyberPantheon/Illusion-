import time
import requests
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import sys
import re

# UI and UX elements
def display_ui_header():
    print("\033[92m" + "="*60)
    print("""
██╗██╗     ██╗     ██╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗
██║██║     ██║     ██║   ██║██╔════╝██║██╔═══██╗████╗  ██║
██║██║     ██║     ██║   ██║███████╗██║██║   ██║██╔██╗ ██║
██║██║     ██║     ██║   ██║╚════██║██║██║   ██║██║╚██╗██║
██║███████╗███████╗╚██████╔╝███████║██║╚██████╔╝██║ ╚████║
╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    """)
    print(" YOU CAN'T CATCH AN ILLUSION... ".center(60, " "))
    print(" Created by: Cyber Pantheon ".center(60, " "))
    print("="*60 + "\033[0m")

# Call the function to display the header
display_ui_header()

def ask_for_proxy_source():
    print("\033[94m1. Use Proxy API URL")
    print("2. Use Local Proxy File\033[0m")
    choice = input("\033[93mChoose proxy input method (1 or 2): \033[0m")
    
    if choice == '1':
        proxy_url = input("\033[93mEnter Proxy API URL: \033[0m")
        return fetch_proxies_from_api(proxy_url)
    elif choice == '2':
        file_path = input("\033[93mEnter Proxy File Path: \033[0m")
        return fetch_proxies_from_file(file_path)
    else:
        print("\033[91mInvalid choice, please select 1 or 2\033[0m")
        return ask_for_proxy_source()

def ask_for_rotation_time():
    wait_time = input("\033[93mEnter the time in seconds to wait before switching proxies: \033[0m")
    try:
        return int(wait_time)
    except ValueError:
        print("\033[91mInvalid input. Please enter a valid integer.\033[0m")
        return ask_for_rotation_time()

def ask_for_working_proxies():
    num_proxies = input("\033[93mHow many working proxies do you need? \033[0m")
    try:
        return int(num_proxies)
    except ValueError:
        print("\033[91mInvalid input. Please enter a valid integer.\033[0m")
        return ask_for_working_proxies()

def fetch_proxies_from_api(api_url):
    print("\033[92mFetching proxies from API...\033[0m")
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print("\033[91mFailed to fetch proxies from API. Status Code: {}\033[0m".format(response.status_code))
        sys.exit()

def fetch_proxies_from_file(file_path):
    if os.path.exists(file_path):
        print("\033[92mLoading proxies from file...\033[0m")
        with open(file_path, 'r') as f:
            return f.read().splitlines()
    else:
        print("\033[91mFile not found! Please check the path.\033[0m")
        sys.exit()

# Function to check proxy format and return appropriate SeleniumWire options
def parse_proxy(proxy):
    # Handle proxies with different formats (username:password@ip:port or ip:port)
    proxy_pattern = re.compile(
        r'^(?:(?P<ip>[\d\.]+):(?P<port>\d+))'  # IP:Port format
        r'(:(?P<username>[^\s:]+):(?P<password>[^\s:]+))?$'  # Optional username and password
    )
    match = proxy_pattern.match(proxy)

    if not match:
        print(f"\033[91mInvalid proxy format: {proxy}\033[0m")
        return None

    ip = match.group('ip')
    port = match.group('port')
    username = match.group('username')
    password = match.group('password')

    if username and password:
        proxy_url = f"http://{username}:{password}@{ip}:{port}"
    else:
        proxy_url = f"http://{ip}:{port}"

    return {
        'proxy': {
            'http': proxy_url,
            'https': proxy_url,
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

# Function to test proxy availability
def is_proxy_working(proxy, driver):
    try:
        driver.get('http://icanhazip.com/')
        time.sleep(3)
        ip_address = driver.find_element(By.TAG_NAME, 'body').text.strip()
        print(f"\033[92mProxy {proxy} is active. IP: {ip_address}\033[0m")
        return True
    except Exception:
        print(f"\033[91mProxy {proxy} is inactive\033[0m")
        return False

# Main function to rotate proxies without closing the browser
def main():
    #display_ui_header()
    proxies = ask_for_proxy_source()
    wait_time = ask_for_rotation_time()
    num_working_proxies = ask_for_working_proxies()

    working_proxies = []
    chrome_options = Options()
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.add_argument("--proxy-bypass-list=localhost,127.0.0.1")

    driver = None

    # Test proxies and collect the required number of working ones
    for proxy in proxies:
        if len(working_proxies) >= num_working_proxies:
            break
        seleniumwire_options = parse_proxy(proxy)
        if seleniumwire_options:
            if driver is None:
                driver = webdriver.Chrome(seleniumwire_options=seleniumwire_options, options=chrome_options)
            else:
                driver.proxy = seleniumwire_options['proxy']

            if is_proxy_working(proxy, driver):
                working_proxies.append(proxy)

    if len(working_proxies) == 0:
        print("\033[91mNo working proxies found!\033[0m")
        sys.exit()

    # Rotate through the working proxies in a loop
    while True:
        for proxy in working_proxies:
            seleniumwire_options = parse_proxy(proxy)
            if seleniumwire_options:
                driver.proxy = seleniumwire_options['proxy']
                print(f"\033[92mSwitching to proxy: {proxy}\033[0m")
                driver.get('http://icanhazip.com/')
                time.sleep(wait_time)

if __name__ == "__main__":
    main()
