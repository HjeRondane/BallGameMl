#origial code
import numpy as np
import matplotlib.pyplot as plt
import random as rd
from matplotlib import animation

x0, y0 = 0, 0
x, y = 0, 0
g=9.8
dt = 0.01
brad = 0.3
life = 30

#obstacle & target
def hwall(ml, mr, md1, mu1):
    x = rd.randrange(ml,mr)
    x1, x2 = x-2, x+2
    y = rd.randrange(md1, mu1)
    return x1, x2, y

def vwall(ml, mr, md1, mu1):
    x = rd.randrange(ml,mr)
    y = rd.randrange(md1, mu1)
    y1, y2 = y-2, y+2
    return x, y1, y2

def target(ml, mr, md1, mu1):
    tagx = rd.randrange(ml,mr)
    tagx1 = tagx - 1
    tagx2 = tagx + 1
    tagy = rd.randrange(md1,mu1)
    return tagx1, tagx2, tagy

def hit_constant(v):
    Brad = brad
    if v**2 < 10:
        c = 0.1
    elif v**2 < 50:
        c = 0.3
    elif v**2 < 100:
        c = 0.5
    elif v**2 < 200:
        c = 0.7
    elif v**2 < 350:
        c = 0.9
    elif v**2 < 500:
        c = 1
    else:
        c = 1.3
    return c*Brad

def hit_hwall(x, y, wx1, wx2, wy, vx, vy):
    if y < wy+hit_constant(vy) and y > wy-hit_constant(vy) and x < wx2+hit_constant(vx) and x> wx1-hit_constant(vx):
        return True

def hit_vwall(x, y, wx, wy1, wy2, vx, vy):
    if x < wx+hit_constant(vx) and x > wx-hit_constant(vx) and y < wy2+hit_constant(vy) and y> wy1-hit_constant(vy):
        return True

def hit_target(x, y, tagx1, tagx2, tagy, vx, vy):
    if y < tagy+hit_constant(vy) and y > tagy-hit_constant(vy) and x < tagx2+hit_constant(vx) and x> tagx1-hit_constant(vx):
            if vy <= 0:
                return 'up'
            else:
                return 'down'

#lastposition
def lastposition(t=0):
    x, y, vx, vy, G = x0, y0, vx0, vy0, g
    while y>=md:
        t += dt
        vy -= G * dt
        x += vx*dt
        y += vy*dt
        if x < ml or x > mr:
            vx = -vx
        wx, wx1, wx2, wy, wy1, wy2 = wxa, wx1a, wx2a, wya, wy1a, wy2a
        if hit_hwall(x, y, wx1, wx2, wy, vx, vy):
            vy = -vy
        if hit_vwall(x, y, wx, wy1, wy2, vx, vy):
            vx = -vx
        if y0>=20:
            wx, wx1, wx2, wy, wy1, wy2 = wxb, wx1b, wx2b, wyb, wy1b, wy2b
            if hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                vy = -vy
            if hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                vx = -vx
        if y0>=40:
            wx, wx1, wx2, wy, wy1, wy2 = wxc, wx1c, wx2c, wyc, wy1c, wy2c
            if hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                vy = -vy
            if hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                vx = -vx
        if y0>=60:
            wx, wx1, wx2, wy, wy1, wy2 = obx, obx1, obx2, oby, oby1, oby2
            if hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                x, y = x0, y0
                break
            if hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                x, y = x0, y0
                break
        if hit_target(x, y, tagx1, tagx2, tagy, vx, vy) == 'up':
            break
        if hit_target(x, y, tagx1, tagx2, tagy, vx, vy) == 'down':
            vy = -vy
    return x, y

#animation function
def move(t=0):
    x, y, vx, vy, G = x0, y0, vx0, vy0, g
    while y>=md:
        t += dt
        vy -= G * dt
        x += vx*dt
        y += vy*dt
        if x < ml or x > mr:
            vx = -vx
        wx, wx1, wx2, wy, wy1, wy2 = wxa, wx1a, wx2a, wya, wy1a, wy2a
        if hit_hwall(x, y, wx1, wx2, wy, vx, vy):
            vy = -vy
        if hit_vwall(x, y, wx, wy1, wy2, vx, vy):
            vx = -vx
        if y0>=20:
            wx, wx1, wx2, wy, wy1, wy2 = wxb, wx1b, wx2b, wyb, wy1b, wy2b
            if hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                vy = -vy
            if hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                vx = -vx
        if y0>=40:
            wx, wx1, wx2, wy, wy1, wy2 = wxc, wx1c, wx2c, wyc, wy1c, wy2c
            if hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                vy = -vy
            if hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                vx = -vx
        if y0>=60:
            wx, wx1, wx2, wy, wy1, wy2 = obx, obx1, obx2, oby, oby1, oby2
            if hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                vx = 0
                vy, G = 0, 0
            if hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                vx = 0
                vy, G = 0, 0
        if hit_target(x, y, tagx1, tagx2, tagy, vx, vy) == 'up':
            vx = 0
            vy, G = 0, 0
        if hit_target(x, y, tagx1, tagx2, tagy, vx, vy) == 'down':
            vy = -vy
        yield x, y

def init():
    ax.set_xlim(ml,mr)
    ax.set_ylim(md,mu)
    line.set_data(xdata, ydata)
    ball.set_center((x0, y0))
    return line, ball

def animate(position):
    x, y = position
    xdata.append(x)
    ydata.append(y)
    line.set_data(xdata, ydata)
    ball.set_center((x, y))
    return line, ball

#main fuction
if __name__ == '__main__':
    print('        ☆Ball game☆')
    print('''           ▼rule▼
1. Check target location
2. Enter launch angle(0~180)
    [launch speed is 20 m/s]
3. If you reach on the target, continue to challenge
4. If you falls off the screen or hit red wall, life -1
5. Run ends when life is 0''')
    while life > 0:
        #map generate
        mr, ml, mu, md = x0+11, x0-11, y0+20, y0 #size
        md1, mu1 = md+1, mu-3
        tagx1, tagx2, tagy = target(ml, mr, md1, mu1)
        wx1a, wx2a, wya = hwall(ml, mr, md1, mu1)
        wxa, wy1a, wy2a = vwall(ml, mr, md1, mu1)
        if y0 >= 20:
            wx1b, wx2b, wyb = hwall(ml, mr, md1, mu1)
            wxb, wy1b, wy2b = vwall(ml, mr, md1, mu1)
        if y0 >= 40:
            wx1c, wx2c, wyc = hwall(ml, mr, md1, mu1)
            wxc, wy1c, wy2c = vwall(ml, mr, md1, mu1)
        if y0 >= 60:
            obx1, obx2, oby = hwall(ml, mr, md1, mu1)
            obx, oby1, oby2 = vwall(ml, mr, md1, mu1)
        #display map
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.set_xlim(ml,mr)
        ax.set_ylim(md,mu)
        ax.plot([wx1a,wx2a],[wya,wya],'k' ,label='wall', lw = 1.6)
        ax.plot([wxa,wxa],[wy1a,wy2a],'k' ,label='wall', lw = 1.6)
        if y0 >= 20:
            ax.plot([wx1b,wx2b],[wyb,wyb],'k' ,label='wall', lw = 1.6)
            ax.plot([wxb,wxb],[wy1b,wy2b],'k' ,label='wall', lw = 1.6)
        if y0 >= 40:
            ax.plot([wx1c,wx2c],[wyc,wyc],'k' ,label='wall', lw = 1.6)
            ax.plot([wxc,wxc],[wy1c,wy2c],'k' ,label='wall', lw = 1.6)
        if y0 >= 60:
            ax.plot([obx1,obx2],[oby,oby],'r' ,label='obstacle', lw = 1.6)
            ax.plot([obx,obx],[oby1,oby2],'r' ,label='obstacle', lw = 1.6)
        ax.plot([tagx1,tagx2],[tagy,tagy],'b' ,label='target', lw = 1.6)
        ax.plot(x0, y0, 'ko')
        height_text = ax.text(x0+1, y0+16, f'Score (Height): {y0:.1f} m')
        life_text = ax.text(x0+5.3, y0+15, f'life: {life:.0f}')
        plt.show()
        while True:
            #get initial condition
            v0 = 20
            theta = (input('theta?: '))
            if theta == 'reset': #reset button
                print('round reset')
                break
            else:
                theta = int(theta)
            theta_rad = np.deg2rad(theta)
            vx0 = v0*np.cos(theta_rad)
            vy0 = v0*np.sin(theta_rad)
            #animation
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
            line, = ax.plot([], [], lw=0.1)
            ball = plt.Circle((x0, y0), brad)
            height_text = ax.text(x0+1, y0+16, f'Score (Height): {y0:.1f} m')
            life_text = ax.text(x0+5.3, y0+15, f'life: {life:.0f}')
            ax.add_patch(ball)
            xdata, ydata = [], []
            ax.plot([wx1a,wx2a],[wya,wya],'k' ,label='wall', lw = 1.6)
            ax.plot([wxa,wxa],[wy1a,wy2a],'k' ,label='wall', lw = 1.6)
            if y0 >= 20:
                ax.plot([wx1b,wx2b],[wyb,wyb],'k' ,label='wall', lw = 1.6)
                ax.plot([wxb,wxb],[wy1b,wy2b],'k' ,label='wall', lw = 1.6)
            if y0 >= 40:
                ax.plot([wx1c,wx2c],[wyc,wyc],'k' ,label='wall', lw = 1.6)
                ax.plot([wxc,wxc],[wy1c,wy2c],'k' ,label='wall', lw = 1.6)
            if y0 >= 60:
                ax.plot([obx1,obx2],[oby,oby],'r' ,label='obstacle', lw = 1.6)
                ax.plot([obx,obx],[oby1,oby2],'r' ,label='obstacle', lw = 1.6)
            ax.plot([tagx1,tagx2],[tagy,tagy],'b' ,label='target', lw = 1.6)
            anim = animation.FuncAnimation(fig, animate, move, blit=True, interval=dt*180, repeat=False, init_func=init)
            plt.show()
            #rule
            x1, y1 = lastposition(t=0)
            if y1 <= md:
                life -= 1
                if life <= 0:
                    break
            else:
                x0, y0 = round(x1), round(y1)
                print('good')
                break
    print ('Run die!')
    print (f'Your Score(Height) is {y0:.1f} m')
