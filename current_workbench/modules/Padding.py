
class Padding:
    """This class is used to set padding values for a rectangular area."""
    def __init__(self, top:float=0, bottom:float=0, right:float=0, left:float=0) -> None:
        """
        Initializes a new object of the Padding class.

        args:
            top (float): The top padding value. Default is 0.
            bottom (float): The bottom padding value. Default is 0.
            right (float): The right padding value. Default is 0.
            left (float): The left padding value. Default is 0.
        """
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left

    def __repr__(self) -> str:
        """
        Returns a string representing the object.

         Returns:
             str: A string representing the object with top, bottom, right, and left padding values.
        """
        return f"(top: {self.top}, bottom: {self.bottom}, right: {self.right}, left: {self.left})"