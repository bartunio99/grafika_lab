import math

import random

from Cube import *
from Ground import *

is_jumping = False
initial_jump_height = 2.0
jump_height = initial_jump_height
jumping_duration = 0
falling_duration = 0

def jump():
    global is_jumping, jump_height, jumping_duration, falling_duration, initial_jump_height
    if not is_jumping and falling_duration == 0:
        is_jumping = True
        jump_height = initial_jump_height
        pygame.time.set_timer(pygame.USEREVENT, 10)
        glTranslatef(0, -4, 0)

def fall():
    global falling_duration
    falling_duration += 0.2
    glTranslatef(0, -0.2, 0)

def handle_jump():
    global is_jumping, jump_height, jumping_duration, falling_duration
    if is_jumping:
        glTranslatef(0, 0.1, 0)
        jump_height -= 0.1
        jumping_duration += 0.01
        if jump_height <= 0 or jumping_duration >= 1.0:
            is_jumping = False
            jump_height = initial_jump_height
            jumping_duration = 0
            falling_duration = 0
            pygame.time.set_timer(pygame.USEREVENT, 0)
            glTranslatef(0, initial_jump_height, 0)


#definicja wierzcholkow dla kazdego nowego szescianu
def set_vertices(max_distance, min_distance = -20):

    x_value_change = random.randrange(-19,19)
    y_value_change = random.randrange(0,1)
    z_value_change = random.randrange(-1*max_distance,min_distance)

    new_vertices = []

    for vert in Cube.vertices:
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)

    return new_vertices

def expandGround(max_distance):
    new_vertices = []
    for v in Ground.ground_vertices:
        new_v = []
        new_z = v[2] + 200

        new_v.append(v[0])
        new_v.append(v[1])
        new_v.append(new_z)

        new_vertices.append(new_v)

    return new_vertices


def light():
    posLight0 = [-1,1,1,0]
    ambLight0 = [0.5,0.5,0.5,0.5]
    difLight0 = [0.5,0.5,0.5,1]
    specLight0 = [0.5,0.5,0.5,1]
    glLightfv(GL_LIGHT0, GL_POSITION, posLight0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambLight0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, difLight0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specLight0)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10.0)


def collision(camera_x, camera_y, camera_z, vertices):
    #najblizsze punkty od gracza:
    x,y,z = getClosestPoint(vertices, [camera_x, camera_y, camera_z])

    distance = calculateSquareDistance(x,y,z,camera_x,camera_y,camera_z)
    return distance < 0.05


def calculateSquareDistance(x1,y1,z1,x2,y2,z2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)

def getClosestPoint(cube, camera):  #cube - lista wierzcholkow szescianu, camera - wsp kamery
    #ponizej sa wierzcholki zawierajace wartosci graniczne szescianu
    max_x = cube[0][0]
    min_x = cube[2][0]
    max_y = cube[1][1]
    min_y = cube[0][1]
    max_z = cube[4][2]
    min_z = cube[0][2]

    camera_x = camera[0]
    camera_y = camera[1]
    camera_z = camera[2]

    x1 = max(min_x, min(camera_x, max_x))
    y1 = max(min_y, min(camera_y, max_y))
    z1 = max(min_z, min(camera_z, max_z))

    return x1,y1,z1


def main():
    global is_jumping, initial_jump_height, jump_height, jumping_duration, falling_duration

    speed = 0.1
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)        #ustawienie wielkosci ekranu, informacja ze bedziemy uzywac opengl(doublebuf - podwojny bufor - do pracy z refresh rate monitora)
    glClearColor(0.53, 0.81, 0.92, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    max_distance = 100

    gluPerspective(45,display[0]/display[1], 0.1, max_distance)    #perspektywa  :FOV w stopniach,proporcje ekranu, clipping plane
    glTranslatef(0,0,-40)  #parametry x,y,z polozenia - mnozy obecna macierz przez translation matrix?

    x_move = 0
    y_move = 0


    cube_dict = {}  #slownik z szescianami

    for x in range(10):
        cube_dict[x] = set_vertices(max_distance)   #wypelnienie cube_dist

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = 0.3
                if event.key == pygame.K_RIGHT:
                    x_move = -0.3
                if event.key == pygame.K_UP:
                    jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0

            if event.type == pygame.USEREVENT:
                handle_jump()

        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)      #czyszczenie grafiki - bufor koloru i glebi - bufora grafiki - miejsce w ramie gdzie przetrzymywana jest obecna klatka
        # Kontrola obszaru granicznego
        if camera_x + x_move >= -30 and camera_x + x_move <= 30:
            glTranslatef(x_move, y_move, speed)
        elif camera_x + x_move < -30:
            glTranslatef(-camera_x - 30, y_move, speed)
        elif camera_x + x_move > 30:
            glTranslatef(30 - camera_x, y_move, speed)

        if falling_duration > 0:
            fall()

        g_vertices = [[-20,-1,camera_z+20], [-20,-1,camera_z-300], [20,-1,camera_z-300], [20,-1,camera_z+20]]
        boundary_1 = [[-20,-1,camera_z+20], [-20,-1,camera_z-300], [-20,8,camera_z-300], [-20,8,camera_z+20]]
        boundary_2 = [[20,-1,camera_z+20], [20,-1,camera_z-300], [20,8,camera_z-300], [20,8,camera_z+20]]
        Ground(g_vertices, boundary_1, boundary_2)
        light()

        for each_cube in cube_dict:
            Cube(cube_dict[each_cube])


        #generacja nowych szescianow
        for each_cube in cube_dict:
            if camera_z <= cube_dict[each_cube][0][2]:
                new_max = int(-1*(camera_z-(max_distance)*2))

                cube_dict[each_cube] = set_vertices(new_max, int(camera_z-max_distance)) #zastap obecna kostke, nowa w odpowiednim miejscu (po to jest new_max)

                speed += 0.001

            x = glGetDoublev(GL_MODELVIEW_MATRIX)
            camera_x = x[3][0]
            camera_y = x[3][1]
            camera_z = x[3][2]
            if(collision(-0.5*camera_x,camera_y,camera_z,cube_dict[each_cube])):
                pygame.quit()
                quit()

        pygame.display.flip()

if __name__ == "__main__":
    main()
