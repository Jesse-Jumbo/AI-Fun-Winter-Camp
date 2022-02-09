import numpy as np
import random
from .QT import QLearningTable

class MLPlay:
    def __init__(self):
        self.ball_served = False
        self.ball_vel = (0, 0)
        self.ball_pos = (95, 400)
        self.platform_pos = (75, 400)
        self.previous_ball = (0, 0)
        self.step = 0
        self.reward = 0
        self.action = 0
        self.action_space = [["SERVE_TO_LEFT"], ["SERVE_TO_RIGHT"], ["MOVE_LEFT"], ["MOVE_RIGHT"], ["NONE"]]
        self.n_actions = len(self.action_space)
        self.n_features = 2
        self.RL = QLearningTable(actions=list(range(self.n_actions)))        
        self.observation = 0
        self.status = "GAME_ALIVE"
        self.state = [self.observation]
        self.state_ = [self.observation]

        print("Initial ml script")

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER" or scene_info["status"] == "GAME_PASS":
            return "RESET"
        
        # self.ball_vel_x = scene_info["ball"][0] - self.previous_ball[0]
        # self.ball_vel_y = scene_info["ball"][1] - self.previous_ball[1]
        # self.ball_pos_x = scene_info["ball"][0]
        # self.ball_pos_y = scene_info["ball"][1]
        # self.platform_1P = scene_info["platform"][0]

        def check():
            self.observation = 0

            '''
            example:
           # 球正在往上 & 球高於257時
            x_trend = self.previous_ball[0]-scene_info['ball'][0]  # 球x軸方向
            y_trend = self.previous_ball[1]-scene_info['ball'][1]  # 球y軸方向
            if scene_info["ball"][1] < 257:
          # x_trend > 0 球往左走 & 限制平在75~85間移動
            if(x_trend > 0 and scene_info['platform'][0] <= 90) and scene_info['ball'][0] >= 70:
                self.observation = 1
            '''

        def step(self, state):
            # reward function
            self.reward = 0
            
            '''
            you can design your reward function here !

            '''

            return self.reward

        self.previous_ball = scene_info["ball"]

        self.ball_vel_x = scene_info["ball"][0] - self.previous_ball[0]
        self.ball_vel_y = scene_info["ball"][1] - self.previous_ball[1]
        self.ball_pos_x = scene_info["ball"][0]
        self.ball_pos_y = scene_info["ball"][1]
        self.platform = scene_info["platform"][0]

        check()

        self.state_ = [self.observation]
        self.reward = step(self, self.state_)
        action = self.RL.choose_action(str(self.state))
        self.RL.learn(str(self.state), self.action, self.reward, str(self.state_))
        self.action = action
        self.state = self.state_
       
        if scene_info["status"] == "GAME_OVER" or scene_info["status"] == "GAME_PASS":
            return "RESET"
        
        return self.action_space[action]
        

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        print(self.RL.q_table)
        self.RL.q_table.to_pickle('games/arkanoid/log/qtable.pickle')
    #    self.RL.plot_cost()
        print("reset ml script")
        
        pass

