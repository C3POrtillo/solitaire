import collections
import random

class Card:
  suits = ["Clubs", "Hearts", "Spades", "Diamonds"]
  icons = ["♣", "♥", "♠", "♦"]
  ranks = [" A", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", " J", " Q", " K"]

  def __init__(self, suit=0, rank=3):
    self.suit = suit
    self.rank = rank

  def __str__(self):
    rank = Card.ranks[self.rank]
    icon = Card.icons[self.suit]
    return f"[{rank} {icon}]"

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
    return self.cards[index]

  def append(self, card):
    self.cards.append(card)

  def remove(self, card):
    self.cards.remove(card)

  def pop(self, i=-1):
    return self.cards.pop(i)

  def shuffle(self):
    random.shuffle(self.cards)

  def display_top(self, count=1):
    if len(self) != 0:
      return str(self[-count])
    else:
      return ""

if __name__ == '__main__':
  deck = Deck()
  deck2 = Deck([])
  print(deck,"\n")
  print(deck2,"Empty\n")
  deck.shuffle()
  print(deck)