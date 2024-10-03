# Illusion Proxy Rotation Tool

This tool rotates proxies seamlessly on the same Chrome browser instance without restarting, using Selenium and SeleniumWire. It allows you to fetch proxies from either an API or a local file, check if they are working, and rotate them periodically.

## Features
- Proxy rotation without restarting the browser.
- Proxy source options: API or local file.
- SeleniumWebDriver integration for proxy testing.
- Customizable wait times between proxy switches.
- Collects a specified number of working proxies before rotating.

## Requirements
To run this tool, you need to install the following:

### Software:
- **Python 3.8+**
- **Google Chrome** browser
- **ChromeDriver** that matches your Chrome version
Also you can get 10 free proxies from https://proxy2.webshare.io , then use the api url you get when you click on " download proxy list"
### Python Libraries:
- `seleniumwire` (for managing proxy settings in Selenium)
- `selenium` (for browser automation)
- `requests` (for fetching proxies from an API)
- `re` (for proxy format validation)
- `os`, `sys`, `time` (standard Python libraries)

### ChromeDriver Setup:
1. Download the correct version of **ChromeDriver** from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
2. Add the **ChromeDriver** executable to your system's PATH, or specify its path in the code.

## Installation

To install the necessary Python dependencies, run the following command:

```bash
pip install -r requirements.txt
```



## How to Use

1. **Clone or download this repository** to your local machine.
   
2. **Install the required dependencies** as listed above.
   
3. **Set up ChromeDriver** according to the instructions under the 'Requirements' section.

4. **Run the script:**
   - Execute the Python script with the command:
     ```bash
     python illusion.py
     ```

5. **Follow the prompts**:
   - Choose your proxy source: either a URL API or a local file.
   - Specify the number of working proxies you want.
   - Set the time interval (in seconds) for rotating the proxies.

6. **View output**: The tool will switch proxies and display the active IP in the terminal.

## Sample Usage

After running the script, you'll see the following in your terminal:

```bash
1. Use Proxy API URL
2. Use Local Proxy File
Choose proxy input method (1 or 2): 1
Enter Proxy API URL: http://example.com/proxies
Fetching proxies from API...
Enter the time in seconds to wait before switching proxies: 10
How many working proxies do you need? 3
Switching to proxy: 123.45.67.89:8080
Proxy 123.45.67.89:8080 is active. IP: 123.45.67.89
...
```

### Proxy File Format
If you choose to use a local proxy file, the file should contain one proxy per line in one of the following formats:
```
ip:port
username:password@ip:port
```

---
