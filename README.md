# Tic_Tac_LLM
##  tictacLLM.py    :This is the code accompanying the article in dev.to
https://dev.to/spicecoder/building-natural-language-command-interfaces-a-bridge-between-llms-and-deterministic-systems-1n4b



play.py is without the llm


## LLM -play Interactions :

The Complete Cycle
For each LLM turn:

We update the context with the human player's move

We add the current board state to the context

We send all previous messages plus the new context to the API

We receive the LLM's move selection

We parse that selection to a valid move

We add the LLM's response to the message history

We update the game board with the LLM's move

This message-based approach creates a continuous conversation context, allowing the LLM to have "memory" of previous game states and moves while ensuring it only makes valid moves within our deterministic game system.
