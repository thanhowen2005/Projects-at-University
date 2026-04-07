from board_and_cost import boards
from board_and_cost import cost_table
from collections import deque
import copy
import pygame
import math
import heapq

pygame.init()

WIDTH = 600
HEIGHT = 690

screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 15)
level = copy.deepcopy(boards)
PI = math.pi
color = 'blue'
height_box = (HEIGHT - 50) // 32
width_box = (WIDTH // 30)


#--------------------------ghost settings------------------------------------
redGhost_image = pygame.transform.scale(pygame.image.load(f'images/ghost_images/red.png'), (30, 30))
pinkGhost_image = pygame.transform.scale(pygame.image.load(f'images/ghost_images/pink.png'), (30, 30))
blueGhost_image = pygame.transform.scale(pygame.image.load(f'images/ghost_images/blue.png'), (30, 30))
orangeGhost_image = pygame.transform.scale(pygame.image.load(f'images/ghost_images/orange.png'), (30, 30))
powerGhost_image = pygame.transform.scale(pygame.image.load(f'images/ghost_images/powerup.png'), (30, 30))

cost = copy.deepcopy(cost_table)

ghost_speed = 2

bGhost_x = 260
bGhost_y = 280
blue_Path = []

pGhost_x = 260
pGhost_y = 320
pink_Path = []

oGhost_x = 320
oGhost_y = 280
orange_Path = []

rGhost_x = 320
rGhost_y = 320
red_Path = []

ghost_targets = [(260,280), (260,320), (320,260), [320,320]]
#---------------------pacman settings--------------------------
player_x = 280
player_y = 480
direction = 0
player_speed = 2
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'images/player_images/{i}.png'), (30, 30)))
score = 0
living_time = 0
time_counter = 0
power = False
powerCount = 0
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
moving = False
begin_wait = 0
live = 2
game_End = False
win = False



##=========================GHOST FUNCTIONS================================
class Ghost:
    def __init__(self, x_cor, y_cor, target, speed, img):
        self.x_pos = x_cor
        self.y_pos = y_cor
        self.center_x = self.x_pos + 10
        self.center_y = self.y_pos + 10
        self.target = target
        self.speed = speed
        self.image = img
        self.rect = self.draw()
    
    def draw(self):
        if not power:
            screen.blit(self.image, (self.x_pos, self.y_pos))
        else :
            screen.blit(powerGhost_image, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 15, self.center_y - 15), (30, 30))
        return ghost_rect
    
    def move_blueGhost(self):
         # r, l, u, d
        global blue_Path
        global orange_Path
        if self.target[0] % 20 != 0 or self.target[1] % 20 != 0:
            self.target = (self.target[0] // 20 * 20, self.target[1] // 20 * 20)

        if not blue_Path:
            blue_Path = self.bfsSearch(self.target)
            if blue_Path:
                del blue_Path[0]

        current_pos = (self.x_pos, self.y_pos)
        
        if blue_Path:  
            if current_pos == blue_Path[0]:  
                del blue_Path[0]
                blue_Path = self.bfsSearch(self.target) 
                if blue_Path:
                    del blue_Path[0]
        if blue_Path:
            self.target = blue_Path[0]
            ghost_targets[0] = self.target
        else:
            ghost_targets[0] = (0, 0)
            

        if blue_Path:
                    
            if self.x_pos == self.target[0]:
                if self.y_pos < self.target[1]:
                    self.y_pos += self.speed
                else:
                    self.y_pos -= self.speed
            else:
                if self.x_pos < self.target[0]:
                    self.x_pos += self.speed
                else:
                    self.x_pos -= self.speed

        return self.x_pos, self.y_pos


    def move_pinkGhost(self):
         # r, l, u, d
        global pink_Path
        global blue_Path
        if self.target[0] % 20 != 0 or self.target[1] % 20 != 0:
            self.target = (self.target[0] // 20 * 20, self.target[1] // 20 * 20)

        if not pink_Path:
            pink_Path = self.dfsSearch(self.target)
            if pink_Path:
                del pink_Path[0]

        current_pos = (self.x_pos, self.y_pos)
        
        if pink_Path:  
            if current_pos == pink_Path[0]:  
                del pink_Path[0]

        if pink_Path:
            self.target = pink_Path[0]
            ghost_targets[1] = self.target

        if pink_Path:
            #move
            if self.x_pos == self.target[0]:
                if self.y_pos < self.target[1]:
                    self.y_pos += self.speed
                else:
                    self.y_pos -= self.speed
            else:
                if self.x_pos < self.target[0]:
                    self.x_pos += self.speed
                else:
                    self.x_pos -= self.speed

        return self.x_pos, self.y_pos


    def move_orangeGhost(self):
         # r, l, u, d

        global orange_Path
        if self.target[0] % 20 != 0 or self.target[1] % 20 != 0:
            self.target = (self.target[0] // 20 * 20, self.target[1] // 20 * 20)
        if not orange_Path:
            orange_Path = self.ucsSearch(self.target) 
            if orange_Path:
                del orange_Path[0]

        current_pos = (self.x_pos, self.y_pos)
        
        if orange_Path:  
            if current_pos == orange_Path[0]:  
                del orange_Path[0] 
                orange_Path = self.ucsSearch(self.target)
                if orange_Path:
                    del orange_Path[0]
        
        if orange_Path:
            self.target = orange_Path[0]
            ghost_targets[2] = self.target
        #move
        if orange_Path:
            if self.x_pos == self.target[0]:
                if self.y_pos < self.target[1]:
                    self.y_pos += self.speed
                else:
                    self.y_pos -= self.speed
            else:
                if self.x_pos < self.target[0]:
                    self.x_pos += self.speed
                else:
                    self.x_pos -= self.speed

        return self.x_pos, self.y_pos

    def move_redGhost(self):
         # r, l, u, d

        global red_Path
        if self.target[0] % 20 != 0 or self.target[1] % 20 != 0:
            self.target = (self.target[0] // 20 * 20, self.target[1] // 20 * 20)
        if not red_Path:
            red_Path = self.astarSearch(self.target) 
            if orange_Path:
                del orange_Path[0]

        current_pos = (self.x_pos, self.y_pos)
        
        if red_Path:  
            if current_pos == red_Path[0]:  
                del red_Path[0] 
                red_Path = self.astarSearch(self.target)
                if red_Path:
                    del red_Path[0]
        
        if red_Path:
            self.target = red_Path[0]
            ghost_targets[3] = self.target
        #move
        if red_Path:
            if self.x_pos == self.target[0]:
                if self.y_pos < self.target[1]:
                    self.y_pos += self.speed
                else:
                    self.y_pos -= self.speed
            else:
                if self.x_pos < self.target[0]:
                    self.x_pos += self.speed
                else:
                    self.x_pos -= self.speed

        return self.x_pos, self.y_pos


    def bfsSearch(self, target):
        height_box = (HEIGHT - 50) // 32
        width_box = (WIDTH // 30)
        x_search = self.x_pos
        y_search = self.y_pos
        start = (x_search // 20 * 20, y_search // 20 * 20)
        frontier = deque([start])
        parent = {start: None}
        explored = set()

        DIRECTIONS = [(20, 0), (-20, 0), (0, -20), (0, 20)]

        while frontier:
            current = frontier.popleft()
            if current[0] % 20 != 0 or current[1] % 20 != 0:
                        current = (current[0] // 20 * 20, current[1] // 20 * 20)

            # Neu tim thay dich thi truy vet duong di
            if current == target:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1] # Tra ve duong di theo thu tu dung
            
            explored.add(current)
            
            for move in DIRECTIONS:
                new_pos = (current[0] + move[0], current[1] + move[1])

                if new_pos not in explored and new_pos not in parent and new_pos not in ghost_targets:
                    grid_x = new_pos[0] // width_box # Chi so cot trong board
                    grid_y = new_pos[1] // height_box # Chi so hang trong board
  
                    if 0 < grid_x < len(level[0]) - 1 and 0 < grid_y < len(level) - 1:
                        if level[grid_y][grid_x] in [0, 1, 2, 9]:
                            frontier.append(new_pos)
                            parent[new_pos] = current # Luu lai cha cua o
        return []
        


    def dfsSearch(self, target):
        height_box = (HEIGHT - 50) // 32
        width_box = (WIDTH // 30)
        x_search = self.x_pos
        y_search = self.y_pos
        start = (x_search // 20 * 20, y_search // 20 * 20)
        stack = [start]
        parent = {start: None}
        explored = set()

        DIRECTIONS = [(20, 0), (-20, 0), (0, -20), (0, 20)]

        while stack:
            current = stack.pop()
            if current[0] % 20 != 0 or current[1] % 20 != 0:
                current = (current[0] // 20 * 20, current[1] // 20 * 20)
            
            # Neu tim thay dich thi truy vet duong di
            if current == target:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1] # Tra ve duong di theo thu tu dung
            
            explored.add(current)
            
            for move in DIRECTIONS:
                new_pos = (current[0] + move[0], current[1] + move[1])
                
                if new_pos not in explored and new_pos not in parent and new_pos not in ghost_targets:
                    grid_x = new_pos[0] // width_box  # Chi so cot trong board
                    grid_y = new_pos[1] // height_box  # Chi so hang trong board
                    
                    if 0 < grid_x < len(level[0]) - 1 and 0 < grid_y < len(level) - 1:
                        if level[grid_y][grid_x] in [0, 1, 2, 9]:
                            stack.append(new_pos)
                            parent[new_pos] = current # Luu lai cha cua o
        return []


    def ucsSearch(self, target):
        height_box = (HEIGHT - 50) // 32
        width_box = (WIDTH // 30)

        x_search = self.x_pos
        y_search = self.y_pos
        start = (x_search // 20 * 20, y_search // 20 * 20)

        priority_queue = [(0, start)]  # (cost, node)
        parent = {start: None}
        cost_so_far = {start: 0}  # Chi phi den moi o
        explored = set()

        DIRECTIONS = [(20, 0), (-20, 0), (0, -20), (0, 20)]  # Huong di chuyen

        while priority_queue:
            current_cost, current = heapq.heappop(priority_queue)  # Lay o co chi phi thap nhat

            # Dam bao vi tri hien tai nam tren luoi
            if current[0] % 20 != 0 or current[1] % 20 != 0:
                current = (current[0] // 20 * 20, current[1] // 20 * 20)

            # Neu tim thay dich thi truy vet duong di
            if current == target:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]  # Tra ve duong di theo thu tu dung

            explored.add(current)

            for move in DIRECTIONS:
                new_pos = (current[0] + move[0], current[1] + move[1])  # Vi tri moi

                if new_pos not in explored and new_pos not in ghost_targets:
                    grid_x = new_pos[0] // width_box  # Chi so cot trong board
                    grid_y = new_pos[1] // height_box  # Chi so hang trong board

                    if 0 < grid_x < len(level[0]) - 1 and 0 < grid_y < len(level) - 1:
                        if level[grid_y][grid_x] in [0, 1, 2, 9]:  # 0, 1, 2, 9 la cac o co the di duoc
                            # Tinh move_cost dua tren hieu gia tri trong ma tran cost
                            current_cost_value = cost[current[1] // height_box][current[0] // width_box]
                            new_cost_value = cost[grid_y][grid_x]
                            move_cost = abs(new_cost_value - current_cost_value) + 1  # Dam bao move_cost > 0

                            new_cost = current_cost + move_cost  # Cap nhat chi phi den o moi

                            if new_pos not in cost_so_far or new_cost < cost_so_far[new_pos]:
                                cost_so_far[new_pos] = new_cost
                                heapq.heappush(priority_queue, (new_cost, new_pos))  # Dua vao hang doi uu tien
                                parent[new_pos] = current  # Luu lai cha cua o

        return []  # Khong tim thay duong di


    def astarSearch(self, target):
        height_box = (HEIGHT - 50) // 32
        width_box = (WIDTH // 30)

        x_search = self.x_pos
        y_search = self.y_pos
        start = (x_search // 20 * 20, y_search // 20 * 20)

        priority_queue = [(0, start)]  # (f-cost, node)
        parent = {start: None}
        g_cost = {start: 0}  # Chi phi tu node bat dau
        explored = set()

        DIRECTIONS = [(20, 0), (-20, 0), (0, -20), (0, 20)]  # Huong di chuyen

        while priority_queue:
            _, current = heapq.heappop(priority_queue)  # Lay node co chi phi nho nhat

            if current == target:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]  # Tra ve duong di theo thu tu nguoc lai

            explored.add(current)  # Danh dau node da duyet

            for move in DIRECTIONS:
                new_pos = (current[0] + move[0], current[1] + move[1])  # Vi tri moi

                # Kiem tra neu vi tri moi hop le
                if new_pos not in explored and new_pos not in ghost_targets:
                    grid_x = new_pos[0] // width_box  # Cot trong luoi
                    grid_y = new_pos[1] // height_box  # Hang trong luoi

                    if 0 < grid_x < len(level[0]) - 1 and 0 < grid_y < len(level) - 1:
                        if level[grid_y][grid_x] in [0, 1, 2, 9]:  # Chi di qua o hop le
                            # Lay chi phi di chuyen tu ma tran cost
                            current_cost = cost[current[1] // height_box][current[0] // width_box]
                            new_cost = cost[grid_y][grid_x]
                            move_cost = abs(new_cost - current_cost) + 1  # Dam bao move_cost > 0

                            # Tinh cac chi phi trong thuat toan A*
                            new_g_cost = g_cost[current] + move_cost  # Chi phi di chuyen
                            h_cost = abs(new_pos[0] - target[0]) + abs(new_pos[1] - target[1])  # Heuristic
                            f_cost = new_g_cost + h_cost  # Tong chi phi

                            # Neu tim thay duong di tot hon thi cap nhat
                            if new_pos not in g_cost or new_g_cost < g_cost[new_pos]:
                                g_cost[new_pos] = new_g_cost
                                heapq.heappush(priority_queue, (f_cost, new_pos))
                                parent[new_pos] = current  # Luu lai cha cua node

        return []  # Khong tim thay duong di




##=============================GRAPHIC FUNCTIONS==========================================
def draw_infor():
    score_txt = font.render(f'Score: {score}', True, 'white')
    living_time_txt = font.render(f'Living time: {living_time} sec', True, 'white')
    screen.blit(score_txt, (35, 660))
    screen.blit(living_time_txt, (135, 660))
    if power:
        power_text = font.render('Power', True, 'red')
        screen.blit(power_text, (365, 665))
        pygame.draw.circle(screen, 'red', (350, 670), 10)
    for i in range(live + 1):
        screen.blit(pygame.transform.scale(player_images[0], (20, 20)), (430 + 30 * i, 660) )
    if game_End:
        box_width = 480
        box_height = 200
        box_x = (600 - box_width) // 2
        box_y = (690 - box_height) // 2

        pygame.draw.rect(screen, 'white', [box_x - 5, box_y - 5, box_width + 10, box_height + 10], 0, 10) 
        pygame.draw.rect(screen, 'gray', [box_x, box_y, box_width, box_height], 0, 10)  

        endgame_text = font.render('Game Over! Space bar to restart!!!', True, 'red')
        totalScore_text = font.render(f'Your score: {score}', True, 'red')
        time_text = font.render(f'Your living time: {living_time} sec', True, 'red')

        text_x = box_x + 20 
        screen.blit(endgame_text, (text_x, box_y + 40))
        screen.blit(totalScore_text, (text_x, box_y + 80))
        screen.blit(time_text, (text_x, box_y + 120))

    if win:
        box_width = 480 
        box_height = 180
        box_x = (600 - box_width) // 2
        box_y = (690 - box_height) // 2

        pygame.draw.rect(screen, 'white', [box_x - 5, box_y - 5, box_width + 10, box_height + 10], 0, 10) 
        pygame.draw.rect(screen, 'gray', [box_x, box_y, box_width, box_height], 0, 10)  

        endgame_text = font.render('Victory! Space bar to restart!!!', True, 'green')
        totalScore_text = font.render(f'Your score: {score}', True, 'red')
        time_text = font.render(f'Your living time: {living_time} sec', True, 'red')

        text_x = box_x + 20  
        screen.blit(endgame_text, (text_x, box_y + 30))
        screen.blit(totalScore_text, (text_x, box_y + 70))
        screen.blit(time_text, (text_x, box_y + 110))

        

def draw_board(board):
    height_box = ((HEIGHT - 50) // 32 )
    width_box = (WIDTH // 30)
    for i in range(len(board)):
        for j in range(len(board[i])):  
            if board[i][j] == 1:
                pygame.draw.circle(screen, 'yellow', (j * width_box + 0.5*width_box, i * height_box + 0.5*height_box), 4)
            if board[i][j] == 2:
                pygame.draw.circle(screen, 'pink', (j * width_box + 0.5*width_box, i * height_box + 0.5*height_box), 10)
            if board[i][j] == 3:
                pygame.draw.line(screen, color, (j * width_box + 0.5 * width_box, i * height_box),
                                 (j * width_box + 0.5 * width_box, i * height_box + height_box), 3)
            if board[i][j] == 4:
                pygame.draw.line(screen, color, (j * width_box, i * height_box + 0.5 * height_box),
                                 (j * width_box + width_box, i * height_box + 0.5 * height_box), 3)
            if board[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * width_box - 0.4 * width_box) - 2, (i * height_box + 0.5 * height_box), width_box, height_box], 0, PI/2, 3)
            if board[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * width_box + 0.5 * width_box), (i * height_box + 0.5 * height_box), width_box, height_box], PI/2, PI, 3)
            if board[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * width_box + 0.5 * width_box), (i * height_box - 0.4 * height_box), width_box, height_box], PI, 3*PI/2, 3)
            if board[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * width_box - 0.4 * width_box) - 2, (i * height_box - 0.4 * height_box), width_box, height_box], 3*PI/2, 2*PI, 3)
            if board[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * width_box, i * height_box + 0.5 * height_box),
                                 (j * width_box + width_box, i * height_box + 0.5 * height_box), 3)        
        

##=============================PACMAN FUNCTIONS==========================================
counter = 0
def draw_player():
    if direction == 0: #RIGHT
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1: #LEFT
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2: #UP
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3: #DOWN
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


move_allowed = [False, False, False, False] #Right, Left, Up, Down
direction_command = 0
def check_position(centerx, centery):
    moves = [False, False, False, False]
    height_box = (HEIGHT - 50) // 32
    width_box = (WIDTH // 30)
    num3 = 11

    if centerx // 30 < 29:
        if direction == 0:
            if level[centery//height_box][(centerx - num3) // width_box] < 3:
                moves[1] = True
        if direction == 1:
            if level[centery//height_box][(centerx + num3) // width_box] < 3:
                moves[0] = True
        if direction == 2:
            if level[(centery+ num3) // height_box][centerx // width_box] < 3:
                moves[3] = True
        if direction == 3:
            if level[(centery - num3) // height_box][centerx // width_box] < 3:
                moves[2] = True

        if direction == 2 or direction == 3:
            if  8 <= centerx % width_box <= 12:
                if level[(centery + num3)//height_box][centerx // width_box] < 3:
                    moves[3] = True
                if level[(centery - num3)//height_box][centerx // width_box] < 3:
                    moves[2] = True
            if  8 <= centery % height_box <= 12:
                if level[centery//height_box][(centerx - width_box) // width_box] < 3:
                    moves[1] = True
                if level[centery//height_box][(centerx + width_box) // width_box] < 3:
                    moves[0] = True

        if direction == 0 or direction == 1:
            if  8 <= centerx % width_box <= 12:
                if level[(centery + height_box)//height_box][centerx // width_box] < 3:
                    moves[3] = True
                if level[(centery - height_box)//height_box][centerx // width_box] < 3:
                    moves[2] = True
            if  8 <= centery % height_box <= 12:
                if level[centery//height_box][(centerx - num3) // width_box] < 3:
                    moves[1] = True
                if level[centery//height_box][(centerx + num3) // width_box] < 3:
                    moves[0] = True

    else:
        moves[0] = True
        moves[1] = True
    return moves


def move_player(play_x, play_y):
    #r, l , u, d
    if direction == 0 and move_allowed[0]:
        play_x += player_speed
    elif direction == 1 and move_allowed[1]:
        play_x -= player_speed

    if direction == 2 and move_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and move_allowed[3]:
        play_y += player_speed
    return play_x, play_y



def collect_item(score, power, powerCount):
    height_box = (HEIGHT - 50) // 32
    width_box = WIDTH // 30
    if 0 < player_x < 600:
        if level[center_y// height_box][center_x//width_box] == 1:
            level[center_y//height_box][center_x//width_box] = 0
            score += 10
        if level[center_y// height_box][center_x//width_box] == 2:
            level[center_y//height_box][center_x//width_box] = 0
            score += 50
            power = True
            powerCount = 0

    return score, power, powerCount


#========================Main for running====================
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    if counter < 19:
        counter += 1
    else:
        counter = 0

    begin_wait += 1
    if begin_wait < 180 or game_End or win:
        moving = False
    else:
        moving = True

    if power and powerCount < 180:
        powerCount += 1
    elif power and powerCount >= 180:
        power_counter = 0
        power = False
    draw_board(level)

    win = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            win = False


    center_x = player_x + 10
    center_y = player_y + 10
    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 10 , 2)


    blueGhost = Ghost(bGhost_x, bGhost_y, (player_x, player_y), ghost_speed, blueGhost_image)
    pinkGhost = Ghost(pGhost_x, pGhost_y, (player_x, player_y), ghost_speed, pinkGhost_image)
    orangeGhost = Ghost(oGhost_x, oGhost_y, (player_x, player_y), ghost_speed, orangeGhost_image)
    redGhost = Ghost(rGhost_x, rGhost_y, (player_x, player_y), ghost_speed, redGhost_image)

    draw_player()
    draw_infor()

    move_allowed = check_position(center_x, center_y)
    if moving:
        time_counter += 1
        living_time = time_counter // 60
        player_x, player_y = move_player(player_x, player_y)
        if not power:
            bGhost_x, bGhost_y = blueGhost.move_blueGhost()
            if begin_wait > 240:
                pGhost_x, pGhost_y = pinkGhost.move_pinkGhost()
            if begin_wait > 300:
                oGhost_x, oGhost_y = orangeGhost.move_orangeGhost()
            if begin_wait > 360:
                rGhost_x, rGhost_y = redGhost.move_redGhost()
            
    score, power, powerCount = collect_item(score, power, powerCount)


    if player_circle.colliderect(blueGhost.rect) or player_circle.colliderect(orangeGhost.rect) or \
        player_circle.colliderect(pinkGhost.rect) or player_circle.colliderect(redGhost.rect):
        if live > 0:
            #player
            power = False
            power_counter = 0
            live -= 1
            player_x = 280
            player_y = 480
            direction = 0
            direction_command = 0
            begin_wait = 0


            #ghost
            bGhost_x = 260
            bGhost_y = 280
            blue_Path.clear()
            
            pGhost_x = 260
            pGhost_y = 320
            pink_Path.clear()
            
            oGhost_x = 320
            oGhost_y = 280
            orange_Path.clear()

            rGhost_x = 320
            rGhost_y = 320
            red_Path.clear()
            ghost_targets = [(260,280), (260,320), (320,260), [320,320]]

        else:
            game_End = True
            moving = False
            begin_wait = 0
            find_blue_Path = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_End or win):
                power = False
                power_counter = 0
                live -= 1
                player_x = 280
                player_y = 480
                direction = 0
                direction_command = 0
                begin_wait = 0

                #ghost
                bGhost_x = 260
                bGhost_y = 280
                blue_Path.clear()
                
                pGhost_x = 260
                pGhost_y = 320
                pink_Path.clear()
                
                oGhost_x = 320
                oGhost_y = 280
                orange_Path.clear()

                rGhost_x = 320
                rGhost_y = 320
                red_Path.clear()
                ghost_targets = [(260,280), (260,320), (320,260), [320,320]]
                
                score = 0
                time_counter = 0
                living_time = 0
                live = 2
                level = copy.deepcopy(boards)
                game_End = False
                win = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction


    move_allowed = check_position(center_x, center_y)
    if direction_command == 0 and move_allowed[0]:
        direction = 0
    if direction_command == 1 and move_allowed[1]:
        direction = 1
    if direction_command == 2 and move_allowed[2]:
        direction = 2
    if direction_command == 3 and move_allowed[3]:
        direction = 3
    pygame.display.flip()
pygame.quit