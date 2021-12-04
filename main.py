import utils.db_manager as db_manager
import services.wish_service as wish_service

from models.wish import Wish

db_manager.initialize()
wish_service.retrieve_history("character")
wishes = wish_service.list("character")

stats = {
    "characters": {
        "5 star": 0,
        "4 star": 0
        },
    "weapons": {
        "5 star": 0,
        "4 star": 0,
        "3 star": 0
        }
    }

for wish in wishes:
    if wish.get_item_type() == Wish.ITEM_TYPES["weapon"]:
        if wish.get_rank_type() == Wish.RANK_TYPES[3]:
            stats["weapons"]["3 star"] += 1
        elif wish.get_rank_type() == Wish.RANK_TYPES[4]:
            stats["weapons"]["4 star"] += 1
        elif wish.get_rank_type() == Wish.RANK_TYPES[5]:
            stats["weapons"]["5 star"] += 1
    elif wish.get_item_type() == Wish.ITEM_TYPES["character"]:
        if wish.get_rank_type() == Wish.RANK_TYPES[4]:
            stats["characters"]["4 star"] += 1
        elif wish.get_rank_type() == Wish.RANK_TYPES[5]:
            stats["characters"]["5 star"] += 1

print(stats)
