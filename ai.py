import deck
import solitaire as s


# prioritize moving columns to columns
# prioritize larger columns for movement
# move from hand to column
# draw card if no valid moves
# always move ace to foundation if possible

class Player:
  def __init__(self, game=None):
    self.start_game(game)
    self.visible_cards_count = [1] * s.Solitaire.col_len
    self.visited = []
    self.wins = 0
    self.losses = 0
    
  def start_game(self, game):
    self.moves = 0
    self.game = s.Solitaire() if game is None else game
    
  def generate_valid_moves(self):
    # -2 = card to foundation
    # -1 = hand to columns
    # 0-7 = columns to columns

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
      if card is None or (card.rank == 12 and card is self.game.columns[src][0]):
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
    if self.game.end():
      return True

    valid_moves = self.generate_valid_moves()
    m_count = len(valid_moves)
    move = None


    # No valid moves
    if m_count == 0:
      move = self.game.draw_card()
    # hand to columns
    elif m_count == 1 and -1 in valid_moves:
      move = self.move_h2c(valid_moves[-1])
    # card to foundation
    elif m_count == 1 and -2 in valid_moves:
      move = self.move_c2f(valid_moves[-2])
    # if 2 moves exist (hand or foundation), move card to foundation
    elif m_count == 2 and -1 in valid_moves and -2 in valid_moves:
      move = self.move_c2f(valid_moves[-2])
    # there is at least 1 column to column move
    else: 
      move = self.move_c2c(valid_moves)

    if move:
      self.moves += 1
    return valid_moves

  def move_h2c(self, moves):
    card = self.game.reserve.pop() 
    dst = self.get_longest_visible_column(moves)
      
    ret = self.game.card_to_column(card, dst)
    self.visible_cards_count[dst] = count_visible(self.game.columns[dst])
    return ret

  def move_c2c(self, moves):
    max_card = deck.Card(suit=-1, rank=-1) # filler card
    max_src = -1

    for src in moves:
      # ignore hand or foundation moves
      if src == -1 or src == -2:
        continue
      # move the largest card first
      curr = s.get_first_visible_card(self.game.columns[src])[0]
      if curr > max_card:
        max_card = curr
        max_src = src
    # move the largest card to the longest pile
    dst = self.get_longest_visible_column(moves[max_src])
    ret = self.game.column_to_column(max_src, dst)
    self.visible_cards_count[dst] = count_visible(self.game.columns[dst])
    return ret

  def move_c2f(self, moves):
    card = None
    for src in moves:
      # skip hand
      if src == -1:
        continue
      # move card from column t o foundation
      else:
        card = self.game.columns[src].pop()
        if not self.game.columns[src].is_empty():
          self.game.columns[src][-1].visible = True
        break
    # move from hand if no other move is possible
    if card is None and -1 in moves:
      card = self.game.reserve.pop()
    return self.game.card_to_foundation(card)
  
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
  p = Player(s.Solitaire(shuffle=False))
  print(p.game.display_game())
  go = None
  while(go != True):
    go = p.best_move()
    print(p.game.display_game())
    print(p.moves)