#include <iostream>
#include <vector>
#include <array>
#include <algorithm>
#define GRID_SIZE 9

enum Play {
    None,
    X,
    O,
};

struct TicTacToeState {
    std::array<Play, GRID_SIZE> grid;
    Play turn;
    Play WinState;

    // Parameterized constructor
    TicTacToeState(const Play newgrid[], Play newturn)
        : turn(newturn), WinState(Play::None) {
        std::copy(newgrid, newgrid + GRID_SIZE, grid.begin());
    }

    // Default constructor
    TicTacToeState() : turn(Play::X), WinState(Play::None) {
        grid.fill(Play::None);  
    }
};

std::vector<TicTacToeState> get_next_states(TicTacToeState &state) {
    std::vector<TicTacToeState> next_states;
    for (int i = 0; i < GRID_SIZE; i++) {
        if (state.grid[i] == Play::None) { 
            TicTacToeState new_state = state;
            new_state.grid[i] = state.turn;
            new_state.turn = (state.turn == Play::O) ? Play::X : Play::O;
            next_states.push_back(new_state);
        }
    }
    return next_states;
}

void print_state(const TicTacToeState &state) {
    std::cout << "Grid:\n";
    for (int i = 0; i < GRID_SIZE; ++i) {
        std::cout << (state.grid[i] == Play::X ? "X" : state.grid[i] == Play::O ? "O" : ".");
        if ((i + 1) % 3 == 0) std::cout << '\n'; 
    }
    std::cout << "Turn: " << (state.turn == Play::X ? "X" : "O") << std::endl;
    std::cout << "WinState: " << (state.WinState == Play::X ? "X" : state.WinState == Play::O ? "O" : "None") << std::endl;
}

bool check_win(TicTacToeState &state) {
    int win_combos[8][3] = {
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},  // Rows
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},  // Columns
        {0, 4, 8}, {2, 4, 6}              // Diagonals
    };

    for (auto &combo : win_combos) {
        if (state.grid[combo[0]] != Play::None &&
            state.grid[combo[0]] == state.grid[combo[1]] &&
            state.grid[combo[1]] == state.grid[combo[2]]) {
            state.WinState = state.grid[combo[0]];
            return true;
        }
    }
    return false;
}

bool check_tie(TicTacToeState &state) {
    for (int i = 0; i < GRID_SIZE; i++) {
        if (state.grid[i] == Play::None) {
            return false;  // If there's an empty cell, it's not a tie
        }
    }
    return true;  // All cells are filled, so it's a tie
}

int evaluate(TicTacToeState &state) {
    if (check_win(state)) {
        return (state.WinState == Play::O) ? 1 : -1;
    }
    return 0;
}

std::pair<int, int> minimax_search(TicTacToeState &state, int depth, int depth_limit, int turn) {
    if (check_win(state) || check_tie(state) || depth == depth_limit) {
        return {evaluate(state), -1};
    }

    int best_score = (turn == 1) ? -2 : 2; // -2 and 2 are out of normal range (-1 to 1)
    int best_move = -1;

    for (int i = 0; i < GRID_SIZE; i++) {
        if (state.grid[i] == Play::None) {
            state.grid[i] = (turn == 1) ? Play::O : Play::X;
            int score = minimax_search(state, depth + 1, depth_limit, -turn).first;
            state.grid[i] = Play::None;

            if (turn == 1) {  
                if (score > best_score) {
                    best_score = score;
                    best_move = i;
                }
            } else {  // Minimizing for player (Play::X)
                if (score < best_score) {
                    best_score = score;
                    best_move = i;
                }
            }
        }
    }

    return {best_score, best_move};
}

void play_game() {
    std::cout << "Start the game:" << std::endl;
    TicTacToeState game_state;

    while (true) {
        print_state(game_state);

        // Human player's move
        int position_played;
        std::cout << "Choose your play (0-8): ";
        std::cin >> position_played;
        if (position_played < 0 || position_played >= GRID_SIZE || game_state.grid[position_played] != Play::None) {
            std::cout << "Invalid move. Try again." << std::endl;
            continue;
        }
        game_state.grid[position_played] = Play::X;
        if (check_win(game_state)) {
            game_state.WinState = Play::X;
            print_state(game_state);
            std::cout << "Player X wins!" << std::endl;
            break;
        }
        if (check_tie(game_state)) {
            print_state(game_state);
            std::cout << "It's a tie!" << std::endl;
            break;
        }

        // AI's move
        int value, position_ai;
        std::tie(value, position_ai) = minimax_search(game_state, 0, 10, 1);
        if (position_ai >= 0 && position_ai < GRID_SIZE) {  // Ensure AI move is valid
            game_state.grid[position_ai] = Play::O;
            if (check_win(game_state)) {
                game_state.WinState = Play::O;
                print_state(game_state);
                std::cout << "Player O wins!" << std::endl;
                break;
            }
            if (check_tie(game_state)) {
                print_state(game_state);
                std::cout << "It's a tie!" << std::endl;
                break;
            }
        } else {
            std::cout << "Error: AI could not find a valid move." << std::endl;
            break;
        }
    }
}

int main() {
    play_game();
    return 0;
}
