#code adj for ml
import numpy as np
import matplotlib.pyplot as plt
import random as rd
from matplotlib import animation

class ball_game:
    def __init__(self):
        self.x0, self.y0 = 0, 0
        self.x, self.y = 0, 0
        self.vx0, self.vy0 = 0, 0
        self.map_down, self.map_up, self.map_left, self.map_right = 0, 0, 0, 0
        self.g=9.8
        self.dt = 0.01
        self.brad = 0.3
        self.life = 10
        self.seed = rd.randint(0, 1000000)
        self.rng = rd.Random(self.seed)

    def nextseed(self):
        self.seed += 1
        self.rng = rd.Random(self.seed)

#obstacle & target
    def hwall(self, ml, mr, md1, mu1):
        x = self.rng.randint(ml,mr)
        x1, x2 = x-2, x+2
        y = self.rng.randint(md1, mu1)
        return x1, x2, y

    def vwall(self, ml, mr, md1, mu1):
        x = self.rng.randint(ml,mr)
        y = self.rng.randint(md1, mu1)
        y1, y2 = y-2, y+2
        return x, y1, y2

    def target(self, ml, mr, md1, mu1):
        tagx = self.rng.randint(ml,mr)
        tagx1 = tagx - 1
        tagx2 = tagx + 1
        tagy = self.rng.randint(md1,mu1)
        return tagx1, tagx2, tagy

    def hit_constant(self, v):
        Brad = self.brad
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

    def hit_hwall(self, x, y, wx1, wx2, wy, vx, vy):
        if y < wy+self.hit_constant(vy) and y > wy-self.hit_constant(vy) and x < wx2+self.hit_constant(vx) and x> wx1-self.hit_constant(vx):
            return True

    def hit_vwall(self, x, y, wx, wy1, wy2, vx, vy):
        if x < wx+self.hit_constant(vx) and x > wx-self.hit_constant(vx) and y < wy2+self.hit_constant(vy) and y> wy1-self.hit_constant(vy):
            return True

    def hit_target(self, x, y, tagx1, tagx2, tagy, vx, vy):
        if y < tagy+self.hit_constant(vy) and y > tagy-self.hit_constant(vy) and x < tagx2+self.hit_constant(vx) and x> tagx1-self.hit_constant(vx):
                if vy <= 0:
                    return 'up'
                else:
                    return 'down'

    #lastposition
    def lastposition(self, t=0):
        x, y, vx, vy, G = self.x0, self.y0, self.vx0, self.vy0, self.g
        while y>=self.map_down:
            t += self.dt
            vy -= G * self.dt
            x += vx*self.dt
            y += vy*self.dt
            if x < self.map_left or x > self.map_right:
                vx = -vx
            wx, wx1, wx2, wy, wy1, wy2 = self.vwall1_x, self.hwall1_x0, self.hwall1_x1, self.hwall1_y, self.vwall1_y0, self.vwall1_y1
            if self.hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                vy = -vy
            if self.hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                vx = -vx
            if self.y0>=20:
                wx, wx1, wx2, wy, wy1, wy2 = self.vwall2_x, self.hwall2_x0, self.hwall2_x1, self.hwall2_y, self.vwall2_y0, self.vwall2_y1
                if self.hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                    vy = -vy
                if self.hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                    vx = -vx
            if self.y0>=40:
                wx, wx1, wx2, wy, wy1, wy2 = self.vwall3_x, self.hwall3_x0, self.hwall3_x1, self.hwall3_y, self.vwall3_y0, self.vwall3_y1
                if self.hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                    vy = -vy
                if self.hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                    vx = -vx
            if self.y0>=60:
                wx, wx1, wx2, wy, wy1, wy2 = self.vobstacle_x, self.hobstacle_x0, self.hobstacle_x1, self.hobstacle_y, self.vobstacle_y0, self.vobstacle_y1
                if self.hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                    x, y = self.x0, self.y0
                    break
                if self.hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                    x, y = self.x0, self.y0
                    break
            if self.hit_target(x, y, self.target_x0, self.target_x1, self.target_y, vx, vy) == 'up':
                break
            if self.hit_target(x, y, self.target_x0, self.target_x1, self.target_y, vx, vy) == 'down':
                vy = -vy
        return x, y

    #animation function
    def move(self, t=0):
        x, y, vx, vy, G = self.x0, self.y0, self.vx0, self.vy0, self.g
        while y>=self.map_down:
            t += self.dt
            vy -= G * self.dt
            x += vx*self.dt
            y += vy*self.dt
            if x < self.map_left or x > self.map_right:
                vx = -vx
            wx, wx1, wx2, wy, wy1, wy2 = self.vwall1_x, self.hwall1_x0, self.hwall1_x1, self.hwall1_y, self.vwall1_y0, self.vwall1_y1
            if self.hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                vy = -vy
            if self.hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                vx = -vx
            if self.y0>=20:
                wx, wx1, wx2, wy, wy1, wy2 = self.vwall2_x, self.hwall2_x0, self.hwall2_x1, self.hwall2_y, self.vwall2_y0, self.vwall2_y1
                if self.hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                    vy = -vy
                if self.hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                    vx = -vx
            if self.y0>=40:
                wx, wx1, wx2, wy, wy1, wy2 = self.vwall3_x, self.hwall3_x0, self.hwall3_x1, self.hwall3_y, self.vwall3_y0, self.vwall3_y1
                if self.hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                    vy = -vy
                if self.hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                    vx = -vx
            if self.y0>=60:
                wx, wx1, wx2, wy, wy1, wy2 = self.vobstacle_x, self.hobstacle_x0, self.hobstacle_x1, self.hobstacle_y, self.vobstacle_y0, self.vobstacle_y1
                if self.hit_hwall(x, y, wx1, wx2, wy, vx, vy):
                    vx = 0
                    vy, G = 0, 0
                if self.hit_vwall(x, y, wx, wy1, wy2, vx, vy):
                    vx = 0
                    vy, G = 0, 0
            if self.hit_target(x, y, self.target_x0, self.target_x1, self.target_y, vx, vy) == 'up':
                vx = 0
                vy, G = 0, 0
            if self.hit_target(x, y, self.target_x0, self.target_x1, self.target_y, vx, vy) == 'down':
                vy = -vy
            yield x, y

    def generate_map(self):
        self.map_right, self.map_left, self.map_up, self.map_down = self.x0+11, self.x0-11, self.y0+20, self.y0 #size
        md1, mu1 = self.map_down+1, self.map_up-3
        self.target_x0, self.target_x1, self.target_y = self.target(self.map_left, self.map_right, md1, mu1)
        self.hwall1_x0, self.hwall1_x1, self.hwall1_y = self.hwall(self.map_left, self.map_right, md1, mu1)
        self.vwall1_x, self.vwall1_y0, self.vwall1_y1 = self.vwall(self.map_left, self.map_right, md1, mu1)
        self.hwall2_x0, self.hwall2_x1, self.hwall2_y = None, None, None
        self.vwall2_x, self.vwall2_y0, self.vwall2_y1 = None, None, None
        self.hwall3_x0, self.hwall3_x1, self.hwall3_y = None, None, None
        self.vwall3_x, self.vwall3_y0, self.vwall3_y1 = None, None, None
        self.hobstacle_x0, self.hobstacle_x1, self.hobstacle_y = None, None, None
        self.vobstacle_x, self.vobstacle_y0, self.vobstacle_y1 = None, None, None
        if self.y0 >= 20:
            self.hwall2_x0, self.hwall2_x1, self.hwall2_y = self.hwall(self.map_left, self.map_right, md1, mu1)
            self.vwall2_x, self.vwall2_y0, self.vwall2_y1 = self.vwall(self.map_left, self.map_right, md1, mu1)
        if self.y0 >= 40:
            self.hwall3_x0, self.hwall3_x1, self.hwall3_y = self.hwall(self.map_left, self.map_right, md1, mu1)
            self.vwall3_x, self.vwall3_y0, self.vwall3_y1 = self.vwall(self.map_left, self.map_right, md1, mu1)
        if self.y0 >= 60:
            self.hobstacle_x0, self.hobstacle_x1, self.hobstacle_y = self.hwall(self.map_left, self.map_right, md1, mu1)
            self.vobstacle_x, self.vobstacle_y0, self.vobstacle_y1 = self.vwall(self.map_left, self.map_right, md1, mu1)

    def display_map(self):
        fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.ax.set_xlim(self.map_left,self.map_right)
        self.ax.set_ylim(self.map_down,self.map_up)
        self.ax.plot([self.hwall1_x0,self.hwall1_x1],[self.hwall1_y,self.hwall1_y],'k' ,label='wall', lw = 1.6)
        self.ax.plot([self.vwall1_x,self.vwall1_x],[self.vwall1_y0,self.vwall1_y1],'k' ,label='wall', lw = 1.6)
        if self.y0 >= 20:
            self.ax.plot([self.hwall2_x0,self.hwall2_x1],[self.hwall2_y,self.hwall2_y],'k' ,label='wall', lw = 1.6)
            self.ax.plot([self.vwall2_x,self.vwall2_x],[self.vwall2_y0,self.vwall2_y1],'k' ,label='wall', lw = 1.6)
        if self.y0 >= 40:
            self.ax.plot([self.hwall3_x0,self.hwall3_x1],[self.hwall3_y,self.hwall3_y],'k' ,label='wall', lw = 1.6)
            self.ax.plot([self.vwall3_x,self.vwall3_x],[self.vwall3_y0,self.vwall3_y1],'k' ,label='wall', lw = 1.6)
        if self.y0 >= 60:
            self.ax.plot([self.hobstacle_x0,self.hobstacle_x1],[self.hobstacle_y,self.hobstacle_y],'r' ,label='obstacle', lw = 1.6)
            self.ax.plot([self.vobstacle_x,self.vobstacle_x],[self.vobstacle_y0,self.vobstacle_y1],'r' ,label='obstacle', lw = 1.6)
        self.ax.plot([self.target_x0,self.target_x1],[self.target_y,self.target_y],'b' ,label='target', lw = 1.6)
        self.ax.plot(self.x0, self.y0, 'ko')
        height_text = self.ax.text(self.x0+1, self.y0+16, f'Score (Height): {self.y0:.1f} m')
        life_text = self.ax.text(self.x0+5.3, self.y0+15, f'life: {self.life:.0f}')
        plt.show()


    def init(self):
        self.ax.set_xlim(self.map_left,self.map_right)
        self.ax.set_ylim(self.map_down,self.map_up)
        self.line.set_data(self.xdata, self.ydata)
        self.ball.set_center((self.x0, self.y0))
        return self.line, self.ball

    def animate(self, position):
        x, y = position
        self.xdata.append(x)
        self.ydata.append(y)
        self.line.set_data(self.xdata, self.ydata)
        self.ball.set_center((x, y))
        return self.line, self.ball
    
    def animation(self):
        fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.line, = self.ax.plot([], [], lw=0.1)
        self.ball = plt.Circle((self.x0, self.y0), self.brad)
        height_text = self.ax.text(self.x0+1, self.y0+16, f'Score (Height): {self.y0:.1f} m')
        life_text = self.ax.text(self.x0+5.3, self.y0+15, f'life: {self.life:.0f}')
        self.ax.add_patch(self.ball)
        self.xdata, self.ydata = [], []
        self.ax.plot([self.hwall1_x0,self.hwall1_x1],[self.hwall1_y,self.hwall1_y],'k' ,label='wall', lw = 1.6)
        self.ax.plot([self.vwall1_x,self.vwall1_x],[self.vwall1_y0,self.vwall1_y1],'k' ,label='wall', lw = 1.6)
        if self.y0 >= 20:
            self.ax.plot([self.hwall2_x0,self.hwall2_x1],[self.hwall2_y,self.hwall2_y],'k' ,label='wall', lw = 1.6)
            self.ax.plot([self.vwall2_x,self.vwall2_x],[self.vwall2_y0,self.vwall2_y1],'k' ,label='wall', lw = 1.6)
        if self.y0 >= 40:
            self.ax.plot([self.hwall3_x0,self.hwall3_x1],[self.hwall3_y,self.hwall3_y],'k' ,label='wall', lw = 1.6)
            self.ax.plot([self.vwall3_x,self.vwall3_x],[self.vwall3_y0,self.vwall3_y1],'k' ,label='wall', lw = 1.6)
        if self.y0 >= 60:
            self.ax.plot([self.hobstacle_x0,self.hobstacle_x1],[self.hobstacle_y,self.hobstacle_y],'r' ,label='obstacle', lw = 1.6)
            self.ax.plot([self.vobstacle_x,self.vobstacle_x],[self.vobstacle_y0,self.vobstacle_y1],'r' ,label='obstacle', lw = 1.6)
        self.ax.plot([self.target_x0,self.target_x1],[self.target_y,self.target_y],'b' ,label='target', lw = 1.6)
        anim = animation.FuncAnimation(fig, self.animate, self.move, blit=True, interval=self.dt*180, repeat=False, init_func=self.init, cache_frame_data=False)
        plt.show()
    
    def main_loop(self):
        while self.life > 0:
            self.generate_map()
            self.display_map()
            while True:
                v0 = 20
                theta = (input('theta?: '))
                if theta == 'reset': #reset button
                    self.nextseed()
                    print('round reset')
                    break
                else:
                    theta = int(theta)
                theta_rad = np.deg2rad(theta)
                self.vx0 = v0*np.cos(theta_rad)
                self.vy0 = v0*np.sin(theta_rad)
                self.animation()
                x1, y1 = self.lastposition(t=0)
                if y1 <= self.map_down:
                    self.life -= 1
                    if self.life <= 0:
                        break
                else:
                    self.x0, self.y0 = round(x1), round(y1)
                    self.nextseed()
                    print('good')
                    break


#main fuction
if __name__ == '__main__':
    bg = ball_game()
    print('        ☆Ball game☆')
    print('''           ▼rule▼
1. Check target location
2. Enter launch angle(0~180)
    [launch speed is 20 m/s]
3. If you reach on the target, continue to challenge
4. If you falls off the screen or hit red wall, life -1
5. Run ends when life is 0''')
    bg.main_loop()
    print ('Run die!')
    print (f'Your Score(Height) is {bg.y0:.1f} m')
