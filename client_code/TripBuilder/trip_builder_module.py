default_point: dict = {'name': '', 'orig': False, 'dest': False, 'lat_long': ()}
default_table: list[dict] = [{'name': '', 'orig': True, 'dest': False, 'lat_long': ()},
                 {'name': '', 'orig': False, 'dest': False, 'lat_long': ()},
                 {'name': '', 'orig': False, 'dest': False, 'lat_long': ()},
                 {'name': '', 'orig': False, 'dest': True, 'lat_long': ()}]

trip_builder_items = default_table

def add_item():
  trip_builder_items.append(default_point)
  print(trip_builder_items)

def delete_item(item):
  trip_builder_items.remove(item)
  print(trip_builder_items)

def update_lat_long_from_db(results: list[dict]) -> None:
  lat_longs: list[tuple[float, float]] = results[0]['lat_longs']
  for idx, p in enumerate(trip_builder_items):
    p['lat_long'] = lat_longs[idx]
