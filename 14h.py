import tkinter


HEIGHT = 103
WIDTH = 101


class Robot:

    def __init__(self, i: int, j: int, di: int, dj: int):
        self.i = i
        self.j = j
        self.di = di
        self.dj = dj

    @classmethod
    def from_input(cls, data: str):
        position, velocity = data.split()
        j, i = map(int, position.removeprefix("p=").split(","))
        dj, di = map(int, velocity.removeprefix("v=").split(","))
        return Robot(i, j, di, dj)

    def destination(self, n: int):
        """
        Return this robot's location after moving for `n` seconds.

        Represent this information as a new Robot object with the same
        `di` and `dj`."""
        i = (self.i + (n * self.di)) % HEIGHT
        j = (self.j + (n * self.dj)) % WIDTH
        return Robot(i, j, self.di, self.dj)


class AreaDisplay(tkinter.Tk):

    def __init__(self):
        super().__init__()
        with open("t.txt") as file:
            self.robots = [
                Robot.from_input(robot) for robot in file.read().splitlines()
            ]
        self.n = 0
        self.canvas = tkinter.Canvas(self, height=HEIGHT * 5, width=WIDTH * 5)
        self.canvas.grid(row=0, column=0)
        self.control_frame = tkinter.Frame(self)
        self.control_frame.grid(row=1, column=0)
        self.left_button = tkinter.Button(self.control_frame, text="<", command=self.left)
        self.left_button.grid(row=0, column=0)
        self.n_label = tkinter.Label(self.control_frame)
        self.n_label.grid(row=0, column=1)
        self.right_button = tkinter.Button(self.control_frame, text=">", command=self.right)
        self.right_button.grid(row=0, column=2)
        self.show()

    def show(self):
        """Show what the area looks like after `self.n` seconds."""
        self.canvas.delete(tkinter.ALL)
        for robot in self.robots:
            destination = robot.destination(self.n)
            self.canvas.create_rectangle(
                destination.j * 5,
                destination.i * 5,
                (destination.j + 1) * 5,
                (destination.i + 1) * 5,
            )
        self.n_label.config(text=str(self.n))

    def left(self):
        """Decrement `n`, then show what the area looks like."""
        self.n -= 1
        self.show()

    def right(self):
        """Increment `n`, then show what the area looks like."""
        self.n += 1
        self.show()


AreaDisplay().mainloop()


# This code was used to find the pattern by trial and error. Something
# interesting happens every 101 frames (134, 235, 336, etc.), and again
# every 103 frames (190, 293, 396, etc.). Triangulating these patterns
# gets the answer.
