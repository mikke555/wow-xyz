import random

from modules.orbiter import Orbiter
from modules.owlto import Owlto
from modules.rubyscore import RubyScore
from modules.token import Token
from modules.utils import fetch_data

top_coins = None


def buy_token(private_key, wallet_label):
    global top_coins

    if top_coins is None:
        top_coins = fetch_data()
        random.shuffle(top_coins)

    token = Token(private_key, wallet_label, top_coins)
    return token.buy()


def ruby_vote(private_key, wallet_label):
    rubby = RubyScore(private_key, wallet_label)
    return rubby.vote()


def owlto_checkin(private_key, wallet_label):
    owlto = Owlto(private_key, wallet_label)
    return owlto.check_in()


def orbiter_checkin(private_key, wallet_label):
    orbiter = Orbiter(private_key, wallet_label)
    return orbiter.check_in()


modules = [ruby_vote, owlto_checkin, buy_token, orbiter_checkin]
