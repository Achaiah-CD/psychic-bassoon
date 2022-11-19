# A Blackjack game
import random


# A class for each card to be specifically fixed with suit and rank/value.
class Card:

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	# Whenever the str() or print() method is called on this class object
	# the following method will be executed.
	def __str__(self):
		return f'{self.rank["rank"]} of {self.suit}'


# A class for all the cards
class Deck:

	def __init__(self):

		# Cards is going to hold the suits and a dictionary of rank and value
		self.cards = []
		suits = ["spades", "clubs", "diamonds", "hearts"]
		ranks = [{
		 "rank": "A",
		 "value": 11
		}, {
		 "rank": "2",
		 "value": 2
		}, {
		 "rank": "3",
		 "value": 3
		}, {
		 "rank": "4",
		 "value": 4
		}, {
		 "rank": "5",
		 "value": 5
		}, {
		 "rank": "6",
		 "value": 6
		}, {
		 "rank": "7",
		 "value": 7
		}, {
		 "rank": "8",
		 "value": 8
		}, {
		 "rank": "9",
		 "value": 8
		}, {
		 "rank": "10",
		 "value": 10
		}, {
		 "rank": "J",
		 "value": 10
		}, {
		 "rank": "Q",
		 "value": 10
		}, {
		 "rank": "K",
		 "value": 10
		}]
		for suit in suits:
			for rank in ranks:  # Call Card class to fix value for each card.
				self.cards.append(Card(suit, rank))

	# Method to shuffle the deck as long as there are more than one card.
	def shuffle(self):
		if len(self.cards) > 1:
			random.shuffle(self.cards)

	# Deal a certain number of cards. The number is determined by the argument
	# 'number' passed to the method
	def deal(self, number):
		cards_dealt = []
		for x in range(number):
			# As long as there are cards left in the deck to be dealt
			if len(self.cards) > 0:
				card = self.cards.pop()
				cards_dealt.append(card)
		return cards_dealt


# A class to help in the process of dealing cards.
class Hand:
	# Dealer is false by default as later we might need to hide the cards drawn
	# by the dealer in the upcoming methods.
	def __init__(self, dealer=False):
		self.cards = []
		self.value = 0
		self.dealer = dealer

	# Add a list of drawn cards.
	def add_card(self, card_list):
		self.cards.extend(card_list)

	# Calculate the value of drawn cards
	def calculate_value(self):
		self.value = 0
		# Ace can be either 1 or 11 in value
		has_ace = False
		for card in self.cards:
			card_value = int(card.rank["value"])
			self.value += card_value
			if card.rank["rank"] == "A":
				has_ace = True

		# If we already have an ace and the calculated value has
		# crossed 21, we keep ace = 1
		if has_ace and self.value > 21:
			self.value -= 10

	# An interface that returns the value of drawn cards.
	def get_value(self):
		self.calculate_value()
		return self.value

	# Check if blackjack has occured.
	def is_blackjack(self):
		return self.get_value() == 21

	# Display dealer/player cards
	def display(self, show_all_dealer_cards=False):
		print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')

		# Enumerate returns the index and value(card).
		# Dealer's first card needa to be hidden.
		# If its the dealer's cards and Index = 0 (i.e., first card).
		for index, card in enumerate(self.cards):

			# Until its the final show or its blackjack, we hide
			# the dealer's first card.
			if index == 0 and self.dealer and \
   not show_all_dealer_cards and not self.is_blackjack():
				print("Hidden")
			else:
				# Print the card dealt
				print(card)

		# As Dealer's card is hidden total value is hidden
		if not self.dealer:
			print("Value:", self.get_value())
		print()


# A class for the actual game
#  and manipulation of the previously defined classes
class Game:

	def play(self):
		game_number = 0  #Current game we are in
		games_to_play = 0  #Total games
		while games_to_play <= 0:
			try:
				games_to_play = int(input("How many games do you want to play? "))
			except:
				print("You must enter a number.")

		while game_number < games_to_play:
			game_number += 1

			# Create a Deck instance and shuffle it.
			deck = Deck()
			deck.shuffle()

			# An instance for player and dealer respectively
			player_hand = Hand()
			dealer_hand = Hand(dealer=True)

			# Deal two cards each in round robin fashion to both player and dealer
			for i in range(2):
				player_hand.add_card(deck.deal(1))
				dealer_hand.add_card(deck.deal(1))

			print()
			print("*" * 30)
			print(f'Game {game_number} of {games_to_play}')
			print("*" * 30)
			player_hand.display()
			dealer_hand.display()

			# See if anyone has initially got a blackjack.
			# If so, go to the next game.
			# The result is announced either way in the check_winner() method.
			if self.check_winner(player_hand, dealer_hand):
				continue

			# Ask to hit or stand OR till value > 21
			choice = ""
			while player_hand.get_value() < 21 and choice not in ["s", "stand"]:
				choice = input("Please enter 'Hit' or 'Stand': ").lower()
				print()
				while choice not in ["s", "stand", "h", "hit"]:
					choice = input("Please enter 'Hit' or 'Stand' or(H/S)").lower()
					print()

				# Deal a card as hit option has been requested.
				# Then display the players cards
				if choice in ["h", "hit"]:
					player_hand.add_card(deck.deal(1))
					player_hand.display()

			# See if the player busted.
			if self.check_winner(player_hand, dealer_hand):
				continue

			player_hand_value = player_hand.get_value()
			dealer_hand_value = dealer_hand.get_value()

			# Deal till dealer has value over 17
			while dealer_hand_value < 17:
				dealer_hand.add_card(deck.deal(1))
				dealer_hand_value = dealer_hand.get_value()

			# Now finally display the dealer's hand as the play is at the end.
			dealer_hand.display(show_all_dealer_cards=True)

			# Check if the dealer bust.
			if self.check_winner(player_hand, dealer_hand):
				continue

			print("Final Results: ")
			print("Your hand:", player_hand_value)
			print("Dealer hand:", dealer_hand_value)

			# Check who the winner is.
			# Game over, hence pass True argument
			# Only now do we compare between player and dealer.
			self.check_winner(player_hand, dealer_hand, True)
		print("\nThanks for playing!")

	# Method that checks who won/busted or if it's a tie.
	def check_winner(self, player_hand, dealer_hand, game_over=False):

		# As long as game is not over, we only check for blackjacks and busts.
		# We don't check who has the better score.
		if not game_over:
			if player_hand.get_value() > 21:
				print("You busted. Dealer wins! ")
				return True
			elif dealer_hand.get_value() > 21:
				print("Dealer busted. You win! ")
				return True
			elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
				print("Both players have a blackjack! Tie!")
				return True
			elif player_hand.is_blackjack():
				print("You have a blackjack! You win!")
				return True
			elif dealer_hand.is_blackjack():
				print("Dealer has a blackjack! Dealer wins!")
				return True

		# Only when the game is over do we compare the dealer's and player's cards.
		else:
			if player_hand.get_value() > dealer_hand.get_value():
				print("You win!")
			elif player_hand.get_value() == dealer_hand.get_value():
				print("Its a tie!")
			else:
				print("Dealer wins.")
			return True
		return False


g = Game()
g.play()
