# Connect-4 AI
I built the game Connect 4 (More details about the rules can be found here: https://en.wikipedia.org/wiki/Connect_Four) in which the AI uses Game Tree based search to play against (and beat) a Myopic player (looks only one move ahead before choosing the best action). To run the game, run the PlayGame file (doesn't require any inputs).

## Some specifications of the program: 
1. The Myopic player always makes the first move.
2. The Game tree looks 5 moves ahead (i.e. game Tree has a cut-off depth of 5).
3. I experimented with multiple evaluation functions and compared their performance based on the number of games won (out of 50 games) and the average number of moves before each win.
4. The Minimax function is implemented with alpha-beta pruning to speed up the process.
5. A comparison between implementation with and without a move ordering heuristic has been shown.


## Uploads
### 2 code files are uploaded:
1. FourConnect: Outlines the gameplay and the Myopic Players' moves. Called in the PlayGame file. 
2. PlayGame: Implements Game Tree-based search to find out the best move for the AI and contains the main function to be run. 

### The report uploaded expands on the following points: 
1. Different evaluation functions used and their performance.
2. The move ordering heuristic used and the difference it makes to the performance.


A file outlining the methods and their functions used in the two code files has also been uploaded.


