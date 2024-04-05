'''from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())


def main():
    read_contract()'''

# main.py
import front_gui
from front_gui import a

# Check if my_variable is defined and has a value
if 'my_variable' in globals() and a is not None:
    print("my_variable is defined and has a value:", a)
else:
    print("my_variable is either not defined or has no value")
    a = front_gui.a