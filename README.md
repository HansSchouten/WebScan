# WebScan
Scan for website misconfigurations

## Installation

Dependencies can be installed by running `py setup.py`.

## Usage

Create a data folder and create a `domains.csv` file in the following format:
```
index,domain
0,test.com
1,test2.com
```

Extend `webscan/scanners.py` with additional scanners for each configuration you would like to check.
Add your scanners to `webscan/webscan.py`.

Next, run `py webscan.py`.
