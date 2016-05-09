import pygame
pygame.init()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 700
IMAGE_DIRECTORY = "/Users/ellenmccullagh/Documents/SIP/Pygame/tetris/images/"
IMAGES = ["black.png", "red.png", "green.png", "blue.png", "orange.png", "lightblue.png"]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

image_paths = []
for image in IMAGES:
    image_paths.append(IMAGE_DIRECTORY + image)

class Tetrominoes(pygame.sprite.Sprite):
    def __init__(self, kind, block_height, block_width, anchor_location, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.points = []
        anchor_x = anchor_location [0]
        anchor_y = anchor_location [1]

        if kind == "I":
            self.points = [[anchor_x, anchor_y], [anchor_x, anchor_y + 1], [anchor_x, anchor_y + 2], [anchor_x, anchor_y + 3]]
        else if kind == "O":
            self.points = [[anchor_x, anchor_y], [anchor_x + 1, anchor_y], [anchor_x, anchor_y + 1], [anchor_x + 1, anchor_y + 1]]


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
        self.image = self.costumes[state]
        self.state = state

    def moveDown(self):
        #CASCADING - on states are cascaded down the grid
        #self.print_block()
        if self.neighbor_down != "None" and self.state != 0 and (not self.fixed):
            #print("inside conditional")
            #print("down neighbor is fixed: {}".format(self.neighbor_down.fixed))
            if (not self.neighbor_down.fixed):
                #print("neighbor is not fixed")
                self.neighbor_down.print_block()
                self.neighbor_down.setCostume(self.state)
                #if self.neighbor_up == "None" or self.neighbor_up.state == 0:
                self.setCostume(0)
            else:
                self.fixed = True
                #print("({}, {}) is fixed because down neighbor fixed".format(self.row, self.column))
        elif self.neighbor_down == "None" and self.state != 0:
            self.fixed = True
            #print("({}, {}) is fixed because reached edge".format(self.row, self.column))

    def moveRight(self):
        if self.neighbor_right!= "None" and self.state != 0 and not self.fixed and not self.moved_once:
            if not self.neighbor_right.fixed:
                #logic! must move necessary blocks before overwriting them.
                #this doesn't arise on move left because the blocks are tested and moved going left to right.
                if self.neighbor_right.state == self.state:
                    self.neighbor_right.moveRight()
                self.neighbor_right.setCostume(self.state)
                #need to move the block only once per game loop.
                self.neighbor_right.moved_once = True

                self.setCostume(0)

    def canIGoLeft(self):
        if

    def moveLeft(self):
        if self.neighbor_left != "None" and self.state != 0 and not self.fixed:
            if not self.neighbor_left.fixed:
                self.neighbor_left.setCostume(self.state)
                self.setCostume(0)

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

    def startShapeI(self):
        anchor_x = self.anchor[0]
        anchor_y = self.anchor[1]
        I_shape = [[anchor_x, anchor_y], [anchor_x, anchor_y + 1], [anchor_x, anchor_y + 2], [anchor_x, anchor_y + 3]]
        for coordinate in I_shape:
            self.blocks[coordinate[1]][coordinate[0]].setCostume(1)

    def startShapeO(self):
        anchor_x = self.anchor[0]
        anchor_y = self.anchor[1]
        O_shape = [[anchor_x, anchor_y], [anchor_x + 1, anchor_y], [anchor_x, anchor_y + 1], [anchor_x + 1, anchor_y + 1]]
        for coordinate in O_shape:
            self.blocks[coordinate[1]][coordinate[0]].setCostume(2)

    def startShapeL(self):
        anchor_x = self.anchor[0]
        anchor_y = self.anchor[1]
        O_shape = [[anchor_x, anchor_y], [anchor_x , anchor_y + 1], [anchor_x, anchor_y + 2], [anchor_x + 1, anchor_y + 2]]
        for coordinate in O_shape:
            self.blocks[coordinate[1]][coordinate[0]].setCostume(3)

    def startShapeJ(self):
        anchor_x = self.anchor[0]
        anchor_y = self.anchor[1]
        O_shape = [[anchor_x, anchor_y], [anchor_x , anchor_y + 1], [anchor_x, anchor_y + 2], [anchor_x - 1, anchor_y + 2]]
        for coordinate in O_shape:
            self.blocks[coordinate[1]][coordinate[0]].setCostume(4)

    def dropDown(self):
        for row in reversed(self.blocks):
            for block in row:
                block.moveDown()

    def pushLEFT(self):
        for row in reversed(self.blocks):
            for block in row:
                block.moveLeft()

    def pushRight(self):
        for row in reversed(self.blocks):
            for block in row:
                block.moveRight()

    def resetMovedOnce(self):
        for row in self.blocks:
            for block in row:
                block.moved_once = False



def main():
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()

    done = False

    squares_group = pygame.sprite.Group()

    main_grid = Grid(12, 16, 300, 400, image_paths, (200, 40), squares_group)
    main_grid.setNeighbors()
    #main_grid.print_neighbors()
    screen.fill((0, 255, 0))
    main_grid.startShapeJ()
    main_grid.draw(screen)
    pygame.display.flip()
    pygame.time.wait(2000)

    while not done:
        screen.fill((0, 255, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    main_grid.pushRight()
                if event.key == pygame.K_LEFT:
                    main_grid.pushLEFT()

        #main_grid.print_grid()
        main_grid.dropDown()

        #main_grid.print_grid()
        main_grid.resetMovedOnce() #necessary to unfreeze blocks from right / left movement.
        main_grid.draw(screen)
        pygame.display.flip()
        clock.tick(3)



if __name__ == '__main__':
    main()
