import random

from eth_account import Account
from web3.exceptions import ContractLogicError

import settings
from modules.config import logger
from modules.modules_config import buy_token, modules
from modules.utils import get_module, sleep


def run(keys, module):
    if settings.SHUFFLE_KEYS:
        random.shuffle(keys)

    total_keys = len(keys)
    max_attempts = 3

    for index, private_key in enumerate(keys, start=1):
        counter = f"[{index}/{total_keys}]"
        address = Account.from_key(private_key).address

        # Convert module into a list
        actions = module if isinstance(module, list) else [module]

        attempts = 0
        while attempts < max_attempts:
            action = random.choice(actions)
            logger.info(f"{counter} action: {action.__name__}")

            try:
                tx_status = action(private_key, counter)

                if tx_status and index < total_keys:
                    sleep(*settings.SLEEP_BETWEEN_WALLETS)
                break  # Success, move on to the next wallet

            except ContractLogicError as err:
                logger.error(f"{counter} {address} | ContractLogicError: {err}")
                logger.debug(f"{counter} {address} | Retrying with a different action")

                attempts += 1

            except Exception as error:
                logger.error(
                    f"{counter} {address} | Error processing wallet: {error}\n"
                )
                break
        else:
            logger.error(
                f"{counter} {address} | Exceeded maximum attempts for this wallet"
            )


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
