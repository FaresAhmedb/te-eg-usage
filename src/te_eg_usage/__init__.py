#! /usr/bin/env python

"""Telecome Egypt Usage - Selenium Simple scraper to get your data usage info

More information at https://github.com/FaresAhmedb/te-eg-usage
"""

import logging as _logging
import time as _time


__all__ = ["TeEgUsage"]
__version__ = "1.0.0"
__author__ = "Fares Ahmed <faresahmed@zohomail.com>"


class TeEgUsage:
    """Get Scraped Usage information from Telecome Egypt Website"""

    LOGIN_URL = "https://my.te.eg/"
    USAGE_URL = "https://my.te.eg/#/offering/usage"
    SUPPORTED_BROWSERS = [
        "firefox",
        "firefox-headless",
        "chrome",
        "chrome-headless",
        "edge"
    ]

    def __init__(
            self,
            mobile_number, # type: str
            password, # type: str
            browser_name="firefox-headless", # type: str
            browser=None
        ) -> None:
        self.mobile_number = mobile_number # type: str
        self.password = password # type: str
        self.browser_name = browser_name # type: str
        self.browser = browser
        self.usage_data = {} # type: dict

        _logging.basicConfig(format="[%(levelname)s] %(message)s")

        if any(
            [
                not isinstance(self.mobile_number, str),
                not isinstance(self.password, str),
                not self.mobile_number,
                not self.password,
            ]
        ):
            _logging.fatal("MobileNumber/Password is not a non-empty str")
            raise TypeError("Your MobileNumber/Password must be a non-empty str")

        if self.browser_name not in self.SUPPORTED_BROWSERS:
            raise RuntimeError(
                "Sorry this browser is not supported. "
                "Supported browser: " + str.join(", ", self.SUPPORTED_BROWSERS)
            )

        _logging.debug("TeEgUsage has been initialized sucessfully with debug mode on")


    def run(self, data_type: type = "dict", json_indent: int = 4):
        """Run through the process of getting the Usage Data from TeEg

        run(data_type="json", [...]) -> str
        run(data_type="dict", [...]) -> dict

        Args:
            data_type (type, optional): Choose the data type
            of the returned object. Choose anything but "json"
            and it will return a dict. Defaults to "json".
            json_indent (int, optional): The indent in the
            generated json. Defaults to 4.

        Returns:
            if `run(data_type="json", ...)`:
                str/json: Python string object that IS json of the usage data
            else:
                dict: Python dictionary object with the TeEg's usage data
        """
        _logging.debug("Setting `%s` webdriver", self.browser_name)

        try:
            if not self.browser: # if no selenium browser was set manually
                self.set_browser()
        except Exception as error:
            _logging.fatal("couldn't set browser/webdriver `%s`", self.browser_name)
            raise error

        _logging.info("Webdriver %s set sucessfully", self.browser_name)

        try:
            self.login()
        except Exception as error:
            _logging.fatal("Login to %s failed", self.LOGIN_URL)
            raise error

        _logging.info("Sucessfully Logged into %s", self.LOGIN_URL)

        try:
            self.get_usage_data()
        except Exception as error:
            _logging.fatal("Failed to scrape data from %s", self.USAGE_URL)
            raise error

        _logging.info("Successfully scraped data from %s", self.USAGE_URL)

        try:
            self.format_usage_data(data_type=data_type, json_indent=json_indent)
        except Exception as error:
            _logging.fatal("There was an error formating the scraped usage data. %s",
                self.usage_data
            )
            raise error

        self.browser.quit()

        return self.usage_data

    def login(self) -> None:
        """Login to Telecome Egypt account using `self.mobile_number`, `self.password`
        """
        from selenium.webdriver.common.keys import Keys

        self.browser.get(self.LOGIN_URL)

        self.browser.switch_to.active_element.send_keys(
            self.mobile_number,
            Keys.TAB,
            self.password,
            Keys.ENTER
        )

        _time.sleep(1)

    def get_usage_data(self) -> None:
        """Get the usage data. DOESN'T WORK WITHOUT THE FUNCTION `TeEgUsage.login()`
        """
        import re

        self.browser.get(self.USAGE_URL)

        _time.sleep(1)

        cons_rmng = self.browser.find_elements_by_class_name("text-dir")
        cons_rmng = list(map(lambda webelm: webelm.text, cons_rmng))

        bundle_info = self.browser.find_elements_by_class_name("col-sm-6")
        bundle_info = list(map(lambda webelm: webelm.text, bundle_info[1::2]))

        self.usage_data["data_timestamp"] = _time.time().__str__()
        self.usage_data["consumed"      ] = cons_rmng  [0]
        self.usage_data["remaining"     ] = cons_rmng  [1]
        self.usage_data["start_date"    ] = bundle_info[0]
        self.usage_data["renewal_date"  ] = bundle_info[1]
        self.usage_data["remaining_days"] = bundle_info[2]
        self.usage_data["renewal_cost"  ] = bundle_info[3]

        # Remove all characters but numbers. "this 3.42" -> [3, 42]
        for elm in self.usage_data:
            self.usage_data[elm] = list(
                                map(
                            int, re.findall(r"\b\d+\b", self.usage_data[elm])
                        )
                    )


    def format_usage_data(self, data_type: str, json_indent=4):
        """Format the Usage Data generated from `TeEgUsage.get_usage_data()`
        """
        from  datetime import datetime

        # Replace all known float elements (e.g. [33, 19]) to float type
        for float_elm in ["data_timestamp", "consumed", "remaining", "renewal_cost"]:
            self.usage_data[float_elm] = float(
                                    str.join(
                                ".", list(map(str, self.usage_data[float_elm]))
                            )
                        )

        # Replace all known date elements to "YYYY-MM-DD" format
        for date_elm in ["start_date", "renewal_date"]:
            self.usage_data[date_elm] = datetime(
                    year  = self.usage_data[date_elm][0],
                    month = self.usage_data[date_elm][1],
                    day   = self.usage_data[date_elm][2]
                ).strftime("%Y-%m-%d")

        # Replace the list [XX] -> XX since remaining days
        # are not float nor a date but a single int
        self.usage_data["remaining_days"] = self.usage_data["remaining_days"][0]

        if data_type == "json":
            import json

            self.usage_data = json.dumps(self.usage_data, indent=json_indent)


    def set_browser(self):
        """Run the specified browser/webdriver
        """
        from selenium import webdriver
        from os import devnull

        firefox_options = _FirefoxOptionsOptmized()
        chrome_options = _ChromeOptionsOptmizeed()

        if self.browser_name == "firefox":
            self.browser = webdriver.Firefox(options=firefox_options, service_log_path=devnull)
        elif self.browser_name == "firefox-headless":
            firefox_options.add_argument("--headless")
            self.browser = webdriver.Firefox(options=firefox_options, service_log_path=devnull)
        elif self.browser_name == "chrome":
            self.browser = webdriver.Chrome(options=chrome_options)
        elif self.browser_name == "chrome-headless":
            chrome_options.add_argument("--headless")
            self.browser = webdriver.Chrome(options=chrome_options)
        elif self.browser_name == "edge":
            self.browser = webdriver.Edge()


def _FirefoxOptionsOptmized():
    from selenium.webdriver.firefox.options import Options

    """firefox but faster thanks to Eray Erdin
    https://erayerdin.hashnode.dev/how-to-make-selenium-load-faster-with-firefox-in-python-ck7ncjyvw00sd8ss1v4i5xob1
    """
    options = Options()

    options.add_argument("--hide-scrollbars")
    options.add_argument("--disable-gpu")
    options.set_preference("network.http.proxy.pipelining", True)
    options.set_preference("network.http.pipelining.maxrequests", 8)
    options.set_preference("content.notify.interval", 500000)
    options.set_preference("content.notify.ontimer", True)
    options.set_preference("content.switch.threshold", 250000)
    options.set_preference(
        "browser.cache.memory.capacity", 65536
    )  # Increase the cache capacity.
    options.set_preference("browser.startup.homepage", "about:blank")
    options.set_preference(
        "reader.parse-on-load.enabled", False
    )  # Disable reader, we won't need that.
    options.set_preference("browser.pocket.enabled", False)  # Duck pocket too!
    options.set_preference("loop.enabled", False)
    options.set_preference(
        "browser.chrome.toolbar_style", 1
    )  # Text on Toolbar instead of icons
    options.set_preference(
        "browser.display.show_image_placeholders", False
    )  # Don't show thumbnails on not loaded images.
    options.set_preference(
        "browser.display.use_document_colors", False
    )  # Don't show document colors.
    options.set_preference(
        "browser.display.use_document_fonts", 0
    )  # Don't load document fonts.
    options.set_preference(
        "browser.display.use_system_colors", True
    )  # Use system colors.
    options.set_preference(
        "browser.formfill.enable", False
    )  # Autofill on forms disabled.
    options.set_preference(
        "browser.helperApps.deleteTempFileOnExit", True
    )  # Delete temprorary files.
    options.set_preference("browser.shell.checkDefaultBrowser", False)
    options.set_preference("browser.startup.homepage", "about:blank")
    options.set_preference("browser.startup.page", 0)  # blank
    options.set_preference(
        "browser.tabs.forceHide", True
    )  # Disable tabs, We won't need that.
    options.set_preference(
        "browser.urlbar.autoFill", False
    )  # Disable autofill on URL bar.
    options.set_preference(
        "browser.urlbar.autocomplete.enabled", False
    )  # Disable autocomplete on URL bar.
    options.set_preference(
        "browser.urlbar.showPopup", False
    )  # Disable list of URLs when typing on URL bar.
    options.set_preference("browser.urlbar.showSearch", False)  # Disable search bar.
    options.set_preference(
        "extensions.checkCompatibility", False
    )  # Addon update disabled
    options.set_preference("extensions.checkUpdateSecurity", False)
    options.set_preference("extensions.update.autoUpdateEnabled", False)
    options.set_preference("extensions.update.enabled", False)
    options.set_preference("general.startup.browser", False)
    options.set_preference("plugin.default_plugin_disabled", False)
    options.set_preference("permissions.default.image", 2)  # Image load disabled again

    return options


def _ChromeOptionsOptmizeed():
    from selenium.webdriver.chrome.options import Options

    options = Options()

    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    return options


def _main(args=None) -> None:
    import os
    import argparse

    parser = argparse.ArgumentParser(
        prog="te-eg-usage",
        description=__doc__,
        add_help=False
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run the program in DEBUG log level"
    )

    parser.add_argument(
        "-b", "--browser",
        help="Choose the web driver to run on",
        default="firefox-headless",
        choices=TeEgUsage.SUPPORTED_BROWSERS,
    )

    parser.add_argument(
        "--dict",
        action="store_true",
        help="Get the output in Python's dict type"
    )

    args = parser.parse_args()

    if "WE_MOBILE_NUMBER" not in os.environ:
        os.sys.exit("WE_MOBILE_NUMBER enviroment variable was not defined")

    if "WE_PASSWORD" not in os.environ:
        os.sys.exit("WE_PASSWORD enviroment variable was not defined")

    if args.debug:
        _logging.getLogger().setLevel("DEBUG")

    if args.dict:
        data_type = "dict"
    else:
        data_type = "json"

    get_usage_data = TeEgUsage(
        mobile_number=os.environ["WE_MOBILE_NUMBER"],
        password=os.environ["WE_PASSWORD"],
        browser_name=args.browser,
    )

    usage_data = get_usage_data.run(data_type=data_type)

    print(usage_data)


if __name__ == "__main__":
    import sys

    sys.exit(_main())
