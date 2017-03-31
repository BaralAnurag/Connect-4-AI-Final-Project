from minimax import Minimax
import time
import random





class ConnectFourGame(object):
   """ Game object that holds state of Connect 4 play_board and game values
   """
   
   
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




   def resetGame(self):
       """ Function to reset the game, but not the names or coins 
       """
       self.plays = 1
       self.game_end = False
       self.game_winner = None


       # x always goes first (arbitrary options on my part)
       self.player_turn = self.game_players[0]


       self.play_board = []
       for i in range(6):
           self.play_board.append([])
           for j in range(7):
               self.play_board[i].append(' ')


   def alternateTurns(self):
       if self.player_turn == self.game_players[0]:
           self.player_turn = self.game_players[1]
       else:
           self.player_turn = self.game_players[0]


       # increment the plays
       self.plays += 1


   def nextMove(self):
       player = self.player_turn
   
       # there are only 42 legal places for pieces on the play_board
       # exactly one piece is added to the play_board each turn
       if self.plays > 42:
           self.game_end = True
           # this would be a stalemate :(
           return


       # move is the column that player want's to play
       move = player.move(self.play_board)


       for i in range(6):
           if self.play_board[i][move] == ' ':
               self.play_board[i][move] = player.coins
               self.alternateTurns()
               self.confirmFours()
               self.printState()
               return


       # if we get here, then the column is full
       print("Invalid move (column is full)")
       return


 
   def confirmFours(self):
       # for each piece in the play_board...
       for i in range(6):
           for j in range(7):
               if self.play_board[i][j] != ' ':
                   # check if a vertical four-in-a-row starts at (i, j)
                   if self.confirmVertical(i, j):
                       self.game_end = True
                       return


                   # check if a horizontal four-in-a-row starts at (i, j)
                   if self.confirmHorizontal(i, j):
                       self.game_end = True
                       return


                   # check if a diagonal (either way) four-in-a-row starts at (i, j)
                   # also, get the slope of the four if there is one
                   diag_fours, slope = self.confirmDiagonal(i, j)
                   if diag_fours:
                       print(slope)
                       self.game_end = True
                       return


   def confirmVertical(self, row, column):
       # print("checking vert")
       fourInARow = False
       consecutiveCount = 0


       for i in range(row, 6):
           if self.play_board[i][column].lower() == self.play_board[row][column].lower():
               consecutiveCount += 1
           else:
               break


       if consecutiveCount >= 4:
           fourInARow = True
           if self.game_players[0].coins.lower() == self.play_board[row][column].lower():
               self.game_winner = self.game_players[0]
           else:
               self.game_winner = self.game_players[1]


       return fourInARow


   def confirmHorizontal(self, row, column):
       fourInARow = False
       consecutiveCount = 0


       for j in range(column, 7):
           if self.play_board[row][j].lower() == self.play_board[row][column].lower():
               consecutiveCount += 1
           else:
               break


       if consecutiveCount >= 4:
           fourInARow = True
           if self.game_players[0].coins.lower() == self.play_board[row][column].lower():
               self.game_winner = self.game_players[0]
           else:
               self.game_winner = self.game_players[1]


       return fourInARow


   def confirmDiagonal(self, row, column):
       fourInARow = False
       count = 0
       slope = None


       # check for diagonals with positive slope
       consecutiveCount = 0
       j = column
       for i in range(row, 6):
           if j > 6:
               break
           elif self.play_board[i][j].lower() == self.play_board[row][column].lower():
               consecutiveCount += 1
           else:
               break
           j += 1  # increment column when row is incremented


       if consecutiveCount >= 4:
           count += 1
           slope = 'positive'
           if self.game_players[0].coins.lower() == self.play_board[row][column].lower():
               self.game_winner = self.game_players[0]
           else:
               self.game_winner = self.game_players[1]


       # check for diagonals with negative slope
       consecutiveCount = 0
       j = column
       for i in range(row, -1, -1):
           if j > 6:
               break
           elif self.play_board[i][j].lower() == self.play_board[row][column].lower():
               consecutiveCount += 1
           else:
               break
           j += 1  # increment column when row is decremented


       if consecutiveCount >= 4:
           count += 1
           slope = 'negative'
           if self.game_players[0].coins.lower() == self.play_board[row][column].lower():
               self.game_winner = self.game_players[0]
           else:
               self.game_winner = self.game_players[1]


       if count > 0:
           fourInARow = True
       if count == 2:
           slope = 'both'
       return fourInARow, slope




   def printState(self):
       
       print("plays: " + str(self.plays))
       print("\t  1   2   3   4   5   6   7 ")
       print("\t____________________________")
       for i in range(5, -1, -1):
           print("\t", end="")
           for j in range(7):
               print("| " + str(self.play_board[i][j]), end=" ")
           print("|")
       print("\t____________________________")
       print("\t  1   2   3   4   5   6   7 ")
       print("=========================================")
       


       if self.game_end:
           print("Game Over...")
           if self.game_winner != None:
               print(str(self.game_winner.name) + " has won.")
           else:
               print("No Winner.")




class GamePlayer(object):
   """ Player object.  This class is for human game_players.
   """
   type = None  # possible types are "Human" and "AI"
   name = None
   coins = None


   def __init__(self, name, coins):
       self.type = "Human"
       self.name = name
       self.coins = coins


   def move(self, state):
       print("{0}'s turn.  {0} is {1}".format(self.name, self.coins))
       game_column = None
       while game_column == None:
           try:
               options = int(input("Enter a move (by column number): ")) - 1
           except ValueError:
               options = None
           if 0 <= options <= 6:
               game_column = options
           else:
               print("Invalid options, try again")
       return game_column




class AI(GamePlayer):
   """ AIPlayer object that extends Player
       The AI algorithm is minimax, the difficulty parameter is the depth to which
       the search tree is expanded.
   """


   difficulty = None


   def __init__(self, name, coins, difficulty):
       self.type = "AI"
       self.name = name
       self.coins = coins
       self.difficulty = difficulty


   def move(self, state):
       print("{0}'s turn.  {0} is {1}".format(self.name, self.coins))


       # sleeping for about 1 second makes it looks like he's thinking
       # time.sleep(random.randrange(8, 17, 1)/10.0)
       # return random.randint(0, 6)


       miniMaxUse = Minimax(state)
       ideal_move, heuristic_eval = miniMaxUse.idealMove(self.difficulty, state, self.coins)
       return ideal_move




