class Wish:
  def __init__(self, id, external_id, time, name, gacha_type, item_type, rank_type):
    self._id = id
    self._external_id = external_id
    self._time = time
    self._name = name
    self._gacha_type = gacha_type
    self._item_type = item_type
    self._rank_type = rank_type

  def get_id(self):
    return self._id

  def get_external_id(self):
    return self._external_id

  def get_time(self):
    return self._time

  def get_name(self):
    return self._name

  def get_gacha_type(self):
    return self._gacha_type

  def get_item_type(self):
    return self._item_type

  def get_rank_type(self):
    return self._rank_type
