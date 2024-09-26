#################################################################
# FILE : snake.py
# WRITER1 : Yonatan Green , yonatan.green1 , 323865386
# WRITER2 : Guy Fussfeld , guyfussfeld , 207766973
# EXERCISE : intro2cs ex10 2022-2023
# DESCRIPTION: snake
#################################################################
class Snake:
    """this class represents a Snake, containing length,color,
        direction, body and head
    """
    def __init__(self, width = 40, height = 30):
        self.__length = 3
        self.__color = "black"
        self.__dir = "Up"
        x , y = width // 2 , height // 2
        self.__head = (x,y)
        self.__body = [(x,y), (x,y-1), (x,y-2)]

    def get_next_head(self):
        """return next coordinate for head of snake"""
        tmp = self.__head
        
        if self.__dir == "Up":
            next_head = (tmp[0],tmp[1]+1)
        elif self.__dir == "Right":
            next_head = (tmp[0]+1,tmp[1])
        elif self.__dir == "Down":
            next_head = (tmp[0],tmp[1]-1)
        elif self.__dir == "Left":
            next_head = (tmp[0]-1,tmp[1])
        
        return next_head

    def grow_snake(self):
        """adding a new head to snake"""       
        new_head = self.get_next_head()
        self.__head = new_head
        self.__body = [new_head] + self.__body
        self.__length += 1

    def remove_head(self):
        self.__body = self.__body[1:]

    def is_self_collapsed(self):
        """check if snake hit itself"""
        return self.__head in self.__body[1:]

    def move_snake(self):
        
        index = len(self.__body)-1
        for i in self.__body[:0:-1]: #iterate from end to beginning excluding head
            self.__body[index] = self.__body[index-1] 
            index -= 1
        next_head = self.get_next_head()
        #update next head
        self.__body[0] = next_head
        self.__head = next_head
        

    def slice_snake(self,min_hit_index):
        self.__body = self.__body[:min_hit_index]
        self.__length = len(self.__body)


    def get_body(self):
        return self.__body

    def get_head(self):
        return self.__head

    def get_color(self):
        return self.__color

    def get_dir(self):
        return self.__dir

    def get_length(self):
        return self.__length
        
    def set_dir(self, dir):       
        self.__dir = dir


