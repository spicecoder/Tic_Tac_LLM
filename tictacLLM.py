import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# Set up OpenAI API
# Note: You'll need to set your OPENAI_API_KEY as an environment variable
# or replace os.getenv("OPENAI_API_KEY") with your actual API key
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI()

def print_board(board):
    """Print the current state of the board"""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def board_state_text(board):
    """Return a text representation of the board for the LLM"""
    return f"""
 {board[0]} | {board[1]} | {board[2]} 
---+---+---
 {board[3]} | {board[4]} | {board[5]} 
---+---+---
 {board[6]} | {board[7]} | {board[8]} 
"""

def check_win(board):
    """Check if a player has won"""
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
    return command_map.get(command.lower().replace(" ", "").replace("-", ""), -1)

def get_position_name(index):
    """Convert board position index to command name"""
    position_names = {
        0: "north-west", 1: "north", 2: "north-east",
        3: "west", 4: "center", 5: "east",
        6: "south-west", 7: "south", 8: "south-east"
    }
    return position_names.get(index, "unknown")

def get_llm_move(board, messages):
    """Get a move from the LLM"""
    # Create a list of available moves
    available_moves = []
    for i in range(9):
        if board[i] == " ":
            available_moves.append(get_position_name(i))
    
    # Update context with the current board state and available moves
    current_state = f"""
Current board state:
{board_state_text(board)}

Available moves: {', '.join(available_moves)}

As the O player, your goal is to get three O's in a row (horizontally, vertically, or diagonally).
Choose one of the available positions by responding with only the position name (e.g., "center", "north-west", etc.).
"""
    
    # Add current state to messages
    messages.append({"role": "user", "content": current_state})
    
    print("LLM is thinking...")
    
    # Get response from LLM
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use "gpt-4" for better gameplay
        messages=messages,
        max_tokens=50,
        temperature=0.7
    )
    
    llm_response = response.choices[0].message.content.strip().lower()
    messages.append({"role": "assistant", "content": llm_response})
    
    # Extract just the command from potential verbose response
    for move in available_moves:
        if move in llm_response or move.replace("-", "") in llm_response:
            return move
    
    # If no valid move found in response, try to make a fallback move
    print(f"LLM response: '{llm_response}' not recognized as a valid move. Making a fallback move.")
    if available_moves:
        return available_moves[0]
    return None

def main():
    print("Welcome to Word-Based Tic-Tac-Toe vs. LLM!")
    print("You are X, and the LLM is O.")
    print("Use these commands to play:")
    print("  1. reset    - Start a new game")
    print("  2. center   - Place mark in center")
    print("  3. north    - Place mark at top middle")
    print("  4. east     - Place mark at middle right")
    print("  5. south    - Place mark at bottom middle")
    print("  6. west     - Place mark at middle left")
    print("  7. north-west - Place mark at top left")
    print("  8. north-east - Place mark at top right")
    print("  9. south-west - Place mark at bottom left")
    print("  10. south-east - Place mark at bottom right")
    print("  11. quit    - End the game")
    
    # Initialize LLM context with system prompt
    messages = [
        {"role": "system", "content": """
You are playing a word-based tic-tac-toe game. You are player O.
The board positions are:

north-west (top-left) | north (top-middle) | north-east (top-right)
-----------------+------------------+-------------------
west (middle-left) | center (middle) | east (middle-right)
-----------------+------------------+-------------------
south-west (bottom-left) | south (bottom-middle) | south-east (bottom-right)

When it's your turn, respond with ONLY the position where you want to place your O.
For example, if you want to place your O in the center, respond with "center".
Be strategic and try to win by getting three O's in a row, column, or diagonal.
Block the human player (X) when they have two X's in a row.
"""
        }
    ]
    
    board = [" " for _ in range(9)]
    game_over = False
    
    print_board(board)
    
    while not game_over:
        # Human player's turn (X)
        command = input("Your turn (X). Enter your command: ")
        
        if command.lower() == "quit":
            print("Thanks for playing!")
            game_over = True
            continue
            
        if command.lower() == "reset":
            board = [" " for _ in range(9)]
            messages = [messages[0]]  # Keep only the system message
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
            
        # Update board with human move
        board[position] = "X"
        
        # Add human move to context
        move_desc = f"Human player placed X at {get_position_name(position)}."
        messages.append({"role": "user", "content": move_desc})
        
        print_board(board)
        
        # Check if human player won
        if check_win(board):
            print("You win!")
            play_again = input("Play again? (yes/no): ")
            if play_again.lower() in ["yes", "y"]:
                board = [" " for _ in range(9)]
                messages = [messages[0]]  # Keep only the system message
                print("New game started!")
                print_board(board)
            else:
                print("Thanks for playing!")
                game_over = True
            continue
            
        # Check for tie
        if check_tie(board):
            print("It's a tie!")
            play_again = input("Play again? (yes/no): ")
            if play_again.lower() in ["yes", "y"]:
                board = [" " for _ in range(9)]
                messages = [messages[0]]  # Keep only the system message
                print("New game started!")
                print_board(board)
            else:
                print("Thanks for playing!")
                game_over = True
            continue
        
        # LLM player's turn (O)
        print("\nLLM's turn (O)...")
        llm_command = get_llm_move(board, messages)
        
        if llm_command:
            position = get_position(llm_command)
            board[position] = "O"
            print(f"LLM placed O at {llm_command}.")
            print_board(board)
            
            # Check if LLM player won
            if check_win(board):
                print("LLM wins!")
                play_again = input("Play again? (yes/no): ")
                if play_again.lower() in ["yes", "y"]:
                    board = [" " for _ in range(9)]
                    messages = [messages[0]]  # Keep only the system message
                    print("New game started!")
                    print_board(board)
                else:
                    print("Thanks for playing!")
                    game_over = True
                continue
                
            # Check for tie
            if check_tie(board):
                print("It's a tie!")
                play_again = input("Play again? (yes/no): ")
                if play_again.lower() in ["yes", "y"]:
                    board = [" " for _ in range(9)]
                    messages = [messages[0]]  # Keep only the system message
                    print("New game started!")
                    print_board(board)
                else:
                    print("Thanks for playing!")
                    game_over = True
                continue

if __name__ == "__main__":
    main()