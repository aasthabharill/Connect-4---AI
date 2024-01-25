from FourConnect import * # See the FourConnect.py file
import csv
import math
from random import shuffle
import time

HUMAN_PLAYER = 1
AI_PLAYER    = 2

class GameTreePlayer:    
    
    def __init__(self):
        pass
    
    
    def makeMove(self, board, col, player):
        tempBoard = [row[:] for row in board]
        for row in range(5, -1, -1):
            if tempBoard[row][col] == 0:
                tempBoard[row][col] = player
                return tempBoard, row, col
        
        # Return the original board if the move is not valid
        return board, -1, -1
    
    
    def get_valid_locations(self,currentState):
        valid_locations = []
        for c in range(7):
            if currentState[0][c] == 0:
                valid_locations.append(c)

        return valid_locations

    
    def winning_move(self,currentState, player):
        # Check verticals
        for c in range(7): 
            count = 0
            for r in range(6):
                if currentState[r][c] == player:
                    count += 1
                else:
                    count = 0
                    
                if count >= 4:
                    return True
                
        #check horizontals
        for r in range(6): 
            count = 0
            for c in range(7):
                if currentState[r][c] == player:
                    count += 1
                else:
                    count = 0
                    
                if count >= 4:
                    return True
                
        # Check positively sloped diaganols
        for r in range(6): 
            for c in range(7):
                count = 0
                colIndex = c
                for rowIndex in range(r, 6):
                    if colIndex > 6:
                        break
                    elif currentState[rowIndex][colIndex] == player:
                        count += 1
                    else:
                        break
                    colIndex += 1 

                if count >= 4:
                    return True

        # Check negatively sloped diaganols
        for c in range(7-3):
            for r in range(3, 6):
                count = 0
                colIndex = c
                for rowIndex in range(r, -1, -1):
                    if colIndex > 6:
                        break
                    elif currentState[rowIndex][colIndex] == player:
                        count += 1
                    else:
                        break
                    colIndex += 1 

                if count >= 4:
                    return True  
                
        return False

    
    def is_terminal_node(self,currentState):
        valid_loc = self.get_valid_locations(currentState)
    
        if len(valid_loc) == 0:                                  #no valid moves left - board full
            return True
        elif self.winning_move(currentState, AI_PLAYER) or self.winning_move(currentState, HUMAN_PLAYER):
            return True
        else:
            return False

    
    # Experimented with different evaluation functions, uncomment them to see results
    def evaluation(self,window, player = AI_PLAYER):
        score = 0
        opp_player = HUMAN_PLAYER
        if player == HUMAN_PLAYER:
            opp_player = AI_PLAYER

        #Evaluation 1 - window has pieces of only the player (can have empty cells).
        if window.count(player) == 4:
            score += 1000000000
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 100
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 1
            
        if window.count(opp_player) == 4:
            score -= 10000000000
        
        return score
    
        
        # # Evaluation 2 - same as above but subtract the number of windows where the opponent could win. 
        # if window.count(player) == 4:
        #     score += 1000000000
        # elif window.count(player) == 3 and window.count(0) == 1:
        #     score += 1
        # elif window.count(player) == 2 and window.count(0) == 2:
        #     score += 1
        # elif window.count(player) == 1 and window.count(0) == 3:
        #     score += 1
            
        # if window.count(opp_player) == 4:
        #     score -= 10000000000
        # if window.count(opp_player) == 3 and window.count(0) == 1:
        #     score -= 1
        # elif window.count(opp_player) == 2 and window.count(0) == 2:
        #     score -= 1
        # elif window.count(opp_player) == 1 and window.count(0) == 3:
        #     score -= 1
        # return score
        
        
        # #Evaluation 4 -  positive weight to winning, negative weight to losing and 0 otherwise.

        # if window.count(player) == 4:
        #     score += 10000
            
        # if window.count(opp_player) == 4:
        #     score -= 10000
        # return score


    def utilityValue(self, currentState, player = AI_PLAYER):
        score = 0

        # Score Horizontal
        for r in range(6):
            for c in range(7-3):
                window = [int(currentState[r][j]) for j in range(c, c+4)]
                score += self.evaluation(window, player)

        # Score Vertical
        for c in range(7):
            col_array = [int(row[c]) for row in currentState]
            for r in range(6 - 3):
                window = col_array[r:r + 4]
                score += self.evaluation(window, player)

        # Score positively sloped diagonals
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [currentState[r + i][c + i] for i in range(4)]
                score += self.evaluation(window, player)

        # Score negatively sloped diagonals
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [currentState[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluation(window, player)

        return score

    def count_winning_positions(self, currentState, player):
        winning_positions = 0

        for r in range(6):
            for c in range(7):
                if currentState[r][c] == player:
                    # Check horizontal winning positions
                    if c + 3 < 7 and currentState[r][c + 1] == player and currentState[r][c + 2] == player and currentState[r][c + 3] == 0:
                        winning_positions += 1
                    # Check vertical winning positions
                    if r + 3 < 6 and currentState[r + 1][c] == player and currentState[r + 2][c] == player and currentState[r + 3][c] == 0:
                        winning_positions += 1
                    # Check positively sloped diagonal winning positions
                    if r + 3 < 6 and c + 3 < 7 and currentState[r + 1][c + 1] == player and currentState[r + 2][c + 2] == player and currentState[r + 3][c + 3] == 0:
                        winning_positions += 1
                    # Check negatively sloped diagonal winning positions
                    if r - 3 >= 0 and c + 3 < 7 and currentState[r - 1][c + 1] == player and currentState[r - 2][c + 2] == player and currentState[r - 3][c + 3] == 0:
                        winning_positions += 1

        return winning_positions
    
    def winning_positions_heuristic(self, currentState, move, player):
        tempBoard = self.makeMove(currentState, move, player)[0]
        return self.count_winning_positions(tempBoard, player)


    def minimizeBeta(self,currentState, depth, alpha, beta, player, opponent):
        
        validMoves = self.get_valid_locations(currentState)
        if depth == 0 or len(validMoves) == 0 or self.is_terminal_node(currentState):
            return self.utilityValue(currentState, player)
        
        for move in validMoves:
            boardScore = float("inf")
            if alpha < beta:
                tempBoard = self.makeMove(currentState, move, opponent)[0]
                boardScore = self.maximizeAlpha(tempBoard, depth - 1, alpha, beta, player, opponent)

            if boardScore < beta:
                beta = boardScore
            if alpha >= beta:
                break
        
        return beta

    def maximizeAlpha(self,currentState, depth, alpha, beta, player, opponent):
        
        validMoves = self.get_valid_locations(currentState) 
        if depth == 0 or len(validMoves) == 0 or self.is_terminal_node(currentState):
            return self.utilityValue(currentState, player)
     
        for move in validMoves:
            boardScore = float("-inf")
            if alpha < beta:
                tempBoard = self.makeMove(currentState, move, player)[0]
                boardScore = self.minimizeBeta(tempBoard, depth - 1, alpha, beta, player, opponent)

            if boardScore > alpha:
                alpha = boardScore
                
            if alpha >= beta:
                break
            
        return alpha
                
    
    def MiniMaxAlphaBeta(self, currentState, depth, player = AI_PLAYER):
        
        if player == AI_PLAYER: 
            opponent = HUMAN_PLAYER
        else: 
            opponent = AI_PLAYER
            
        alpha = float("-inf")
        beta = float("inf")
            
        validMoves = self.get_valid_locations(currentState)
        
        # without move ordering - commented out
        shuffle(validMoves)
        # bestMove  = validMoves[0]
        
        # with move ordering heuristic 
        ordered_moves = sorted(validMoves, key=lambda move: self.winning_positions_heuristic(currentState, move, player), reverse=True)
        bestMove = ordered_moves[0]
        bestScore = float("-inf")
    
        for move in validMoves:
            tempBoard = self.makeMove(currentState, move, player)[0]
            boardScore = self.minimizeBeta(tempBoard, depth - 1, alpha, beta, player, opponent)
            if boardScore > bestScore:
                bestScore = boardScore
                bestMove = move
        return bestMove


    def FindBestAction(self, currentState):
        depth = 5
        bestAction = self.MiniMaxAlphaBeta(currentState,depth,AI_PLAYER)  
        return bestAction


def PlayGame():
    fourConnect = FourConnect()
    # fourConnect.PrintGameState()
    gameTree = GameTreePlayer()
    
    move=0
    while move<42: #At most 42 moves are possible
        if move%2 == 0: #Myopic player always moves first
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        # fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    if fourConnect.winner==None:
        print("Game is drawn.")
    else:
        print("Winner : Player {0}".format(fourConnect.winner))
    print("Moves : {0}".format(move))
    
    return move,fourConnect.winner
    

def main():
    # PlayGame()
    start = time.time()
    total_moves = 0
    ai_wins = 0

    for i in range(50):
        print("Game {0}".format(i+1))
        moves, winner = PlayGame()

        total_moves += moves

        if winner == AI_PLAYER:
            ai_wins += 1
        
        print("\n")

    average_moves = total_moves / 50

    print("Average Number of Moves: {:.2f}".format(average_moves))
    print("AI_PLAYER Wins: {}/50".format(ai_wins))
    end = time.time()
    print("The time of execution of above program is :",(end-start) * 10**3, "ms")
    


if __name__=='__main__':
    main()
