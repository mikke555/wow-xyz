import random

from modules.owlto import Owlto
from modules.rubbyscore import RubbyScore
from modules.token import Token
from modules.utils import fetch_data

top_coins = None


def buy_token(private_key, wallet_label):
    global top_coins

    if top_coins is None:
        top_coins = fetch_data(update=False)
        random.shuffle(top_coins)

    token = Token(private_key, wallet_label, top_coins)
    return token.buy()


def rubby_vote(private_key, wallet_label):
    rubby = RubbyScore(private_key, wallet_label)
    return rubby.vote()


def owlto_checkin(private_key, wallet_label):
    owlto = Owlto(private_key, wallet_label)
    return owlto.check_in()


modules = [rubby_vote, owlto_checkin, buy_token]
