from scraping.find_rich_addresses import find_rich_addresses
from scraping.find_rich_addresses import filter_addresses_with_balance
def main():

    find_rich_addresses()
    filter_addresses_with_balance()
    filter_contracts_verified(filename)