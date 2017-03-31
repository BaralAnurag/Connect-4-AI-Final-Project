import random

class Minimax(object):
    """ Minimax object that takes a current connect four play_board state
    """
    
    play_board = None
    coins  = ["x", "o"]
    
    def __init__(self, play_board):
        # copy the play_board to self.play_board
        self.play_board = [x[:] for x in play_board]
            
    def idealMove(self, depth, state, current_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        
        # determine opponent's color
        if current_player == self.coins [0]:
            opponent_player = self.coins [1]
        else:
            opponent_player = self.coins [0]
        
        # enumerate all legal moves
        allowable_moves = {} # will map legal move states to their alpha values
        for column in range(7):
            # if column i is a legal move...
            if self.isAllowableMove(column, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, column, current_player)
                allowable_moves[column] = -self.searchTree(depth-1, temp, opponent_player)

        ideal_move = None
        ideal_alpha = -10000000
                       
        moves = allowable_moves.items()
        
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= ideal_alpha:
                ideal_alpha = alpha
                ideal_move = move
        
        return  ideal_move, ideal_alpha
        
    def searchTree(self, depth, state, current_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the play_board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """
        
        # enumerate all legal moves from this state
        allowable_moves = []
        for i in range(7):
            # if column i is a legal move...
            if self.isAllowableMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, current_player)
                allowable_moves.append(temp)
        
        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(allowable_moves) == 0 or self.gameOver(state):
            # return the heuristic value of node
            return self.heuristic_eval(state, current_player)
        
        # determine opponent's color
        if current_player == self.coins [0]:
            opponent_player = self.coins [1]
        else:
            opponent_player = self.coins [0]

        alpha = -10000000
        for child in allowable_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.searchTree(depth-1, child, opponent_player))
        return alpha

    def isAllowableMove(self, game_column, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        
        for i in range(6):
            if state[i][game_column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True
        
        # if we get here, the column is full
        return False
    
    def gameOver(self, state):
        if self.consecutiveCoins(state, self.coins [0], 4) >= 1:
            return True
        elif self.consecutiveCoins(state, self.coins [1], 4) >= 1:
            return True
        else:
            return False
        
    
    def makeMove(self, state, game_column, coin):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
            
            Returns a copy of new state array with the added move
        """
        
        temp = [x[:] for x in state]
        for i in range(6):
            if temp[i][game_column] == ' ':
                temp[i][game_column] = coin
                return temp

    def heuristic_eval(self, state, coin):
        """ Simple heuristic to evaluate play_board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if coin == self.coins [0]:
            o_coin = self.coins [1]
        else:
            o_coin = self.coins [0]
        
        my_fours = self.consecutiveCoins(state, coin, 4)
        my_threes = self.consecutiveCoins(state, coin, 3)
        my_twos = self.consecutiveCoins(state, coin, 2)
        opp_fours = self.consecutiveCoins(state, o_coin, 4)
        
        if opp_fours > 0:
            return -100000
        else:
            return my_fours*100000 + my_threes*100 + my_twos
            
    def consecutiveCoins(self, state, coin, consecutive):
        count = 0
        # for each piece in the play_board...
        for i in range(6):
            for j in range(7):
                # ...that is of the color we're looking for...
                if state[i][j].lower() == coin.lower():
                    # check if a vertical streak starts at (i, j)
                    count += self.yCheck(i, j, state, consecutive)
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.xCheck(i, j, state, consecutive)
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self.zCheck(i, j, state, consecutive)
        # return the sum of streaks of length 'streak'
        return count
            
    def yCheck(self, row, column, state, consecutive):
        consecutiveCount = 0
        for i in range(row, 6):
            if state[i][column].lower() == state[row][column].lower():
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= consecutive:
            return 1
        else:
            return 0
    
    def xCheck(self, row, column, state, consecutive):
        consecutiveCount = 0
        for j in range(column, 7):
            if state[row][j].lower() == state[row][column].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= consecutive:
            return 1
        else:
            return 0
    
    def zCheck(self, row, column, state, consecutive):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][column].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
            
        if consecutiveCount >= consecutive:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = column
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][column].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount >= consecutive:
            total += 1

        return total
