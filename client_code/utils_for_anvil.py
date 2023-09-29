# anvil requires dropdown items to be either a list of strings or tuples.  if tuples, it needs ('label', value)
def convert_list_of_ints_to_tuples_for_dd(list_of_int: list[int]) -> list[tuple]:
  return [(str(i), i) for i in list_of_int]

def color_rows(rp):
  '''rp is an anvil.RepeatingPanel'''
  for i, r in enumerate(rp.get_components()):
    if not i%2:
      r.background='theme:Gray 200'
