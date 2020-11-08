import deck

class Foundation(deck.Deck):
  def __init__(self, suit):
    super().__init__([])
    self.suit = suit

  def get_top_cards(self, count=1):
    if len(self) != 0:
      return self[-count:]
    else:
      return [f"[   {deck.Card.icons[self.suit]}]"]

class Solitaire:
  col_len = 7
  pad = "=" * 54
  valid_patterns = [[1,3], [0,2]] # C/S = 0, H/D = 1
  
  def __init__(self, n=1):
    self.draw = n
    self.stock = deck.Deck()
    # self.stock.shuffle()
    self.reserve = deck.Deck([])

    self.columns = []
    for dst in range(Solitaire.col_len):
      cards = deck.Deck([])
      for _ in range(1, dst+2):
        cards.append(self.stock.pop())
      try:
        cards[-1].visible = True
      except:
        pass
      self.columns.append(cards)

    self.foundations = [Foundation(i) for i in range(4)]

    self.moves = 0

  def get_row_count(self):
    n = 0
    for dst in self.columns:
      if len(dst) > n:
        n = len(dst)
    return n

  def display_columns(self):
    
    rows = []
    for row in range(self.get_row_count()):
      r = []
      for dst in range(Solitaire.col_len):
        card = self.columns[dst][row]
        if card is None:
          r.append("")
        else:
          r.append(card)
      rows.append("\t".join(str(card) for card in r))
    return "\n".join(rows)
  
  def display_game(self):
    # col_len columns for cards
    r1 = [""] * Solitaire.col_len
    r1[0] = f"[ {len(self.stock):02} ]"
    for i in range(4):
      r1[3+i] = self.foundations[i].get_top_cards()[0]

    r2 = [f"[ {len(self.reserve):02} ]"] + self.reserve.get_top_cards()

    r1 = "\t".join(str(_) for _ in r1)
    r2 = "\t".join(str(_) for _ in r2)
    return "\n\n".join([Solitaire.pad, r1, r2, self.display_columns(), Solitaire.pad])

  def draw_card(self, count=None):
    if count == None:
      count = self.draw

    # If the draw pile does not have enough cards, reshuffle available cards
    if self.stock.is_empty():
      self.reset_deck()

    for _ in range(count):
      drawn_card = self.stock.pop()
      drawn_card.visible = True
      self.reserve.append(drawn_card)

  def reset_deck(self):
    while not self.reserve.is_empty():
      # move all reserve cards to draw pile while preserving order
      return_card = self.reserve.pop()
      return_card.visible = False
      self.stock.append(return_card)

  def card_to_column(self, card: deck.Card, dst: int):
    # move a card to a column
    compare_card = self.columns[dst][-1]
    valid = is_valid_move(card, compare_card)
    if valid:
      self.columns[dst].append(card)
    
    return valid

  def card_to_foundation(self, card: deck.Card):
    # move a card to the foundations piles
    compare_card = self.foundations[card.suit][-1]
    valid = is_valid_move(card, compare_card, foundation=True)
    if valid:
      self.foundations[card.suit].append(card)
    
    return valid

  def column_to_column(self, src: int, dst: int):
    # move a group of cards from a source column to a destination column
    card, i = get_first_visible_card(self.columns[src])
    compare_card = self.columns[dst][-1]
    valid = is_valid_move(card, compare_card)
    if valid:
      while len(self.columns[src]) > i:
        self.columns[dst].append(self.columns[src].pop(i))
      if not self.columns[src].is_empty():
        self.columns[src][-1].visible = True

    return valid

  def won(self):  
    for f in self.foundations:
      if len(f) != 13:
        return False
    return True

def get_first_visible_card(src: deck.Deck):
  card = None
  i = 0
  if src.is_empty():
    return None, None
  for c in src:
    if c is not None and c.visible == True:
      card = c
      break
    i += 1
  return card, i
      
def is_valid_move(card_1: deck.Card, card_2: deck.Card, foundation=False):
  ordinance = False
  pattern = foundation
  if card_1 is None:
    return False

  if foundation:
    if card_2 is not None:
      ordinance = card_1.rank == (card_2.rank + 1)
    else:
      ordinance = card_1.rank == 0
  else:
    if card_2 is not None:
      ordinance = card_1.rank == (card_2.rank - 1)
      pattern = card_1.suit in Solitaire.valid_patterns[card_2.suit % 2]
    else:
      ordinance = card_1.rank == 12
      pattern = True
  return ordinance and pattern

  


if __name__ == '__main__':
  s = Solitaire()
  s.draw_card()
  print(s.display_game())
  card = s.reserve.pop()
  s.card_to_column(card, 4)
  print(s.display_game())
  s.column_to_column(4,0)
  print(s.display_game())
  s.column_to_column(5,0)
  print(s.display_game())
  while not s.stock.is_empty():
    s.draw_card()
  print(s.display_game())
  s.draw_card()
  print(s.display_game())