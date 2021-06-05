# te-eg-usage
> Telecom Egypt Usage - Selenium simple scraper to get your data usage info

[![PyPI Version][pypi-version]][pypi-url]
[![PyPI License][pypi-license]][pypi-url]
[![PyPI Downloads][pypi-downloads]][pypi-url]

Get your Telecom Egypt account data usage info from [my.te.eg](https://my.te.eg/) website directly from \
Python or through the Command-Line Interface entry point. Get what you own \
and know why your data is being stolen.

## Installation

You will need a webdriver for selenium to run te-eg-usage \
Read [this](https://selenium-python.readthedocs.io/installation.html#drivers) for instructions on how to install
one.

### Using PyPi
```console
pip install te-eg-usage
```

### Manual installation
```console
git clone https://github.com/FaresAhmedb/te-eg-usage.git
cd te-eg-usage && python setup.py install --user
```

## Usage

### Command-Line Interface

First we will have to set enviroment variables for the entry point to access and use to log-in 

OS X & Linux:
```bash
$ export WE_MOBILE_NUMBER=XXXXXXXXXX
$ export WE_PASSWORD=XXXXXXXX
```

Windows:
```powershell
> set WE_MOBILE_NUMBER=XXXXXXXXXX
> set WE_PASSWORD=XXXXXXXX
```

Now you can use it!

```console
$ te-eg-usage
{
    "data_timestamp": 1622923340.4587903,
    "consumed": 39.1,
    "remaining": 100.9,
    "start_date": "2021-06-02",
    "renewal_date": "2021-07-02",
    "remaining_days": 27,
    "renewal_cost": 120.0
}
```

CLI Arguments
```
$ # To use a specific webdriver. firefox-headless is the default
$ te-eg-usage --browser BROWSERNAME
$ # Avillable webdrivers are firefox, firefox-headless, chrome, chrome-headless, edge
$
$ # For debug mode
$ te-eg-usage --debug
$
$ # To get a dict Python object instead of JSON
$ te-eg-usage
$
$ # Everything demo
$ te-eg-usage --debug --dict --browser chrome
```

### Pytohn
`This snippet will get you started
```python
from te_eg_usage import TeEgUsage

usage_data_scraper = TeEgUsage(
    mobile_number="XXXXXXXXXX",
    password="XXXXXXXX",
    browser_name="chrome",
)

usage_data = usage_data_scraper.run() # .run(data_type="json") for json

print("\n".join("{}\t{}".format(k, v) for k, v in usage_data.items()))

# output:
# data_timestamp  1622923340.4587903
# consumed        40.0
# remaining       100.0
# start_date      YYYY-MM-DD
# renewal_date    YYYY-MM-DD
# remaining_days  DD
# renewal_cost    120.0
```

## Release History

* 1.0.0
    * The Release

## Meta

fares ahmed <faresahmed@zohomail.com>

Distributed under the GPLv3 license. See ``LICENSE`` for more information.

[https://github.com/faresahmedb/te-eg-usage](https://github.com/faresahmedb/)

## Contributing

1. Fork it (<https://github.com/faresahmedb/te-eg-usage/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[pypi-url]: https://pypi.python.org/pypi/te-eg-usage/
[pypi-version]: https://img.shields.io/pypi/v/te-eg-usage.svg
[pypi-license]: https://img.shields.io/pypi/l/te-eg-usage.svg
[pypi-downloads]: https://img.shields.io/pypi/dm/te-eg-usage.svg
