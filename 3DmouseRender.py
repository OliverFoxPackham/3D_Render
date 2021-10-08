import pygame
import math

draw = False
thetaX = 0
thetaY = 0
thetaZ = 0
width = 1100
height = 800
# view only needs z
# view is always orthoganal (=perpindicular) to plane of projection
# it is not nessasaraly the same distance from it however
view = (500)
win = pygame.display.set_mode([width,height])
run = True

def main():
    clock = pygame.time.Clock()
    global run
    global view
    global draw
    global thetaX
    global thetaY
    global thetaZ
    win.fill((150,200,200))
    while run:
        clock.tick(60)
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Sense mouse
            if (event.type == pygame.MOUSEBUTTONDOWN):#zoom in and out
                if event.button == 4:
                    view -= 10
                if event.button == 5:
                    view += 10
                if event.button == 1:
                    clickedx,clickedy = pygame.mouse.get_pos()

        # Drag mouse
        if (pygame.mouse.get_pressed(num_buttons=3)[0]):
            mx,my = pygame.mouse.get_pos()
            thetaY += (-mx+clickedx)/170
            thetaX += (-my+clickedy)/170
            clickedx = mx
            clickedy = my

        # rotate around Z
        pressedkeys = pygame.key.get_pressed()
        if pressedkeys[pygame.K_j]:
            thetaZ -= .01
        if pressedkeys[pygame.K_l]:
            thetaZ += .01


        win.fill((150,200,200))
        updateScreen()
    pygame.quit()

def updateScreen():
    for point in range(len(projPoints())):
        pygame.draw.circle(win,(0,0,0),(projPoints()[point]), 4)
    pygame.display.update()

def projPoints():
    pointlist = getPoints()
    newpointlist = []
    for point in pointlist:

        # Rotate around
        rotatex = rotateX(point,thetaX)
        rotatey = rotateY(rotatex,thetaY)
        rotatez = rotateZ(rotatey,thetaZ)

        # project onto window
        # vector "viewToPoint" = point-view = (point[x]-view[x],point[y]-view[x],point[z]-view[z])
        # the line between them is b+mx = view + (time * viewToPoint)
        # the point along the line intersecting the window (at z=0) we take for t = point of intersect
        # time is -view[z]/(point[z]-view[z]) and the intersect is (t * viewToPoint) + view = 0
        newpointx= -view*rotatez[0]/(rotatez[2]-view)
        newpointy= -view*rotatez[1]/(rotatez[2]-view)

        # center view
        newpoint = (newpointx+width/2,newpointy+height/2)
        newpointlist.append(newpoint)
    return (newpointlist)

def rotateX(point,thetaX):
    newx = point[0]
    newy = point[1]*math.cos(thetaX)-point[2]*math.sin(thetaX)
    newz = point[2]*math.cos(thetaX)+point[1]*math.sin(thetaX)
    return (newx,newy,newz)

def rotateY(point,thetaY):
    newx = point[0]*math.cos(thetaY)-point[2]*math.sin(thetaY)
    newy = point[1]
    newz = point[2]*math.cos(thetaY)+point[0]*math.sin(thetaY)
    return (newx,newy,newz)

def rotateZ(point,thetaZ):
    newx = point[0]*math.cos(thetaZ)-point[1]*math.sin(thetaZ)
    newy = point[1]*math.cos(thetaZ)+point[0]*math.sin(thetaZ)
    newz = point[2]
    return (newx,newy,newz)

def getPoints():
    #return ((0,100,0),(0,-100,0),(100,0,0),(-100,0,0),(0,0,100),(0,0,-100))
    return ((100,100,100),(-100,100,100),(100,-100,100),(-100,-100,100),
    (100,100,-100),(-100,100,-100),(100,-100,-100),(-100,-100,-100))


main()
