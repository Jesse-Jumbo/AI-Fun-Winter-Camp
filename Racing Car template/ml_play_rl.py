import numpy as np
from .Qtable import QLearningTable


class MLPlay:
    def __init__(self):
        self.car_pos = (20, 160)
        self.cars_pos = []
        self.car_lane = self.car_pos[1] // 50  # lanes 1 ~ 9
        self.step = 0
        self.reward = 0
        self.action = 0
        # 可自行定義有種action
        self.action_space = ["SPEED", "BRAKE"]
        self.n_actions = len(self.action_space)
        self.n_features = 2
        self.RL = QLearningTable(actions=list(range(self.n_actions)))
        self.observation = 0
        self.status = "ALIVE"
        # 可自行定義state
        self.state = [self.observation, ]
        self.state_ = [self.observation, ]

        print("Initial ml script")

    # 16 grid relative position  // 此16宮格可作為賽車相對位置之參考

    #      |    |    |    |    |    |
    #      |  1 |  2 |  3 |  4 |  5 |
    #      |    |    |    |    |    |
    #      |  6 |  c |  8 |  9 | 10 |
    #      |    |    |    |    |    |
    #      | 11 | 12 | 13 | 14 | 15 |
    #      |    |    |    |    |    |

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            return "RESET"

        def check_grid():
            self.observation = 0

            '''
            observation可以用來記錄車子狀態, 如下

            # car position
            x = scene_info["x"]
            y = scene_info["y"]

            if y <= 140: # lane 1
                self.observation = 1
            if y >= 490: # lane 9
                self.observation = 2
            '''

        def step(self, state):
            # reward function
            self.reward = 0

            '''
            you can design your reward function here !
            '''

            return self.reward

        check_grid()

        self.reward = step(self, self.state_)
        action = self.RL.choose_action(str(self.state))
        self.RL.learn(str(self.state), self.action, self.reward, str(self.state_))
        self.action = action
        self.state = self.state_

        if scene_info["status"] != "GAME_ALIVE" and scene_info["status"] != "ALIVE":
            return "RESET"

        if scene_info.__contains__("coin"):
            self.coin_pos = scene_info["coin"]

        return self.action_space[action]

    def reset(self):
        """
        Reset the status
        """
        print(self.RL.q_table)
        self.RL.q_table.to_pickle('games/RacingCar/log/qlearning.pickle')
        #    self.RL.plot_cost()
        print("reset ml script")

        pass