class Padding:
    def __init__(self, top:float=0, bottom:float=0, right:float=0, left:float=0) -> None:
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left

    def __repr__(self) -> str:
        return f"(top: {self.top}, bottom: {self.bottom}, right: {self.right}, left: {self.left})"