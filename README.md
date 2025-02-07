##  🚀 Installation
Windows
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
MacOS
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Settings
```env
# WOW.XYZ
MCAP_RANK = 20  # TOP 20 by market cap
BUY_VALUE = [0.05, 0.3]  # $0.05 - $0.30
CACHE_MAX_AGE = 5  # update json cache every 5 min

# Account management
SHUFFLE_KEYS = True
USE_PROXY = True

SLEEP_BETWEEN_WALLETS = [30, 60]
SLEEP_BETWEEN_ACTIONS = [10, 20]

RETRY = 1

```
