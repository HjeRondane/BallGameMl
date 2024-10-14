#ball game ai
import numpy as np
from ball_game import ball_game
import joblib
import random
import warnings

class ballgame_ai(ball_game):
    def __init__(self):
        super().__init__()
        self.model = joblib.load('bg_randomforest.pkl')
        self.mlb = joblib.load('bg_randomforest_mlb.pkl')

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
        return [tag_x, tag_y,
                vwal1_x, vwal1_y, vwal2_x, vwal2_y, vwal3_x, vwal3_y,
                hwal1_x, hwal1_y, hwal2_x, hwal2_y, hwal3_x, hwal3_y,
                vobst_x, vobst_y, hobst_x, hobst_y]

    def predict(self, state):
        state = [self.get_state()]
        prediction = self.model.predict(state)
        angles = self.mlb.inverse_transform(prediction)[0]
        if 181 in angles:
            return 'reset'
        elif type(angles) == tuple:
            if angles == ():
                return 'reset'
            else:
                return angles[0]
        else:
            return random.choice(angles)

    def run_game(self):
        reset_count = 0
        level_count = 0
        temp_reset = 0
        while self.life > 0:
            self.generate_map()
            while True:
                v0 = 20
                if temp_reset == 2:
                    theta = 'reset'
                    temp_reset = 0
                else:
                    theta = self.predict(self.get_state())
                if theta == 'reset':
                    self.nextseed()
                    reset_count += 1
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
                    temp_reset += 1
                    if self.life <= 0:
                        break
                else:
                    self.x0, self.y0 = round(x1), round(y1)
                    self.nextseed()
                    level_count += 1
                    break
        print(f'''Run die!
              your score is {self.y0:.1f} m
              reset count: {reset_count}
              level count: {level_count}
              ''')

if __name__ == '__main__':
    warnings.filterwarnings("ignore", message="X does not have valid feature names, but RandomForestClassifier was fitted with feature names")
    bg_ai = ballgame_ai()
    print(bg_ai.seed)
    bg_ai.run_game()
    
