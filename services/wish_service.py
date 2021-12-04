import sqlite3
import utils.db_manager as db_manager
import integrations.miHoYo.client as client

from models.wish import Wish

def retrieve_history():
    result = client.index("character", 1)
    for element in result["data"]["list"]:
        print(element["id"])
        print(element["time"])
        print(element["gacha_type"])
        print(element["name"])
        print(element["item_type"])
        print(element["rank_type"])
	

def create(external_id, time, name, gacha_type, item_type, rank_type):
    cursor = sqlite3.connect(db_manager.DB_PATH).cursor()
    cursor.execute("""
      INSERT INTO wishes (external_id, time, name, gacha_type, item_type, rank_type) VALUES(?, ?, ?, ?, ?)
    """, (external_id, time, name, gacha_type, item_type, rank_type))

def list(gacha_type):
    cursor = sqlite3.connect(db_manager.DB_PATH).cursor()
    cursor.execute("""
      SELECT id, external_id, time, name, gacha_type, item_type, rank_type
        FROM wishes
        WHERE gacha_type = ?
    """, gacha_type)
    records = cursor.fetchall()

    wishes = []

    for record in records:
      wishes.append(Wish(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))

    return wishes
