#dataset generator for ml
import numpy as np
import pandas as pd
from tqdm import tqdm
from ball_game import ball_game

class dataset_generator(ball_game):
    def __init__(self):
        super().__init__()
        self.dataset_columns = ['target_x','target_y','vwall1_x','vwall1_y','vwall2_x','vwall2_y','vwall3_x','vwall3_y','hwall1_x','hwall1_y','hwall2_x','hwall2_y','hwall3_x','hwall3_y','vobstacle_x','vobstacle_y','hobstacle_x','hobstacle_y','action']
        self.dataset = pd.DataFrame(columns=self.dataset_columns)

    def mid_point(self, num0, num1, num2 = None):
        if num0 is None or num1 is None:
            return 0
        elif num2 == None:
            return int(num0 - num1)
        else:
            return int((num0 + num1) / 2 - num2)
        
    def get_state(self):
        tag_x = self.mid_point(self.target_x0, self.target_x1, self.x0)
        tag_y = self.mid_point(self.target_y, self.y0)
        vwal1_x = self.mid_point(self.vwall1_x, self.x0)
        vwal1_y = self.mid_point(self.vwall1_y0, self.vwall1_y1, self.y0)
        vwal2_x = self.mid_point(self.vwall2_x, self.x0)
        vwal2_y = self.mid_point(self.vwall2_y0, self.vwall2_y1, self.y0)
        vwal3_x = self.mid_point(self.vwall3_x, self.x0)
        vwal3_y = self.mid_point(self.vwall3_y0, self.vwall3_y1, self.y0)
        hwal1_x = self.mid_point(self.hwall1_x0, self.hwall1_x1, self.x0)
        hwal1_y = self.mid_point(self.hwall1_y, self.y0)
        hwal2_x = self.mid_point(self.hwall2_x0, self.hwall2_x1, self.x0)
        hwal2_y = self.mid_point(self.hwall2_y, self.y0)
        hwal3_x = self.mid_point(self.hwall3_x0, self.hwall3_x1, self.x0)
        hwal3_y = self.mid_point(self.hwall3_y, self.y0)
        vobst_x = self.mid_point(self.vobstacle_x, self.x0)
        vobst_y = self.mid_point(self.vobstacle_y0, self.vobstacle_y1, self.y0)
        hobst_x = self.mid_point(self.hobstacle_x0, self.hobstacle_x1, self.x0)
        hobst_y = self.mid_point(self.hobstacle_y, self.y0)
        return [tag_x, tag_y, vwal1_x, vwal1_y, vwal2_x, vwal2_y, vwal3_x, vwal3_y, hwal1_x, hwal1_y, hwal2_x, hwal2_y, hwal3_x, hwal3_y, vobst_x, vobst_y, hobst_x, hobst_y]

    def generate_data(self, repeat = 25000):
        for i in range(4):
            self.y0 = 20 * i
            for j in tqdm(range(repeat)):
                self.generate_map()
                state = self.get_state()
                act = []
                for k in range(181):
                    v0 = 20
                    theta_rad = np.deg2rad(k)
                    self.vx0 = v0*np.cos(theta_rad)
                    self.vy0 = v0*np.sin(theta_rad)
                    x1, y1 = self.lastposition(t=0)
                    if y1 > self.map_down:
                        act.append(k)
                if act == []:
                    act.append(181)
                self.nextseed()
                self.dataset.loc[len(self.dataset)] = state + [act]

if __name__ == '__main__':
    dg = dataset_generator()
    dg.generate_data(25000)
    dg.dataset.to_csv('bg_dataset.csv', index=False)
