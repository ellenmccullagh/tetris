import pygame
import random
pygame.init()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 700
IMAGE_DIRECTORY = "images/"
IMAGES = ["black.png", "red.png", "green.png", "blue.png", "orange.png", "lightblue.png", "purple.png", "yellow.png"]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

image_paths = []
for image in IMAGES:
    image_paths.append(IMAGE_DIRECTORY + image)

class Square(pygame.sprite.Sprite):
    def __init__(self, height, width, row, column, costumes, location, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.height = height
        self.width = width

        self.row = row
        self.column = column

        self.neighbor_right = None
        self.neighbor_left = None
        self.neighbor_up = None
        self.neighbor_down = None

        self.state = 0 #0 for off, 1 for red, 2 for green, 3 for blue, 4 for orange and 5 for light blue
        self.costumes = [] #should be in same order as above

        self.moved_once = False #to prevent flushing right every time right arrow pressed.

        for costume in costumes:
            loaded_costume = pygame.image.load(costume).convert()
            loaded_costume = pygame.transform.scale(loaded_costume, (int(width), int(height)))
            self.costumes.append(loaded_costume)

        self.location = location
        self.fixed = False

        self.image = self.costumes[0] #setting costume to black square
        self.rect = self.image.get_rect()
        self.rect.topleft = location

        self.chain = [] #this is for when

    def setNeighbors(self, neighbor_right, neighbor_left, neighbor_up, neighbor_down):
        self.neighbor_right = neighbor_right
        self.neighbor_left = neighbor_left
        self.neighbor_up = neighbor_up
        self.neighbor_down = neighbor_down

    def setCostume(self, state):
        #print("state: {}".format(state))
        self.image = self.costumes[state]
        self.state = state

    def print_block(self):
        print("State: {}; Location: ({}, {})".format(self.state, self.row, self.column))

    def print_neighbors(self):
        print("I am at ({}, {}), my neighbors are:".format(self.row, self.column))
        neighbors = [(self.neighbor_right, "right"), (self.neighbor_left, "left"), (self.neighbor_up, "up"), (self.neighbor_down, "down")]
        for neighbor in neighbors:
            if neighbor[0] == "None":
                print("{}: None".format(neighbor[1]))
            else:
                print("{}: ".format(neighbor[1]), end = "")
                neighbor[0].print_block()

    def draw(self, screen):
        screen.blit(self.image, self.location)


class Grid:
    def __init__(self, blocks_across, blocks_updown, grid_width, grid_height, images, location, squares_group):
        self.blocks_across = blocks_across
        self.blocks_updown = blocks_updown

        self.grid_height = grid_height
        self.grid_width = grid_width

        self.block_height = self.grid_height / self.blocks_updown
        self.block_width = self.grid_width / self.blocks_across

        self.images = images
        self.location = location

        self.anchor = [int(blocks_across / 2), 0]

        # blocks are set in a 2x2 array of rows. the rows will be drawn bottom up so the bottom will be 0 and top will be increase in number
        self.blocks = []

        for i in range(self.blocks_updown): #row
            block_row = []
            for j in range(self.blocks_across): #column
                block_location = (self.location[0] + self.block_width * j, self.location[1] + self.block_height * i)
                new_block = Square(self.block_height, self.block_width, i, j, self.images, block_location, squares_group)
                block_row.append(new_block)
            self.blocks.append(block_row)

    def setNeighbors(self):
        for i in range(self.blocks_updown):
            for j in range(self.blocks_across):
                block_right = "None"
                block_left = "None"
                block_up = "None"
                block_down = "None"

                if j != self.blocks_across - 1:
                    block_right = self.blocks[i][j + 1]
                if j != 0:
                    block_left = self.blocks[i][j - 1]
                if i > 0:
                    block_up = self.blocks[i - 1][j]
                if i < self.blocks_updown - 1:
                    block_down = self.blocks[i + 1][j]

                self.blocks[i][j].setNeighbors(block_right, block_left, block_up, block_down)

    def draw(self, screen):
        for row in self.blocks:
            for block in row:
                block.draw(screen)

    def print_grid(self):
        for row in self.blocks:
            for block in row:
                block.print_block()

    def print_neighbors(self):
        for row in self.blocks:
            for block in row:
                block.print_neighbors()

class Tetromino:
    def __init__(self, anchor_location):
        self.anchor_location = anchor_location
        self.state = 0
        self.points = []

    def setKind(self, kind):
        anchor_x = self.anchor_location [0]
        anchor_y = self.anchor_location [1]
        if kind == "I":
            self.points = [[anchor_x, anchor_y], [anchor_x, anchor_y + 1],
                            [anchor_x, anchor_y + 2], [anchor_x, anchor_y + 3]]
            self.state = 1
        elif kind == "O":
            self.points = [[anchor_x, anchor_y], [anchor_x + 1, anchor_y],
                            [anchor_x, anchor_y + 1], [anchor_x + 1, anchor_y + 1]]
            self.state = 2
        elif kind == "L":
            self.points = [[anchor_x, anchor_y], [anchor_x , anchor_y + 1],
                            [anchor_x, anchor_y + 2], [anchor_x + 1, anchor_y + 2]]
            self.state = 3
        elif kind == "J":
            self.points = [[anchor_x, anchor_y], [anchor_x , anchor_y + 1],
                            [anchor_x, anchor_y + 2], [anchor_x - 1, anchor_y + 2]]
            self.state = 4
        elif kind == "S":
            self.points = [[anchor_x, anchor_y], [anchor_x + 1 , anchor_y], [anchor_x, anchor_y + 1], [anchor_x - 1, anchor_y + 1]]
            self.state = 5
        elif kind == "Z":
            self.points = [[anchor_x, anchor_y], [anchor_x - 1 , anchor_y], [anchor_x, anchor_y + 1], [anchor_x + 1, anchor_y + 1]]
            self.state = 6
        elif kind == "T":
            self.points = [[anchor_x, anchor_y], [anchor_x + 1 , anchor_y], [anchor_x + 2, anchor_y], [anchor_x + 1, anchor_y + 1]]
            self.state = 7
        elif kind == "None":
            self.points = []
            self.state = 0

    def moveDown(self):
        for i in range(len(self.points)):
            self.points[i][1] += 1

    def moveRight(self):
        for i in range(len(self.points)):
            self.points[i][0] += 1

    def moveLeft(self):
        for i in range(len(self.points)):
            self.points[i][0] -= 1

    def rotateClockwise(self): # apply translation to origin, rotate then translate back again.
        point_of_rotation = self.points[1]
        new_points = []
        for point in self.points:
            new_points.append([point[1] - point_of_rotation[1] + point_of_rotation[0], #new x
                                point_of_rotation[0] - point[0] + point_of_rotation[1]]) #new y
        print("Old points: {}".format(self.points))
        print("New points: {}".format(new_points))
        return new_points

    def rotateCounterClockwise(self):
        point_of_rotation = self.points[1]
        new_points = []
        for point in self.points:
            new_points.append([point_of_rotation[1] - point[1] + point_of_rotation[0] #new x
                                , point[0] - point_of_rotation[0] + point_of_rotation[1]]) #new y
        print("Old points: {}".format(self.points))
        print("New points: {}".format(new_points))
        return new_points

class Game:
    def __init__(self, screen_dimensions, grid_dimensions, images, grid_location, squares_group):
        self.grid = Grid(grid_dimensions[0], grid_dimensions[1], screen_dimensions[0], screen_dimensions[1], images, grid_location, squares_group)
        self.grid.setNeighbors()
        self.tetro = Tetromino((int(grid_dimensions[0]/2), 0))
        self.tetro.setKind("L")
        self.tetro_states = ["I", "O", "L", "J", "S", "Z", "T"]
        self.ready = False
        self.score = 0
        self.myfont = pygame.font.SysFont("monospace", 15)

    def randomTetro(self):
        random_number = random.randint(0, len(self.tetro_states) - 1)
        print("random number: {}".format(random_number))
        self.tetro.setKind(self.tetro_states[random_number])
        self.ready = False

    def resetGrid(self):
        for row in self.grid.blocks:
            for block in row:
                if not block.fixed:
                    if [block.column, block.row] in self.tetro.points: #if the block is one of the tetromino points it should have the associated costume
                        block.setCostume(self.tetro.state)
                    else:
                        block.setCostume(0) # this block is not one of the tetromino points

    def canMoveDown(self):
        count = 0
        for point in self.tetro.points:
            down = self.grid.blocks[point[1]][point[0]].neighbor_down
            if down == "None" or down.fixed:
                    count += 1
        if count == 0:
            return True
        else:
            return False

    def moveDown(self):
        if self.canMoveDown():
            self.tetro.moveDown()
            self.resetGrid()
            if not self.canMoveDown():
                for point in self.tetro.points:
                    self.grid.blocks[point[1]][point[0]].fixed = True
                    self.tetro.setKind("None")
                    self.ready = True
            else:
                self.ready = False

    def canMoveRight(self):
        count = 0
        for point in self.tetro.points:
            print("row: {}, column:{}".format(point[0], point[1]))
            right = self.grid.blocks[point[1]][point[0]].neighbor_right
            if right == "None" or right.fixed:
                    count += 1
        if count == 0:
            return True
        else:
            return False

    def moveRight(self):
        if self.canMoveRight():
            self.tetro.moveRight()
            self.resetGrid()

    def canMoveLeft(self):
        count = 0
        for point in self.tetro.points:
            left = self.grid.blocks[point[1]][point[0]].neighbor_left
            if left == "None" or left.fixed:
                    count += 1
        if count == 0:
            return True
        else:
            return False

    def moveLeft(self):
        if self.canMoveLeft():
            self.tetro.moveLeft()
            self.resetGrid()

    def rowsFilled(self):
        filled_rows = []
        for row in reversed(self.grid.blocks):
            total = 0
            for block in row:
                if block.state != 0 and block.fixed:
                    total += 1
            if total == self.grid.blocks_across:
                filled_rows.append(row[0].row) #row number
                self.score += 1
        return filled_rows

    def moveRowsDown(self, start_row):
        for i in reversed(range(0, start_row + 1)): #want inclusive
            for j in range(0, self.grid.blocks_across): #moving across the row from left to right
                print("indices: i = {}, j = {}".format(i, j))
                if i == 0:
                    self.grid.blocks[i][j].fixed = False
                    self.grid.blocks[i][j].setCostume(0)
                else:
                    self.grid.blocks[i][j].fixed = False
                    self.grid.blocks[i][j].setCostume(self.grid.blocks[i-1][j].state) #minus 1 goes up
                    self.grid.blocks[i][j].fixed = self.grid.blocks[i-1][j].fixed

    def filledRowAnimation(self, row):
        print("animation here")
        pygame.display.flip()

    def clearFilledRows(self):
        filled_rows = self.rowsFilled()
        for row_filled in filled_rows:
            self.filledRowAnimation(row_filled)
            print("this row is filled: {}".format(row_filled))
            self.moveRowsDown(row_filled) #don't need to minus one because the range function that is reversed later is not inclusive

    def canRotateClockwise(self):
        for point in self.tetro.rotateClockwise():
            if not(0 <= point[0] < self.grid.blocks_across and 0 <= point[1] < self.grid.blocks_updown):
                return False
            if self.grid.blocks[point[1]][point[0]].fixed:
                return False
        return True

    def canRotateCounterClockwise(self):
        count = 0
        for point in self.tetro.rotateCounterClockwise():
            #print("New X = {}, max = {}".format(point[0], self.grid.blocks_across))
            #print("New Y = {}, max = {}".format(point[1], self.grid.blocks_updown))
            if not(0 <= point[0] < self.grid.blocks_across and 0 <= point[1] < self.grid.blocks_updown):
                return False
            if self.grid.blocks[point[1]][point[0]].fixed:
                return False
        return True

    def rotateClockwise(self):
        if self.canRotateClockwise():
            self.tetro.points = self.tetro.rotateClockwise()

    def rotateCounterClockwise(self):
        if self.canRotateCounterClockwise():
            self.tetro.points = self.tetro.rotateCounterClockwise()

    def displayScore(self, screen, location):
        label = self.myfont.render("Score: {}".format(self.score), 1, (0, 0, 0))
        screen.blit(label, location)


def main():
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()

    done = False

    squares_group = pygame.sprite.Group()
    tetromino_group = pygame.sprite.Group()

    main_game = Game((240, 480), (10, 20), image_paths, (200, 10), squares_group)

    screen.fill((0, 255, 0))

    main_game.grid.draw(screen)
    pygame.display.flip()
    pygame.time.wait(2000)

    while not done:
        screen.fill((0, 255, 0))
        main_game.displayScore(screen, (10, 10))

        if main_game.ready:
            main_game.randomTetro()
            main_game.grid.draw(screen)
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    main_game.moveRight()
                if event.key == pygame.K_LEFT:
                    main_game.moveLeft()
                if event.key == pygame.K_a:
                    main_game.rotateCounterClockwise()
                if event.key == pygame.K_d:
                    main_game.rotateClockwise()

        main_game.moveDown()
        main_game.clearFilledRows()

        main_game.grid.draw(screen)
        pygame.display.flip()
        clock.tick(3)

if __name__ == '__main__':
    main()
