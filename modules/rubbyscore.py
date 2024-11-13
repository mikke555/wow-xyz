from modules.config import RUBBYSCORE
from modules.wallet import Wallet


class RubbyScore(Wallet):
    def __init__(self, private_key, counter):
        super().__init__(private_key, counter)
        self.label += "RubbyScore |"
        self.contract = self.get_contract(
            RUBBYSCORE, abi=[{"type": "function", "name": "vote", "inputs": []}]
        )

    def vote(self):
        tx_data = self.get_tx_data()
        contract_tx = self.contract.functions.vote().build_transaction(tx_data)

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} vote",
        )
