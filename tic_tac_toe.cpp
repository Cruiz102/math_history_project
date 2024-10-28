#include <iostream>
#include <vector>
#include <bitset>
#include <array>
#include <cstring>
#define GRID_SIZE 9

enum Play {
    None,
    X,
    O,
};

struct TicTacToeState {
    std::array<int, GRID_SIZE> grid;
    Play turn;
    Play WinState;

    // Parameterized constructor
    TicTacToeState(const int newgrid[], Play newturn)
        : turn(newturn), WinState(Play::None) {
        std::copy(newgrid, newgrid + GRID_SIZE, grid.begin());
    }

    // Default constructor
    TicTacToeState() : turn(Play::X), WinState(Play::None) {
        grid.fill(0);  
    }
};

struct ActionState {
    TicTacToeState state;
    std::bitset<GRID_SIZE> actions;
};

std::vector<ActionState> get_next_action_states(TicTacToeState &state) {
    std::vector<ActionState> action_states;
    for (int i = 0; i < GRID_SIZE; i++) {
        if (state.grid[i] == 0) { 
            ActionState action_state;
            TicTacToeState new_state = state;
            new_state.grid[i] = state.turn;  
            action_state.state = new_state;
            action_state.actions.set(i);     
            action_states.push_back(action_state);
        }
    }
    return action_states;
}



void print_state(const TicTacToeState &state) {
    std::cout << "Grid: ";
    for (int i = 0; i < GRID_SIZE; ++i) {
        std::cout << state.grid[i] << ' ';
        if ((i + 1) % 3 == 0) std::cout << '\n'; 
    }
    std::cout << "Turn: " << (state.turn == Play::X ? "X" : "O") << std::endl;
    std::cout << "WinState: " << (state.WinState == Play::X ? "X" : state.WinState == Play::O ? "O" : "None") << std::endl;
}



void change_win_state(TicTacToeState &state) {
    int win_combos[8][3] = {
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},  // Rows
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},  // Columns
        {0, 4, 8}, {2, 4, 6}              // Diagonals
    };

    for (auto &combo : win_combos) {
        if (state.grid[combo[0]] == state.turn &&
            state.grid[combo[1]] == state.turn &&
            state.grid[combo[2]] == state.turn) {
            state.WinState = state.turn;
            print_state(state);
            
            return;
        }
    }
}


void generate_all_tabular_states() {
    TicTacToeState initial_state;
    std::vector<TicTacToeState> game_stack;
    game_stack.push_back(initial_state);
    int count = 0;
    while (!game_stack.empty()) {
        std::cout << count++ << std::endl;
        TicTacToeState curr_state = game_stack.back();
        game_stack.pop_back();
        
        print_state(curr_state);
        std::vector<ActionState> act_states = get_next_action_states(curr_state);
        for (ActionState &act_state : act_states) {
            change_win_state(act_state.state);
            if (act_state.state.WinState == Play::None) {
                game_stack.push_back(act_state.state);
            }
        }
    }
}

int dfs_traverse(ActionState& action_state){
    change_win_state(action_state.state);
    if(action_state.actions.all()){
        return Play::None;
    }
    if(action_state.state.WinState != Play::None){
        return action_state.state.WinState;
    }
    std::vector<ActionState> childrens =  get_next_action_states(action_state.state);
    for(int i = 0; i < childrens.size(); i++){
        dfs_traverse(childrens[i]);
    }
    return -1;
}
void perfect_tree_search(TicTacToeState &state){
    std::vector<ActionState> childrens =  get_next_action_states(state);
    for( ActionState& action_state: childrens){
        int result  = dfs_traverse(action_state);
        if(result == Play::X){
            std::cout << "Best Play for X" << std::endl;
        }

        if(result == Play::O){
            std::cout << "Best Play for O" << std::endl;
        }
        else{
            std::cout << "It will end at draw" << std::endl;
        }
    }
}

int main() {
    generate_all_tabular_states();
    return 0;
}
