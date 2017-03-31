

class InputPrompts(object):

   
   game_winner = None #the winner of the game
   player_turn = None # keeps track of whose turn it is
   game_players = [None, None] # current players
   play_board = None # the current board state
   plays = None # number of plays made
   game_end = None # boolean for if the game is over 
   coins = ["X", "O"]


   def __init__(self):  
       self.game_end = False
       self.game_winner = None
       self.plays = 1

       print("ARE YOU READY TO LOSE AT CONNECT FOUR!")  # the display message
       print("Choose a Player. You can choose between Computer or Human?")


       while self.game_players[0] == None:
           options = str(input("Type 'Human' or 'Computer': "))
           if options == "Human" or options.lower() == "human":
               name = str(input("What should we call this player? "))
               self.game_players[0] = GamePlayer(name, self.coins [0])
           elif options == "Computer" or options.lower() == "computer":
               name = str(input("What should we call this player? "))
               diff = int(input("How deep do you want to search?  "))
               self.game_players[0] = AI(name, self.coins [0], diff)
           else:
               print("Invalid options, please try again")
       print("{0} will be {1}".format(self.game_players[0].name, self.coins [0]))


       print("Should Player 2 be a Human or a Computer?")
       while self.game_players[1] == None:
           options = str(input("Type 'Human' or 'Computer': "))
           if options == "Human" or options.lower() == "human":
               name = str(input("What should we call this player? "))
               self.game_players[1] = GamePlayer(name, self.coins [1])
           elif options == "Computer" or options.lower() == "computer":
               name = str(input("What should we call this player? "))
               diff = int(input("How deep do you want to search? "))
               self.game_players[1] = AI(name, self.coins [1], diff)
           else:
               print("You are bad at connect 4. Try again with a valid move")
       print("{0} will be {1}".format(self.game_players[1].name, self.coins [1]))


       # x always goes first (arbitrary options on my part)
       self.player_turn = self.game_players[0]


       self.play_board = []
       for i in range(6):
           self.play_board.append([])
           for j in range(7):
               self.play_board[i].append(' ')


