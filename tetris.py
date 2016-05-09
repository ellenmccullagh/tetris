import pygame

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 700
IMAGE_DIRECTORY = "/Users/ellenmccullagh/Documents/SIP/Pygame/tetris/images/"
IMAGES = ["black.png", "red.png", "green.png", "blue.png", "orange.png", "lightblue.png"]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

image_paths = []
for image in IMAGES:
    image_paths.append(IMAGE_DIRECTORY + image)

class Square(pygame.sprite.Sprite):
    def __init__(self, height, width, row, column, costumes, location):
        pygame.sprite.Sprite.__init__(self)
        self.height = height
        self.width = width

        self.row = row
        self.column = column

        self.neighbor_right = None
        self.neighbor_left = None
        self.neighbor_up = None
        self.neightbor_down = None

        self.state = 0 #0 for off, 1 for red, 2 for green, 3 for blue, 4 for orange and 5 for light blue
        self.costumes = [] #should be in same order as above

        for costume in costumes:
            loaded_costume = pygame.image.load(costume).convert()
            loaded_costume = pygame.transform.scale(loaded_costume, (int(width), int(height)))
            self.costumes.append(loaded_costume)

        self.location = location
        self.fixed = False

        self.image = self.costumes[0] #setting costume to off
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def setNeighbors(self, neighbor_right, neighbor_left, neighbor_up, neighbor_down):
        self.neighbor_right = neighbor_right
        self.neighbor_left = neighbor_left
        self.neighbor_up = neighbor_up
        self.neighbor_down = neighbor_down

    def setCostume(self, state):
        self.image = self.costume[state]

    def moveDown(self):
        if self.neighbor_down == "None":
            return
        if not self.neighbor_down.fixed:
            self.neighbor_down.setCostume(self.state)
            if self.neighbor_up.state == 0:
                self.setCostume(0)
        else:
            self.fixed == True

    def moveRight(self):
        if self.neighbor_right == "None":
            return
        if not self.neighbor_right.fixed:
            self.neighbor_right.setCostume(self.state)
            if self.neighbor_left.state == 0:
                self.setCostume(0)

    def moveLeft(self):
        if self.neighbor_left == "None":
            return
        if not self.neighbor_left.fixed:
            self.neighbor_left.setCostume(self.state)
            if self.neighbor_right.state == 0:
                self.setCostume(0)

    def draw(self, screen):
        screen.blit(self.image, self.location)


class Grid:
    def __init__(self, blocks_across, blocks_updown, grid_width, grid_height, images, location):
        self.blocks_across = blocks_across
        self.blocks_updown = blocks_updown

        self.grid_height = grid_height
        self.grid_width = grid_width

        self.block_height = self.grid_height / self.blocks_updown
        self.block_width = self.grid_width / self.blocks_across

        self.images = images
        self.location = location

        # blocks are set in a 2x2 array of rows. the rows will be drawn bottom up so the bottom will be 0 and top will be increase in number
        self.blocks = []
        for i in range(self.blocks_updown): #row
            block_row = []
            for j in range(self.blocks_across): #column
                block_location = (self.location[0] + self.block_width * j, self.location[1] + self.block_height * i)
                new_block = Square(self.block_height, self.block_width, i, j, self.images, block_location)
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
                    block_right = self.blocks[i][j - 1]
                if j != 0:
                    block_left = self.blocks[i][j - 1]
                if i > 0:
                    block_down = self.blocks[i - 1][j]
                if i < self.blocks_updown - 1:
                    block_up = self.blocks[i + 1][j]

                self.blocks[i][j].setNeighbors(block_right, block_left, block_up, block_down)

    def draw(self, screen):
        for row in self.blocks:
            for block in row:
                block.draw(screen)


def main():
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()

    done = False

    while not done:
        screen.fill(WHITE)
        '''
        main_grid = Grid(3, 4, 300, 400, image_paths, (0, 250))
        main_grid.setNeighbors()
        main_grid.draw(screen)
        '''
        square_test = Square(30, 40, 1, 1, image_paths, (350, 250))
        pygame.display.flip()
        clock.tick(60)



if __name__ == '__main__':
    main()
