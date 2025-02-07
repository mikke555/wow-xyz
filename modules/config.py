import json
from sys import stderr

from loguru import logger

logger.remove()
logger.add(
    stderr,
    format="<white>{time:HH:mm:ss}</white> | <level>{message}</level>",
)

# Network data
CHAIN_DATA = {
    "ethereum": {
        "rpc": "https://rpc.ankr.com/eth",
        "explorer": "https://etherscan.io",
        "token": "ETH",
        "chain_id": 1,
    },
    "base": {
        "rpc": "https://mainnet.base.org",
        "explorer": "https://basescan.org",
        "token": "ETH",
        "chain_id": 8453,
    },
}

# Infinite amount for max approve
INFINITE_AMOUNT = (
    115792089237316195423570985008687907853269984665640564039457584007913129639935
)

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

# Smart contract addresses on Base Network
OWLTO = "0x26637c9fDbD5Ecdd76a9E21Db7ea533e1B0713b6"
RUBBYSCORE = "0xe10Add2ad591A7AC3CA46788a06290De017b9fB4"
ORBITER = "0x06A9376d079Bac1C5A83C3FD4c5a25B72CE35273"

# ABI
with open("data/abi/erc20.json") as f:
    ERC20_ABI = json.load(f)
