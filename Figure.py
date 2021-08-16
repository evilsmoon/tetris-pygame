import random
colors = [
    (37, 235, 11),
    (160, 154, 143),
    (139, 176, 186),
    (57, 217, 227),
    (82, 30, 24),
    (13, 216, 46),
    (198, 39, 57)
]


class Figure:

    figures = [
        [[4, 5, 6, 7], [1, 5, 9, 13]],  # Linea
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # Piramide
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 8, 9], [4, 5, 6, 10]],  # L Derecha
        [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],  # L Izquierda
        [[5, 6, 9, 10]],  # Cuadrado
        [[1, 2, 4, 5], [0, 4, 5, 9], [5, 6, 8, 9],
         [1, 5, 6, 10]],  # zig-zag  Derecha
        [[1, 2, 6, 7], [3, 6, 7, 10], [5, 6, 10, 11],
         [2, 5, 6, 9]]  # zig-zag  Izquierda
    ]
 

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, (len(self.figures) - 1))
        self.color = random.randint(0, (len(colors) - 1))
        self.rotation = 0

    # gets the specific shape and color of currently falling object
    def get_image(self):
        return self.figures[self.type][self.rotation]

    # increments to the next rotation of any type of figure
    def rotate(self):
        self.rotation = (self.rotation + 1) % (len(self.figures[self.type]))
