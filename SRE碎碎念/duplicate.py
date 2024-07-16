
def find_duplicate_addr(data):
    addr_map = {}
    duplicates = []

    # Populate the addr_map with sets of (lb-id, pool-id)
    for item in data:
        addr = item["addr"]
        lb_id = item["lb-id"]
        pool_id = item["pool-id"]
        if addr not in addr_map:
            addr_map[addr] = set()
        addr_map[addr].add((lb_id, pool_id))

    # Find duplicates where addr has more than one unique (lb-id, pool-id)
    for addr, id_set in addr_map.items():
        if len(id_set) > 1:
            for item in data:
                if item["addr"] == addr:
                    duplicates.append(item)

    return duplicates

duplicates = find_duplicate_addr(data)
for d in duplicates:
    print(d)