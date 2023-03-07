import pickle

verified_view = False


if verified_view:
    with open('output/non_vetted_addresses.pickle', 'rb') as f:
        addresses = pickle.load(f)
else:
    with open('output/rich_contract_addresses_unverified.pickle', 'rb') as f:
        addresses = pickle.load(f)


# Print all the addresses to the console
for address in addresses:
    print(address)


