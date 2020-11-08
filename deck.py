import collections
import random

class Card:
  suits = ["Clubs", "Hearts", "Spades", "Diamonds"]
  icons = ["♣", "♥", "♠", "♦"]
  ranks = [" A", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", " J", " Q", " K"]

  def __init__(self, suit=0, rank=3, visible=False):
    self.suit = suit
    self.rank = rank
    self.visible = visible

  def __str__(self):
    rank = Card.ranks[self.rank]
    icon = Card.icons[self.suit]
    if self.visible:
      return f"[{rank} {icon}]"
    else:
      return "[    ]"
  
  def __repr__(self):
    return self.__str__()

class Deck:
  def __init__(self, cards=None):
    if cards == None:
      self.cards = [Card(suit, rank) for suit in range(4) for rank in range(13)]
    else:
      self.cards = cards

  def __str__(self):
    return '\t'.join(str(card) for card in self.cards)

  def __len__(self):
    return len(self.cards)

  def __getitem__(self, index):
    try:
      return self.cards[index]
    except:
      pass

  def append(self, card):
    self.cards.append(card)

  def remove(self, card):
    self.cards.remove(card)

  def pop(self, i=-1):
    return self.cards.pop(i)

  def insert(self, i, card):
    self.cards.insert(i, card)

  def shuffle(self):
    random.shuffle(self.cards)

  def get_top_cards(self, count=1):
    return self[-count:]

  def is_empty(self):
    return len(self.cards) == 0

if __name__ == '__main__':
  deck = Deck()
  deck2 = Deck([])
  print(deck,"\n")
  print(deck2,"Empty\n")
  deck.shuffle()
  print(deck)