import sqlite3
import utils.db_manager as db_manager
import integrations.miHoYo.client as client

from models.wish import Wish

def retrieve_history(gacha_type, load_all=False):
    end_id = "0"
    result = client.index(gacha_type, end_id=end_id)

    while len(result["data"]["list"]) > 0:
        count = create(result["data"]["list"])

        if not load_all and count < len(result["data"]["list"]):
            break

        end_id = result["data"]["list"][-1]["id"]
        result = client.index(gacha_type, end_id=end_id)

def create(list):
    count = 0
    with sqlite3.connect(db_manager.DB_PATH) as conn:
        cursor = conn.cursor()
        for element in list:
            cursor.execute("""
                SELECT external_id, gacha_type FROM wishes WHERE external_id = ? AND gacha_type = ?
            """, (element["id"], element["gacha_type"]))
            record = cursor.fetchone()

            if record is None:
                count += 1
                cursor.execute("""
                    INSERT INTO wishes (external_id, time, name, gacha_type, item_type, rank_type) VALUES(?, ?, ?, ?, ?, ?)
                """, (element["id"], element["time"], element["name"], element["gacha_type"], element["item_type"], element["rank_type"]))
                
        cursor.close()
        return count

def list(gacha_type):
    with sqlite3.connect(db_manager.DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
          SELECT id, external_id, time, name, gacha_type, item_type, rank_type
            FROM wishes
            WHERE gacha_type = ?
            ORDER BY datetime(time) DESC
        """, (Wish.GACHA_TYPES[gacha_type],))
        records = cursor.fetchall()

        wishes = []

        for record in records:
          wishes.append(Wish(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))

        cursor.close()
        return wishes
