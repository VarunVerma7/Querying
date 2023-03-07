import pickle

verified_view = False

if verified_view:
    with open('output/rich_contract_addresses_verfied.pickle', 'rb') as f:
        addresses = pickle.load(f)
else:
    with open('output/rich_contract_addresses_unverfied.pickle', 'rb') as f:
        addresses = pickle.load(f)


# Output the addresses to a text file
file_name_suffix = 'verified' if verified_view else 'unverified'
with open(f'output/addresses_{file_name_suffix}.txt', 'w') as f:
    for address in addresses:
        f.write(f"{address}\n")
