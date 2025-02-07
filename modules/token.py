import random

import settings
from modules.config import ZERO_ADDRESS, logger
from modules.utils import ether, get_eth_price, wei
from modules.wallet import Wallet


class Token(Wallet):
    def __init__(self, private_key, counter, coin_data):
        super().__init__(private_key, counter)
        self.coin = random.choice(coin_data)["node"]

        self.label += f"{self.coin['symbol'].upper()} |"
        self.usd_price = float(self.coin["usdPrice"])

        self.contract = self.get_contract(self.coin["address"])
        self.min_size = self.contract.functions.MIN_ORDER_SIZE().call()
        self.decimals = self.contract.functions.decimals().call()
        self.market_type = self.contract.functions.marketType().call()

    def calc_token_amount(self, amount_usd, slippage=0.05):
        """Calculates the token amount to purchase, accounting for slippage"""
        token_amount = (amount_usd / self.usd_price) * (10**self.decimals)
        token_amount_w_slippage = int(token_amount * (1 - slippage))

        return token_amount_w_slippage

    def calc_wei_amount(self, amount_usd):
        eth_price = get_eth_price()
        amount_wei = wei(amount_usd / eth_price)

        return amount_wei

    def buy(self):
        usd_amount = random.uniform(*settings.BUY_VALUE)
        token_amount = self.calc_token_amount(usd_amount)
        wei_amount = self.calc_wei_amount(usd_amount)

        if wei_amount >= self.get_balance():
            logger.warning(
                f"{self.label} Generated amount {ether(wei_amount):.6f} exceeds wallet balance, skipping\n"
            )
            return False

        order_size = max(token_amount, self.min_size)

        contract_tx = self.contract.functions.buy(
            self.address,  # recipient
            self.address,  # refundRecipient
            ZERO_ADDRESS,  # orderReferrer
            "",  # comment
            self.market_type,  # expectedMarketType
            order_size,  # minOrderSize
            0,  # sqrtPriceLimitX96
        ).build_transaction(self.get_tx_data(value=wei_amount))

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} buy",
        )
