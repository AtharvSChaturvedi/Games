import pygame
import sys
from collections import deque
import copy

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 400
BOARD_SIZE = 300
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = BOARD_SIZE // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (52, 152, 219)
BUTTON_HOVER = (41, 128, 185)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe AI - Search Algorithms')
screen.fill(BG_COLOR)

# Font
font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 16)

class TicTacToe:
    def __init__(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.ai_algorithm = 'BFS'
        self.search_stats = {'nodes_explored': 0, 'time': 0}
        
    def draw_lines(self):
        # Horizontal lines
        for row in range(1, BOARD_ROWS):
            pygame.draw.line(screen, LINE_COLOR, 
                           (0, row * SQUARE_SIZE), 
                           (BOARD_SIZE, row * SQUARE_SIZE), 
                           LINE_WIDTH)
        # Vertical lines
        for col in range(1, BOARD_COLS):
            pygame.draw.line(screen, LINE_COLOR, 
                           (col * SQUARE_SIZE, 0), 
                           (col * SQUARE_SIZE, BOARD_SIZE), 
                           LINE_WIDTH)
    
    def draw_figures(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 'O':
                    pygame.draw.circle(screen, CIRCLE_COLOR, 
                                     (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                      int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 
                                     CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board[row][col] == 'X':
                    pygame.draw.line(screen, CROSS_COLOR, 
                                   (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                   (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), 
                                   CROSS_WIDTH)
                    pygame.draw.line(screen, CROSS_COLOR, 
                                   (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                   (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                   CROSS_WIDTH)
    
    def mark_square(self, row, col, player):
        if self.board[row][col] is None:
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self, board=None):
        if board is None:
            board = self.board
            
        # Check rows
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
                return board[row][0]
        
        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
                return board[0][col]
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2]
        
        # Check for draw
        if all(board[row][col] is not None for row in range(3) for col in range(3)):
            return 'Draw'
        
        return None
    
    def get_available_moves(self, board):
        moves = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    moves.append((row, col))
        return moves
    
    def bfs_search(self, board, player):
        """BFS implementation for game tree exploration"""
        import time
        start_time = time.time()
        nodes_explored = 0
        
        queue = deque()
        available_moves = self.get_available_moves(board)
        
        if not available_moves:
            return None
        
        # Evaluate each immediate move
        best_move = available_moves[0]
        best_score = -float('inf')
        
        for move in available_moves:
            row, col = move
            new_board = copy.deepcopy(board)
            new_board[row][col] = player
            nodes_explored += 1
            
            # Check immediate win
            winner = self.check_winner(new_board)
            if winner == player:
                self.search_stats = {
                    'nodes_explored': nodes_explored,
                    'time': time.time() - start_time
                }
                return move
            
            # BFS evaluation
            queue.append((new_board, move, 1))
        
        opponent = 'X' if player == 'O' else 'O'
        move_scores = {move: 0 for move in available_moves}
        
        while queue:
            current_board, original_move, depth = queue.popleft()
            
            if depth > 3:  # Limit depth for BFS
                continue
            
            winner = self.check_winner(current_board)
            if winner == player:
                move_scores[original_move] += (10 - depth)
            elif winner == opponent:
                move_scores[original_move] -= (10 - depth)
            elif winner is None:
                next_moves = self.get_available_moves(current_board)
                for next_move in next_moves:
                    r, c = next_move
                    new_board = copy.deepcopy(current_board)
                    new_board[r][c] = opponent if depth % 2 == 1 else player
                    queue.append((new_board, original_move, depth + 1))
                    nodes_explored += 1
        
        best_move = max(move_scores, key=move_scores.get)
        self.search_stats = {
            'nodes_explored': nodes_explored,
            'time': time.time() - start_time
        }
        return best_move
    
    def dfs_search(self, board, player):
        """DFS implementation for game tree exploration"""
        import time
        start_time = time.time()
        nodes_explored = 0
        
        available_moves = self.get_available_moves(board)
        
        if not available_moves:
            return None
        
        best_move = available_moves[0]
        best_score = -float('inf')
        opponent = 'X' if player == 'O' else 'O'
        
        def dfs_helper(current_board, depth, is_maximizing):
            nonlocal nodes_explored
            nodes_explored += 1
            
            winner = self.check_winner(current_board)
            
            if winner == player:
                return 10 - depth
            elif winner == opponent:
                return depth - 10
            elif winner == 'Draw':
                return 0
            
            if depth >= 4:  # Limit depth
                return 0
            
            moves = self.get_available_moves(current_board)
            
            if is_maximizing:
                max_score = -float('inf')
                for move in moves:
                    r, c = move
                    new_board = copy.deepcopy(current_board)
                    new_board[r][c] = player
                    score = dfs_helper(new_board, depth + 1, False)
                    max_score = max(max_score, score)
                return max_score
            else:
                min_score = float('inf')
                for move in moves:
                    r, c = move
                    new_board = copy.deepcopy(current_board)
                    new_board[r][c] = opponent
                    score = dfs_helper(new_board, depth + 1, True)
                    min_score = min(min_score, score)
                return min_score
        
        for move in available_moves:
            row, col = move
            new_board = copy.deepcopy(board)
            new_board[row][col] = player
            score = dfs_helper(new_board, 1, False)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        self.search_stats = {
            'nodes_explored': nodes_explored,
            'time': time.time() - start_time
        }
        return best_move
    
    def heuristic(self, board, player):
        """Heuristic function for A* search"""
        opponent = 'X' if player == 'O' else 'O'
        score = 0
        
        # Check all winning patterns
        patterns = [
            # Rows
            [(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)],
            # Columns
            [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)],
            # Diagonals
            [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]
        ]
        
        for pattern in patterns:
            player_count = sum(1 for r, c in pattern if board[r][c] == player)
            opponent_count = sum(1 for r, c in pattern if board[r][c] == opponent)
            empty_count = sum(1 for r, c in pattern if board[r][c] is None)
            
            if opponent_count == 0:
                score += player_count ** 2
            if player_count == 0:
                score -= opponent_count ** 2
        
        return score
    
    def astar_search(self, board, player):
        """A* implementation with heuristic function"""
        import time
        import heapq
        start_time = time.time()
        nodes_explored = 0
        
        available_moves = self.get_available_moves(board)
        
        if not available_moves:
            return None
        
        opponent = 'X' if player == 'O' else 'O'
        best_move = available_moves[0]
        best_score = -float('inf')
        
        for move in available_moves:
            row, col = move
            new_board = copy.deepcopy(board)
            new_board[row][col] = player
            nodes_explored += 1
            
            # Check immediate win
            winner = self.check_winner(new_board)
            if winner == player:
                self.search_stats = {
                    'nodes_explored': nodes_explored,
                    'time': time.time() - start_time
                }
                return move
            
            # A* evaluation
            g_cost = 1  # Depth
            h_cost = self.heuristic(new_board, player)
            f_cost = g_cost + h_cost
            
            # Priority queue: (f_cost, counter, g_cost, board, move)
            # Counter prevents comparison of board states
            counter = 0
            pq = [(f_cost, counter, g_cost, new_board, move)]
            move_score = h_cost
            
            while pq:
                _, _, current_g, current_board, _ = heapq.heappop(pq)
                
                # Limit depth
                if current_g >= 3:
                    continue
                
                next_moves = self.get_available_moves(current_board)
                for next_move in next_moves:
                    r, c = next_move
                    next_board = copy.deepcopy(current_board)
                    next_player = opponent if current_g % 2 == 1 else player
                    next_board[r][c] = next_player
                    nodes_explored += 1
                    
                    winner = self.check_winner(next_board)
                    if winner == player:
                        move_score += (10 - current_g)
                    elif winner == opponent:
                        move_score -= (10 - current_g)
                    
                    if winner is None and current_g < 2:
                        next_g = current_g + 1
                        next_h = self.heuristic(next_board, player)
                        next_f = next_g + next_h
                        counter += 1
                        heapq.heappush(pq, (next_f, counter, next_g, next_board, move))
            
            if move_score > best_score:
                best_score = move_score
                best_move = move
        
        self.search_stats = {
            'nodes_explored': nodes_explored,
            'time': time.time() - start_time
        }
        return best_move
    
    def ai_move(self):
        if self.ai_algorithm == 'BFS':
            move = self.bfs_search(self.board, 'O')
        elif self.ai_algorithm == 'DFS':
            move = self.dfs_search(self.board, 'O')
        else:  # A*
            move = self.astar_search(self.board, 'O')
        
        if move:
            row, col = move
            self.mark_square(row, col, 'O')
    
    def reset(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.search_stats = {'nodes_explored': 0, 'time': 0}

def draw_ui(game):
    # Draw status bar
    pygame.draw.rect(screen, (40, 40, 40), (0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE))
    
    # Display current player or winner
    if game.game_over:
        if game.winner == 'Draw':
            text = font.render("Game Draw!", True, TEXT_COLOR)
        else:
            text = font.render(f"Winner: {game.winner}!", True, TEXT_COLOR)
    else:
        text = font.render(f"Player: {game.current_player}", True, TEXT_COLOR)
    screen.blit(text, (10, BOARD_SIZE + 5))
    
    # Display algorithm
    algo_text = small_font.render(f"AI: {game.ai_algorithm}", True, TEXT_COLOR)
    screen.blit(algo_text, (10, BOARD_SIZE + 30))
    
    # Display search stats
    if game.search_stats['nodes_explored'] > 0:
        stats_text = small_font.render(
            f"Nodes: {game.search_stats['nodes_explored']} | {game.search_stats['time']:.3f}s", 
            True, TEXT_COLOR
        )
        screen.blit(stats_text, (10, BOARD_SIZE + 50))
    
    # Draw buttons - compact layout
    button_width = 55
    button_height = 30
    button_x_start = 310
    button_y = BOARD_SIZE + 10
    button_spacing = 5
    
    # Algorithm selection buttons
    bfs_color = BUTTON_HOVER if game.ai_algorithm == 'BFS' else BUTTON_COLOR
    dfs_color = BUTTON_HOVER if game.ai_algorithm == 'DFS' else BUTTON_COLOR
    astar_color = BUTTON_HOVER if game.ai_algorithm == 'A*' else BUTTON_COLOR
    
    pygame.draw.rect(screen, bfs_color, (button_x_start, button_y, button_width, button_height), border_radius=5)
    pygame.draw.rect(screen, dfs_color, (button_x_start + button_width + button_spacing, button_y, button_width, button_height), border_radius=5)
    pygame.draw.rect(screen, astar_color, (button_x_start + (button_width + button_spacing) * 2, button_y, button_width, button_height), border_radius=5)
    
    bfs_text = small_font.render("BFS", True, TEXT_COLOR)
    dfs_text = small_font.render("DFS", True, TEXT_COLOR)
    astar_text = small_font.render("A*", True, TEXT_COLOR)
    
    screen.blit(bfs_text, (button_x_start + 15, button_y + 8))
    screen.blit(dfs_text, (button_x_start + button_width + button_spacing + 15, button_y + 8))
    screen.blit(astar_text, (button_x_start + (button_width + button_spacing) * 2 + 20, button_y + 8))
    
    # Reset button
    reset_button_width = button_width * 3 + button_spacing * 2
    pygame.draw.rect(screen, (231, 76, 60), (button_x_start, button_y + button_height + 10, reset_button_width, button_height), border_radius=5)
    reset_text = small_font.render("Reset Game", True, TEXT_COLOR)
    screen.blit(reset_text, (button_x_start + 35, button_y + button_height + 18))

def main():
    game = TicTacToe()
    clock = pygame.time.Clock()
    
    # Button dimensions
    button_width = 55
    button_height = 30
    button_x_start = 310
    button_y_algo = BOARD_SIZE + 10
    button_spacing = 5
    reset_button_width = button_width * 3 + button_spacing * 2
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                mouseX, mouseY = event.pos
                
                # Check algorithm buttons
                if button_y_algo <= mouseY <= button_y_algo + button_height:
                    if button_x_start <= mouseX <= button_x_start + button_width:
                        game.ai_algorithm = 'BFS'
                    elif button_x_start + button_width + button_spacing <= mouseX <= button_x_start + (button_width + button_spacing) * 2:
                        game.ai_algorithm = 'DFS'
                    elif button_x_start + (button_width + button_spacing) * 2 <= mouseX <= button_x_start + (button_width + button_spacing) * 3:
                        game.ai_algorithm = 'A*'
                
                # Check reset button
                reset_y = button_y_algo + button_height + 10
                if reset_y <= mouseY <= reset_y + button_height:
                    if button_x_start <= mouseX <= button_x_start + reset_button_width:
                        game.reset()
                        screen.fill(BG_COLOR)
                
                # Check board clicks
                if mouseY < BOARD_SIZE and game.current_player == 'X':
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    
                    if game.mark_square(clicked_row, clicked_col, 'X'):
                        game.current_player = 'O'
                        winner = game.check_winner()
                        if winner:
                            game.game_over = True
                            game.winner = winner
            
            # Reset button also works when game is over
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_over:
                mouseX, mouseY = event.pos
                reset_y = button_y_algo + button_height + 10
                if reset_y <= mouseY <= reset_y + button_height:
                    if button_x_start <= mouseX <= button_x_start + reset_button_width:
                        game.reset()
                        screen.fill(BG_COLOR)
        
        # AI move
        if game.current_player == 'O' and not game.game_over:
            pygame.time.wait(500)  # Small delay for better UX
            game.ai_move()
            game.current_player = 'X'
            winner = game.check_winner()
            if winner:
                game.game_over = True
                game.winner = winner
        
        # Draw everything
        screen.fill(BG_COLOR)
        game.draw_lines()
        game.draw_figures()
        draw_ui(game)
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
