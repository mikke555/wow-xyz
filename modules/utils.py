import json
import os
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List

import questionary
import requests
from questionary import Choice
from tqdm import tqdm
from web3 import Web3

import settings
from modules.config import logger


def get_module():
    choices = [
        Choice("buy random coin on wow.xyz", "buy_token"),
        Choice("random transaction on Base", "base_txn"),
    ]
    module = questionary.select(
        "Select an action to perform:",
        choices=choices,
    ).ask()
    return module


def wei(amount_eth: float) -> int:
    return Web3.to_wei(amount_eth, "ether")


def ether(amount_wei: int) -> float:
    return Web3.from_wei(amount_wei, "ether")


def get_eth_price(symbol="ETH") -> float:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    response = requests.get(url)
    data = response.json()

    return float(data["price"])


def sort_by_mcap(data: List[Dict], limit: int = settings.MCAP_RANK) -> List[Dict]:
    """Sorts a list of coins by market and returns the top entries"""
    sorted_data = sorted(
        data, key=lambda x: float(x["node"]["marketCap"]), reverse=True
    )
    top_coins = sorted_data[:limit]

    return top_coins


def get_coins(json_path: str) -> None:
    """Fetches coin data from wow.xyz and writes to a json file"""
    json_data = {
        "query": "query pagesWowHomePageQuery(\n  $sortType: WowTrendingType!\n  $chainName: EChainName!\n) {\n  ...WowHomePageTokenListFragment_2IshaC\n}\n\nfragment WowHomePageTokenListFragment_2IshaC on Query {\n  wowTrending(trendingType: $sortType, order: DESC, chainName: $chainName, first: 50) {\n    edges {\n      node {\n        name\n        address\n        chainId\n        description\n        creator {\n          __typename\n          avatar {\n            small\n          }\n          handle\n          walletAddress\n          ... on Node {\n            __isNode: __typename\n            id\n          }\n        }\n        hasGraduated\n        image {\n          mimeType\n          originalUri\n          medium\n        }\n        usdPrice\n        symbol\n        totalSupply\n        marketCap\n        blockTimestamp\n        nsfw\n        socialLinks {\n          twitter\n          discord\n          website\n          telegram\n        }\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n    }\n    count\n  }\n}\n",
        "variables": {
            "sortType": "MARKETCAP",
            "chainName": "BaseMainnet",
        },
    }

    resp = requests.post("https://api.wow.xyz/universal/graphql", json=json_data)

    if resp.status_code != 200:
        print(f"HTTP Error: {resp.status_code} {resp.text}")

    data = resp.json()["data"]["wowTrending"]["edges"]

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)


def fetch_data(
    *, update: bool = False, json_path: str = "data/trending.json"
) -> List[Dict]:
    """Fetches data either from a local JSON cache file or from a remote API"""
    if update:
        json_data = None
    else:
        try:
            # Retrieve last modified time of the cache file
            file_stat = os.stat(json_path)
            last_modified_time = datetime.fromtimestamp(file_stat.st_mtime)
            current_time = datetime.now()
            time_difference = current_time - last_modified_time

            time_difference = current_time - last_modified_time

            max_age = timedelta(minutes=settings.CACHE_MAX_AGE)

            # Check if cache is still valid
            if time_difference < max_age:
                with open(json_path, "r") as f:
                    json_data = json.load(f)
                    logger.info("Using data from local JSON cache\n")
            else:
                logger.info("Local cache is outdated...")
                json_data = None

        except FileNotFoundError:
            logger.info("No local cache found...")
            json_data = None

    # If no cache found, fetch the data from remote source
    if not json_data:
        logger.info("Fetching data from remote API\n")
        get_coins(json_path)
        # Load the newly fetched data
        with open(json_path, "r") as f:
            json_data = json.load(f)

    return sort_by_mcap(json_data)


def random_sleep(from_sleep: int, to_sleep: int) -> None:
    x = random.randint(from_sleep, to_sleep)
    time.sleep(x)


def sleep(from_sleep: int, to_sleep: int) -> None:
    x = random.randint(from_sleep, to_sleep)
    desc = datetime.now().strftime("%H:%M:%S")

    for _ in tqdm(
        range(x), desc=desc, bar_format="{desc} | Sleeping {n_fmt}/{total_fmt}"
    ):
        time.sleep(1)
    print()
