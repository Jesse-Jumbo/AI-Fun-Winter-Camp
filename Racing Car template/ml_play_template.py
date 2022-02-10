import numpy as np
import pandas as pd

class MLPlay:
    def __init__(self):
        self.car_pos_x =20
        self.p_car_pos_x =20

        self.car_pos_y = 160
        self.reward = 0
        # self.action = "a"
        self.action = 0
        # 可自行定義有種action
        self.action_space = ["SPEED", "BRAKE", "MOVE_LEFT","MOVE_RIGHT", "NONE"]
        # self.action_space = {"SPEED": "SPEED","b": "MOVE_LEFT","c": "MOVE_RIGHT","d": "NONE"}
        # self.action_space = ["SPEED", "BRAKE", "NONE"]
        # self.action_space = ["MOVE_LEFT", "MOVE_RIGHT", "NONE"]
        self.n_actions = len(self.action_space)
        # self.RL = QLearningTable(actions=["SPEED","","c"])
        self.RL = QLearningTable(actions=list(range(self.n_actions)))
        self.observation = 0
        self.status = "ALIVE"
        # 可自行定義state
        self.state = ""
        self.state_ = ""
        self.distance = 0
        self.prev_distance = 0
        self.over_times = 0
        self.pass_times = 0
        print("Initial ml script")


    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        '''
        if scene_info["status"] == "GAME_OVER":
            return "RESET"
        '''

        self.car_pos_x = scene_info["x"]
        self.car_pos_y = scene_info["y"]
        self.distance = scene_info["distance"]
        def check_grid():
            #狀態為蘇老師說的，直線速度與左右車道的結合
            self.observation = 0
            
            # 走到最上貨是最下車到是要避免的，因此給不同的狀態
            if self.car_pos_y <= 140: # lane 1
                self.observation = 1
                self.state_ = '撞到上面'
                return

            if self.car_pos_y >= 490: # lane 9
                self.observation = 1
                self.state_ = '撞到下面'
                return 

            #檢查前後是否有車以及距離
            
            for car in scene_info["all_cars_pos"]:
                #與我在近乎同一個車道 abs(car[1]-self.car_pos_y) < 30
                #在我前方 car[0] > self.car_pos_x
                #與我的距離小於180  car[0] - self.car_pos_x < 180 
                if abs(car[1]-self.car_pos_y) < 40 and  car[0] > self.car_pos_x and car[0] - self.car_pos_x < 180:
                    self.observation = 1
                    self.state_ = "該減速"
                    return
                #與我在近乎同一個車道 abs(car[1]-self.car_pos_y) < 30
                #在我後方 car[0] < self.car_pos_x
                #與我的距離小於120  car[0] - self.car_pos_x > -120   
                elif abs(car[1]-self.car_pos_y) < 40 and car[0] < self.car_pos_x and car[0] - self.car_pos_x > -120:
                    self.observation = 1
                    self.state_ = "該加速"
                    return
                else:
                    pass
            

            #不是上述條件則狀態維持在不動
            self.observation = 1
            self.state_ = "不動"
            return 
        
        def check_nearby(state):
            result_state = state

            isLeft = False
            isRight = False

            cars = scene_info["all_cars_pos"]
            cars = list(filter(lambda pos: pos[0] > -100,  cars))

            if(len(cars) == 1): return result_state

            for car in cars:
                bias = 30

                if car == (self.car_pos_x, self.car_pos_y):
                    continue
                if ( (car[0] > self.car_pos_x - 60) and (car[0] < self.car_pos_x + bias + 60 * 2) ):
                    # print("a")
                    if(car[1] > ( self.car_pos_y - 30 - bias ) ):
                        # print("a")
                        isLeft = True
                    if(car[1] < self.car_pos_y + 30 + bias):
                        # print("b")
                        isRight = True
            
            if isLeft:
                result_state += ";左邊有車"
            if isRight:
                result_state += ";右邊有車"

            return result_state + ";"

        def step(self, state):
            # reward function
            self.reward = 0
            if self.observation != 0:
                #以下各個狀態的reward就是需要各為自己調整了!
                if state == '撞到上面' or state == '撞到下面':
                    self.reward = -1000

                if state.find("該減速") > -1:
                    self.reward = -100
                
                if state.find("該加速") > -1:
                    self.reward = -100
                
                if state.find("不動") > -1:
                    self.reward = 5000
                    #鼓勵往前走
                    if self.distance > self.prev_distance:
                        self.reward += 4000
                    else:
                        self.reward -= 200
                    # elif self.prev_distance > self.distance:
                    #     self.reward -= 100 + (self.prev_distance - self.distance) * 100
                    
                if state.find("左")>-1:
                    self.reward -= 200

                if state.find("右")>-1:
                    self.reward -= 200

                # if 
                
            if scene_info["status"] == "GAME_OVER":
                self.reward = -5000
                self.over_times += 1
            if scene_info["status"] == "GAME_PASS":
                self.reward = 5000
                self.pass_times += 1

            # print(state + " reward:" + str(self.reward), end=' ' )
            return self.reward



        check_grid()
        self.state_ = check_nearby(self.state_)

        self.reward = step(self, self.state_)
        action = self.RL.choose_action(str(self.state_))
        #Disable following line if dont want to update model, just use it
        self.RL.learn(str(self.state), self.action, self.reward, str(self.state_))
        self.action = action
        self.state = self.state_
        
        self.prev_distance = self.distance
        self.p_car_pos_x = self.p_car_pos_x

        if scene_info["status"] != "GAME_ALIVE" and scene_info["status"] != "ALIVE":
            return "RESET"
        return self.action_space[action]


    def reset(self):
        """
        Reset the status
        """
        disp = self.RL.q_table.set_axis(self.action_space, axis=1, inplace=False)
        print(disp)
        print(f"Game_over_times: {self.over_times}")
        print(f"Game_pass_times: {self.pass_times}")
        #Disable following line if don't save model
        self.RL.q_table.to_pickle('games/RacingCar/log/qlearning.pickle')
        #self.RL.plot_cost()
        print("reset ml script")
        
        pass


class QLearningTable:
    def __init__(self, actions, learning_rate=0.1, reward_decay=0.9, e_greedy=0.1):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        try:
            self.q_table = pd.read_pickle('games/RacingCar/log/qtable.pickle')
        except Exception as e:
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
            

    def choose_action(self, observation):
        self.check_state_exist(observation)

        # action selection
        if np.random.uniform() > self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]

            # some actions may have the same value, randomly choose on in these actions
            max_item_in_line = state_action[state_action == np.max(state_action)]
            action = np.random.choice(max_item_in_line.index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s)
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'GAME_OVER' or s_ != 'GAME_PASS':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        if state not in list(self.q_table.index):
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    # [""] + ["SPEED", "MOVE_LEFT", "MOVE_RIGHT", "NONE"],
                    index=self.q_table.columns,
                    name=state,
                )
            )