#################################################################
# FILE : apple.py
# WRITER1 : Yonatan Green , yonatan.green1 , 323865386
# WRITER2 : Guy Fussfeld , guyfussfeld , 207766973
# EXERCISE : intro2cs ex10 2022-2023
# DESCRIPTION: apple
#################################################################
class Apple:
    """This Class represents a simple apple
        containing single coordinate and color
    """
    def __init__(self, pos):
        self.__color = "green"
        self.__pos = pos

    def get_pos(self):
        return self.__pos

    def get_color(self):
        return self.__color
