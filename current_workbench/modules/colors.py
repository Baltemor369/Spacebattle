colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'gray': (128, 128, 128),
    'lightgray': (192, 192, 192),
    'darkgray': (64, 64, 64),
    'maroon': (128, 0, 0),
    'olive': (128, 128, 0),
    'navy': (0, 0, 128),
    'purple': (128, 0, 128),
    'teal': (0, 128, 128),
    'lime': (0, 128, 0),
    'aqua': (0, 255, 255),
    'fuchsia': (255, 0, 255),
    'silver': (192, 192, 192),
    'darkred': (139, 0, 0),
    'firebrick': (178, 34, 34),
    'brown': (165, 42, 42),
    'indianred': (205, 92, 92),
    'rosybrown': (188, 143, 143),
    'lightcoral': (240, 128, 128),
    'salmon': (250, 128, 114),
    'darksalmon': (233, 150, 122),
    'lightsalmon': (255, 160, 122),
    'coral': (255, 127, 80),
    'tomato': (255, 99, 71),
    'orangered': (255, 69, 0),
    'gold': (255, 215, 0),
    'orange': (255, 165, 0),
    'darkorange': (255, 140, 0),
    'khaki': (240, 230, 140),
    'yellowgreen': (154, 205, 50),
    'olivedrab': (107, 142, 35),
    'forestgreen': (34, 139, 34),
    'greenyellow': (173, 255, 47),
}

def RGB(color_str: str) -> tuple[int, int, int]:
    """
    Convert a color name in a RGB code.

    Args:
        color_str (str): a string represent the color name.

    Returns:
        Tuple[int, int, int]:  a tuple of integer corresponding to the color
    """

    color_str = color_str.lower()
    light =False
    dark =False

    if color_str.find("light ") != -1:
        color_str = color_str.replace("light ","")
        light = True
    
    if color_str.find("dark ") != -1:
        color_str = color_str.replace("dark ","")
        dark = True
    
    if color_str in colors:
        if light:
           return adjust_brightness(colors[color_str],160)
        elif dark:
            return adjust_brightness(colors[color_str],50)
        else:
            return colors[color_str]    
    else:
        return "color name is not valide or is not in our color list."
    
def adjust_brightness(color:tuple[int,int,int],brightness:int) -> tuple[int,int,int]:
    """
    Adjust the brightness of a color.

    Args:
    color (tuple[int,int,int]): a tuple of integer corresponding to the color.
    brightness (int): the brightness to adjust.

    Returns:
    tuple[int,int,int]: a tuple of integer corresponding to the adjusted color.
    """
    r,g,b = color
    new_r = 0
    new_g = 0
    new_b = 0
    bright_r = 0
    bright_g = 0
    bright_b = 0

    new_r = int(r * brightness / 120)

    if new_r > 255:
        bright_r = new_r - 255
        new_r = 255
    
    new_g = int(g * brightness / 120)
    
    if new_g > 255:
        bright_g = new_g - 255
        new_g = 255

    new_b = int(b * brightness / 120)

    if new_b > 255:
        bright_b = new_b - 255
        new_b = 255
    
    if 0 <= new_r < 255:
        new_r += max(bright_r, bright_g, bright_b)
    if 0 <= new_g < 255:
        new_g += max(bright_r, bright_g, bright_b)
    if 0 <= new_b < 255:
        new_b += max(bright_r, bright_g, bright_b)
    
    return (min(new_r,255), min(new_g,255), min(new_b,255))        