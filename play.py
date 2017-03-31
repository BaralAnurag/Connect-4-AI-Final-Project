from connect4 import *



def main():
   """ Play a game!
   """


   g = ConnectFourGame()
   g.printState()
   player1 = g.game_players[0]
   player2 = g.game_players[1]



   exit = False
   while not exit:
       while not g.game_end:
           g.nextMove()


       g.printState()

       while True:
           play_again = str(input("Would you like to lose again? "))


           if play_again.lower() == 'yes' or play_again.lower() == 'yes':
               g.resetGame()
               g.printState()
               break
           elif play_again.lower() == 'no' or play_again.lower() == 'no':
               print("Thanks for losing!")
               exit = True
               break
           else:
               print("That is not an option human scum."),



if __name__ == "__main__":  #main method
   main()


