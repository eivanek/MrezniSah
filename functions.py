import pygame as pg


def array_to_move(x, y):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    move = ""
    x += 1
    y += 1
    move += letters[y]
    if x == 7:
        x = 1
    elif x == 6:
        x = 2
    elif x == 5:
        x = 3
    elif x == 3:
        x = 5
    elif x == 2:
        x = 6
    elif x == 1:
        x = 7
    elif x == 0:
        x = 8
    move += str(x)
    return move

def get_image_figure(name, resolution):
    resolution = resolution // 8
    img_name = 'slike/' + name + '.png'
    image = pg.image.load(img_name)
    image = pg.transform.scale(image, resolution)
    return image

def convert_coordinates_to_array(x, y, square_size):
    x = 0
    y = 0
    ss_1 = square_size
    ss_2 = 0
    for i in range(0, 8):
        if x <= ss_1:
            y = ss_2
            break
        else:
            ss_1 += square_size
            ss_2 += 1
    ss_1 = square_size
    ss_2 = 0
    for i in range(0, 8):
        if y <= ss_1:
            x = ss_2
            break
        else:
            ss_1 += square_size
            ss_2 += 1
    return x, y
