import deck

class Foundation(deck.Deck):
  def __init__(self, suit):
    super().__init__([])
    self.suit = suit

  def append(self, card):
    if card.suit == self.suit:
      super().append(card)

  def display_top(self, count=1):
    if len(self) != 0:
      return str(self[-count])
    else:
      return f"[   {deck.Card.icons[self.suit]}]"


class Solitaire:
  """
  Represents a game of solitaire
  Attributes:
    stock: the draw pile
    reserve: the drawn card pile
    columns: the piles where the player can stack cards
    foundation: initially empty piles where the player must eventually store cards
  """
  
  def __init__(self, n=1):
    self.draw = n
    self.stock = deck.Deck()
    self.stock.shuffle()

    self.reserve = deck.Deck([])

    self.columns = []
    for col in range(8):
      cards = deck.Deck([])
      for _ in range(col):
        cards.append(self.stock.pop())
      self.columns.append(cards)

    self.foundation = [Foundation(i) for i in range(4)]

  def display_columns(self):
    # n rows by 8 cols
    n = 0
    for col in self.columns:
      if len(col) > n:
        n = len(col)

    rows = []
    for row in range(n):
      r = []
      for col in range(8):
        try:
          r.append(self.columns[col][row])
        except:
          r.append("")
      rows.append("\t".join(str(card) for card in r))
    return "\n".join(rows)
  
  def display_game(self):
    # 8 columns for cards
    r1 = [""] * 8
    r1[0] = "[DECK]"
    for i in range(4):
      print(self.foundation[i])
      r1[-(i+1)] = self.foundation[i].display_top()

    r1 = "\t".join(str(card) for card in r1)
    r2 = self.reserve.display_top(self.draw)
    return "\n".join([r1, r2, self.display_columns()])

if __name__ == '__main__':
  s = Solitaire()
  print(s.display_game())
