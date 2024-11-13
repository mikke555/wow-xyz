import random

from eth_account import Account

import settings
from modules.config import logger
from modules.modules_config import buy_token, modules
from modules.utils import get_module, sleep


def run(keys, module):
    if settings.SHUFFLE_KEYS:
        random.shuffle(keys)

    total_keys = len(keys)

    for index, private_key in enumerate(keys, start=1):
        counter = f"[{index}/{total_keys}]"
        address = Account.from_key(private_key).address

        action = random.choice(module) if isinstance(module, list) else module
        logger.info(f"{counter} Performing action: {action.__name__}")

        try:
            tx_status = action(private_key, counter)

            if tx_status and index < total_keys:
                sleep(*settings.SLEEP_BETWEEN_WALLETS)

        except Exception as error:
            logger.error(f"{counter} {address} | Error processing wallet: {error}\n")


def main():
    with open("keys.txt") as file:
        keys = [row.strip() for row in file]

    module = get_module()

    if module == "buy_token":
        run(keys, buy_token)
    elif module == "base_txn":
        run(keys, modules)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Cancelled by user")
