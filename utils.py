class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x},{self.y})"

    def fromStr(self, str):
        self.x, self.y = eval(str)

if __name__ == "__main__":
    print("This module is not for direct call!")