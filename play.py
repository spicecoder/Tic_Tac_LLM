def print_board(board):
    """Print the current state of the board"""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_win(board):
    """Check if a player has won"""
    # Define winning combinations (rows, columns, diagonals)
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
            return True
    return False

def check_tie(board):
    """Check if the game is a tie"""
    return " " not in board

def get_position(command):
    """Convert word command to board position index"""
    command_map = {
        "northwest": 0, "north": 1, "northeast": 2,
        "west": 3, "center": 4, "east": 5,
        "southwest": 6, "south": 7, "southeast": 8,
        "north-west": 0, "north-east": 2, 
        "south-west": 6, "south-east": 8
    }
    return command_map.get(command.lower().replace(" ", ""), -1)

def main():
    print("Welcome to Word-Based Tic-Tac-Toe!")
    print("Use these commands to play:")
    print("  1. reset    - Start a new game")
    print("  2. center   - Place mark in center")
    print("  3. north    - Place mark at top middle")
    print("  4. east     - Place mark at middle right")
    print("  5. south    - Place mark at bottom middle")
    print("  6. west     - Place mark at middle left")
    print("  7. north-west or northwest - Place mark at top left")
    print("  8. north-east or northeast - Place mark at top right")
    print("  9. south-west or southwest - Place mark at bottom left")
    print("  10. south-east or southeast - Place mark at bottom right")
    print("  11. quit    - End the game")
    
    board = [" " for _ in range(9)]
    current_player = "X"
    game_over = False
    
    print_board(board)
    
    while not game_over:
        command = input(f"Player {current_player}, enter your command: ")
        
        if command.lower() == "quit":
            print("Thanks for playing!")
            game_over = True
            continue
            
        if command.lower() == "reset":
            board = [" " for _ in range(9)]
            current_player = "X"
            print("Game reset!")
            print_board(board)
            continue
            
        position = get_position(command)
        
        if position == -1:
            print("Invalid command. Please try again.")
            continue
            
        if board[position] != " ":
            print("That position is already taken. Try another.")
            continue
            
        board[position] = current_player
        print_board(board)
        
        if check_win(board):
            print(f"Player {current_player} wins!")
            play_again = input("Play again? (yes/no): ")
            if play_again.lower() in ["yes", "y"]:
                board = [" " for _ in range(9)]
                current_player = "X"
                print("New game started!")
                print_board(board)
            else:
                print("Thanks for playing!")
                game_over = True
            continue
            
        if check_tie(board):
            print("It's a tie!")
            play_again = input("Play again? (yes/no): ")
            if play_again.lower() in ["yes", "y"]:
                board = [" " for _ in range(9)]
                current_player = "X"
                print("New game started!")
                print_board(board)
            else:
                print("Thanks for playing!")
                game_over = True
            continue
            
        # Switch player
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()