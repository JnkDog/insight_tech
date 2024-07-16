
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

def find_duplicate_addr(data):
    addr_map = {}
    duplicates = []

    # Populate the addr_map with sets of (lb-id, pool-id)
    for item in data:
        addr = item["addr"]
        lb_id = item["lb-id"]
        pool_id = item["pool-id"]
        if addr not in addr_map:
            addr_map[addr] = []
        addr_map[addr].append((lb_id, pool_id, item))

    # Check for duplicates in the mapped addr lists
    for addr, items in addr_map.items():
        if len(items) > 1:
            seen = set()
            for lb_id, pool_id, item in items:
                if any(lb_id == other_lb_id or pool_id == other_pool_id for other_lb_id, other_pool_id, _ in items if (lb_id, pool_id) != (other_lb_id, other_pool_id)):
                    duplicates.append(item)

    return duplicates

duplicates = find_duplicate_addr(data)
for d in duplicates:
    print(d)