import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path


class Aki(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):

        possible = []
        path = [game_map[self.row][self.col]]
        stack = []

        row = self.row
        col = self.col
        visited = [(row, col)]

        flag = True

        while flag:
            if row == goal[0] and col == goal[1]:
                break

            if row > 0:
                example = (row - 1, col)
                if example not in visited:
                    possible.append(game_map[row - 1][col])
            if col > 0:
                example = (row, col - 1)
                if example not in visited:
                    possible.append(game_map[row][col - 1])
            if row < (len(game_map) - 1):
                example = (row + 1, col)
                if example not in visited:
                    possible.append(game_map[row + 1][col])
            if col < (len(game_map[0]) - 1):
                example = (row, col + 1)
                if example not in visited:
                    possible.append(game_map[row][col + 1])

            if not possible:
                elem = stack.pop()
                row = elem.row
                col = elem.col
                path.pop()

            else:
                possible.sort(
                    key=lambda tile: (
                        tile.cost(), -4 if tile.row < row else -3 if tile.col > col else -2 if tile.row > row else -1)
                    , reverse=True)
                elem = possible.pop()
                row = elem.row
                col = elem.col
                path.append(game_map[elem.row][elem.col])
                visited.append((elem.row, elem.col))
                stack.extend(possible)
                possible = []

            if not stack:
                flag = False
        return path


class Jocke(Agent):

    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)


    def get_agent_path(self, game_map, goal):

        list = []
        possible = []
        paths=[]
        path = [game_map[self.row][self.col]]


        row = self.row
        col = self.col
        visited = [(row, col)]

        flag = True

        while flag:
            if row == goal[0] and col == goal[1]:
                break

            if row > 0:
                example = (row - 1, col)
                if example not in visited:
                    possible.append(game_map[row - 1][col])
            if col > 0:
                example = (row, col - 1)
                if example not in visited:
                    possible.append(game_map[row][col - 1])
            if row < (len(game_map) - 1):
                example = (row + 1, col)
                if example not in visited:
                    possible.append(game_map[row + 1][col])
            if col < (len(game_map[0]) - 1):
                example = (row, col + 1)
                if example not in visited:
                    possible.append(game_map[row][col + 1])

            if not possible:
                paths.append(((row, col), []))
                elem = list.pop(0)
                row = elem.row
                col = elem.col



            else:
                neighbors_sum={}
                elem=row, col
                for i in possible:
                    sum=0
                    cnt=0
                    if i.row > 0 and (elem!=i.row-1,i.col):
                        element=game_map[i.row-1][i.col]
                        sum+=element.cost()
                        cnt+=1
                    if i.col > 0 and (elem!=i.row,i.col-1):
                        element = game_map[i.row][i.col-1]
                        sum += element.cost()
                        cnt += 1
                    if i.row < (len(game_map) - 1) and (elem!=i.row+1,i.col):
                        element = game_map[i.row+1][i.col]
                        sum += element.cost()
                        cnt += 1
                    if i.col < (len(game_map[0]) - 1) and (elem!=i.row,i.col+1):
                        element = game_map[i.row][i.col +1]
                        sum += element.cost()
                        cnt += 1
                    if sum!=0:
                        sum=sum/cnt
                    neighbors_sum[i.position()]= sum

                if (2,1) in neighbors_sum:
                    print(neighbors_sum[(2, 1)])
                    if (1,0) in neighbors_sum:
                        print(neighbors_sum[(1,0)])

                possible.sort(
                    key=lambda tile: (
                        neighbors_sum[tile.position()], -4 if tile.row < row else -3 if tile.col > col else -2 if tile.row > row else -1))

                paths.append(((row,col), possible))
                for i in possible:
                    visited.append(i.position())
                list.extend(possible)
                elem = list.pop(0)
                row = elem.row
                col = elem.col
                possible = []

            if not list:
                flag = False

        paths=paths[-1::-1]
        print(paths)
        elem_r = goal[0]
        elem_c=goal[1]
        elem=game_map[goal[0]][goal[1]]

        path_helper=[]



        for onepath in paths:
            for onetile in onepath[1]:
                if (elem_r, elem_c) == onetile.position():
                    elem_r, elem_c = onepath[0]
                    path_helper.append(onetile)

        path_helper.extend(path)
        path_helper=path_helper[-1::-1]
        path=path_helper


        return path

# class Draza(Agent):


class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
