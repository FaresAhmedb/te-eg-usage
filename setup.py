import setuptools
from os.path import dirname, join, abspath

setuptools.setup(
    name                          = "te-eg-usage",
    version                       = "1.0.0",
    description                   = "Telecome Egypt Usage - Selenium Simple scraper to get your data usage info",
    long_description              = open(join(abspath(dirname(__file__)), "README.md")).read(),
    long_description_content_type = "text/markdown",
    author                        = "Fares Ahmed",
    author_email                  = "faresahmed@zohomail.com",
    python_requires               = "~=3.5",
    url                           = "https://github.com/FaresAhmedb/te-eg-usage",
    entry_points                  = {
        "console_scripts": ["te-eg-usage=te_eg_usage:_main"],
    },
    include_package_data          =  True,
    install_requires              = ["selenium==3.141.0"],
    package_dir                   = {"": "src"},
    packages                      = setuptools.find_packages(where="src"),
    license                       = "GPLv3",
    classifers                    = [
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Home Automation"
    ]
)
