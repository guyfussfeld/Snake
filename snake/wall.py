#################################################################
# FILE : wall.py
# WRITER1 : Yonatan Green , yonatan.green1 , 323865386
# WRITER2 : Guy Fussfeld , guyfussfeld , 207766973
# EXERCISE : intro2cs ex10 2022-2023
# DESCRIPTION: wall
#################################################################
class Wall:
    """This Class represents a wall object, containing color, direction
        and body - containing 3 positions. 
    """
    def __init__(self, pos, dir):
        self.__color = "blue"
        self.__dir = dir

        #set wall coordinates according to direction
        if dir == "Up":
            self.__body = [(pos[0], pos[1]+1), pos, (pos[0], pos[1]-1)]
        if dir == "Down":
            self.__body = [(pos[0], pos[1]-1), pos, (pos[0], pos[1]+1)]
        if dir == "Right":
            self.__body = [(pos[0]+1, pos[1]), pos, (pos[0]-1, pos[1])]
        if dir == "Left":
            self.__body = [(pos[0]-1, pos[1]), pos, (pos[0]+1, pos[1])]

    def get_color(self):
        return self.__color

    def get_cells(self):
        return self.__body

    def move_wall(self):
        """this function changes the body coordinates of the wall
            to the next position
        """

        index = len(self.__body)-1
        for i in self.__body[:0:-1]: #iterate from end to beginning excluding head
            self.__body[index] = self.__body[index-1] 
            index -= 1
        self.__body[0] = self.get_next_pos()
        
    def get_next_pos(self):
        """return next coordinate for head of wall"""
        tmp = self.__body[0]

        if self.__dir == "Up":
            next_pos = (tmp[0], tmp[1]+1)
        elif self.__dir == "Right":
            next_pos = (tmp[0]+1, tmp[1])
        elif self.__dir == "Down":
            next_pos = (tmp[0], tmp[1]-1)
        elif self.__dir == "Left":
            next_pos = (tmp[0]-1, tmp[1])

        return next_pos
