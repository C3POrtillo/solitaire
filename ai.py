import deck
import solitaire as s


# prioritize moving columns to columns
# prioritize larger columns for movement
# move from hand to column
# draw card if no valid moves
# always move ace to foundation if possible

class Player:
  def __init__(self, game=None):
    self.game = s.Solitaire() if game is None else game
    self.moves = 0
    self.visible_cards_count = [1] * s.Solitaire.col_len
    self.visited = []
    
    
  def generate_valid_moves(self):
    # -2 = card to foundation
    # -1 = hand to columns
    # 0-7 = columns to columns
    # value is false if move is invalid
    # values is a list of valid columns if there exists a valid move

    valid_moves = self.generate_h2c_moves()
    valid_moves.update(self.generate_c2c_moves())
    valid_moves.update(self.generate_c2f_moves())
    print(valid_moves)

    return valid_moves

  def generate_h2c_moves(self):
    # generate moves from reserve to column
    top_reserve = self.game.reserve[-1]
    valid_h2c = []
    for i in range(s.Solitaire.col_len):
      dst = self.game.columns[i]
      compare_card = dst[-1]
      if s.is_valid_move(top_reserve, compare_card):
        valid_h2c.append(i)

    if len(valid_h2c) == 0:
      return {}
    else:
      return {-1: valid_h2c}

  def generate_c2c_moves(self):
    # generate moves from column to column, element is true if that column can move to another column
    valid_c2c = {}
   
    for src in range(s.Solitaire.col_len):
      card = s.get_first_visible_card(self.game.columns[src])[0]
      if card is None:
        continue
      for dst in range(s.Solitaire.col_len):
        if src == dst:  
          continue
        compare_card = self.game.columns[dst][-1]
        if s.is_valid_move(card, compare_card):
          if src in valid_c2c:
            valid_c2c[src].append(dst)
          else:
            valid_c2c[src] = [dst]

    return valid_c2c

  def generate_c2f_moves(self):
    # generate moves from column to foundation, element is true if a card can be put on a foundation pile
    valid_c2f = []
    for src in range(s.Solitaire.col_len):
      if not self.game.columns[src].is_empty():
        card = self.game.columns[src][-1]
        compare_card = self.game.foundations[card.suit][-1]
        if s.is_valid_move(card, compare_card, foundation=True):
          valid_c2f.append(src)

    # reserve comparison
    if not self.game.reserve.is_empty():
      card = self.game.reserve[-1]
      compare_card = self.game.foundations[card.suit][-1]
      if s.is_valid_move(card, compare_card, foundation=True):
        valid_c2f.append(-1)

    if len(valid_c2f) == 0:
      return {}
    else:
      return {-2: valid_c2f}
    

  def best_move(self):
    valid_moves = self.generate_valid_moves()
    m_count = len(valid_moves)

    # No valid moves
    if m_count == 0:
      self.game.draw_card()
    # hand is the only valid move
    elif m_count == 1 and -1 in valid_moves:
      self.move_h2c(valid_moves[-1])
    # a card can be put on its respective foundation pile
    elif -2 in valid_moves:
      self.move_c2f(valid_moves[-2])
    # a valid move exists somewhere
    else: 
      self.move_c2c(valid_moves)

    self.moves += 1


  def move_h2c(self, moves):
    card = self.game.reserve.pop() 
    dst = self.get_longest_visible_column(moves)
      
    self.game.card_to_column(card, dst)
    self.visible_cards_count[dst] += 1

  def move_c2c(self, moves):
    max_card = deck.Card(suit=-1, rank=-1) # filler card
    max_src = -1

    for src in moves:
      if src == -1:
        continue
      curr = s.get_first_visible_card(self.game.columns[src])[0]
      if curr > max_card:
        max_card = curr
        max_src = src

    dst = self.get_longest_visible_column(moves[max_src])
    self.game.column_to_column(max_src, dst)
    self.visible_cards_count[dst] = count_visible(self.game.columns[dst])

  def move_c2f(self, moves):
    card = None
    for src in moves:
      if src == -1:
        card = self.game.reserve.pop()
        break
      else:
        card = self.game.columns[src].pop()
        if not self.game.columns[src].is_empty():
          self.game.columns[src][-1].visible = True
        break
    self.game.card_to_foundation(card)
  
  def get_longest_visible_column(self, moves):
    dst = None
    maxi = 0
    for col in moves:
      if self.visible_cards_count[col] > maxi:
        maxi = self.visible_cards_count[col]
        dst = col
    return dst

def count_visible(src: deck.Deck):
  v_count = 0
  if src.is_empty():
    return v_count
  for c in src:
    if c.visible == True:
      v_count += 1
  return v_count


if __name__ == '__main__':
  p = Player()
  print(p.game.display_game())
  for i in range(101):
    p.best_move()
    print(p.game.display_game())
    print(p.moves)
  print("\t".join(str(len(_)) for _ in p.game.foundations))