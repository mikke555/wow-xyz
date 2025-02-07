from datetime import datetime

from modules.config import ORBITER
from modules.wallet import Wallet


class Orbiter(Wallet):
    def __init__(self, private_key, counter):
        super().__init__(private_key, counter)
        self.label += "Orbiter |"

    def check_in(self):
        date = datetime.now().strftime("%Y%m%d")
        padded_date_hex = hex(int(date))[2:].zfill(64)

        tx = self.get_tx_data(
            data="0x30ea198a" + padded_date_hex,
            to=self.to_checksum(ORBITER),
        )

        return self.send_tx(tx, tx_label=f"{self.label} check-in")
