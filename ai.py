import deck
import solitaire as s


# prioritize moving columns to columns
# prioritize larger columns for movement
# move from hand to column
# draw card if no valid moves

class Player:
  def __init__(self, game=None):
    self.game = s.Solitaire() if game is None else game
    self.hand = None
    self.moves = 0
    self.first_visible_cards = [None] * 8
    

  def store_card(self):
    if self.hand == None:
      self.hand = self.game.reserve[-1]
    
  def generate_valid_moves(self):
    # 0 = hand to columns
    # 1-8 = columns to columns
    # value is false if move is invalid
    # values is a list of valid columns if there exists a valid move

    valid_moves = self.generate_h2c_moves()
    valid_moves.update(self.generate_c2c_moves())

    return valid_moves

  def generate_h2c_moves(self):
    # generate moves from reserve to column
    self.store_card()
    valid_h2c = [False] * 8
    t_count = 0
    for i in range(8):
      dst = self.game.columns[i]
      compare_card = dst[-1]
      if s.is_valid_move(self.hand, compare_card):
        valid_h2c[i] = True
        t_count += 1
    if t_count == 0:
      return {}
    else:
      return {0: valid_h2c}

  def generate_c2c_moves(self):
    # generate moves from column to column, element is true if that column can move to another column
    valid_c2c = {col+1: [False for _ in range(8)] for col in range(8)}
    
    for i in range(8):
      self.first_visible_cards[i] = (self.game.get_first_visible_card(i))

    for src in range(8):
      card = self.first_visible_cards[src][0]
      if card is None:
        valid_c2c.pop(src+1)
        continue
      t_count = 0
      for dst in range(8):
        if src == dst:
          continue
        compare_card = self.game.columns[dst][-1]
        if s.is_valid_move(card, compare_card):
          valid_c2c[src+1][dst] = True
          t_count += 1

      if t_count == 0:
        valid_c2c.pop(src+1)

    return valid_c2c

  # def 

if __name__ == '__main__':
  p = Player()
  print(p.generate_valid_moves())
  print(p.first_visible_cards)
 