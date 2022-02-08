"""
The template of the main script of the machine learning process
"""
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pickle
import math

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.previous_ball = (0,0)
        #如果要換不同模型，可以改這個檔名，譬如knn.pickle則可以用KNN model
        # with open(os.path.join(os.path.dirname(__file__),'save','knn.pickle'), 'rb' ) as f:
        with open(os.path.join(os.path.dirname(__file__),'save','res.pickle'), 'rb' ) as f:
            self.model = pickle.load(f)
        print('init complete')


    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"
        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_RIGHT"
        else:
            ball_x = scene_info['ball'][0]
            ball_y = scene_info['ball'][1]
            speed_x = scene_info['ball'][0] - self.previous_ball[0]
            speed_y = scene_info['ball'][1] - self.previous_ball[1]

            if speed_x > 0:
                if speed_y > 0: Direction = 2
                else: Direction = 1
            else:
                if speed_y > 0:Direction = 2
                else: Direction = 3
            x = np.array([ball_x,ball_y,speed_x,speed_y,Direction]).reshape((1,-1))
            y = self.model.predict(x)
            #print(y)
            if scene_info['platform'][0]+20+5<y:
                command = 'MOVE_RIGHT'
            elif scene_info['platform'][0]+20-5 >y:
                command = 'MOVE_LEFT'
            else:
                command = 'NONE'

        self.previous_ball = scene_info['ball']
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False