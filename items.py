def get_room_items(items, room_id):
    for item in items:
        if item["room_id"] == room_id:
            yield item


def get_total(items):
    count = 0
    cost = 0.0
    for item in items:
        count += item["quantity"]
        cost += item["price"] * item["quantity"]
    return count, cost
