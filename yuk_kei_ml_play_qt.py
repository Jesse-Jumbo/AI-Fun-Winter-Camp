import numpy as np
import random
from .QT import QLearningTable


class MLPlay:
    def __init__(self):             # 初始化所有變數
        self.ball_served = False    # 是否發球
        self.ball_vel = (0, 0)      # 球的速度
        self.ball_pos = (95, 400)   # 球的位置
        self.platform_pos = (75, 400)   # 板子的x, y 座標
        self.previous_ball = (0, 0)     # 球的先前位置
        self.step = 0       #
        self.reward = 0     # 獎勵分數
        self.action = 0     # 索引行動列表
        self.action_space = ["SERVE_TO_LEFT", "SERVE_TO_RIGHT", "MOVE_LEFT", "MOVE_RIGHT", "NONE"]  # 板子的所有行動
        self.n_actions = len(self.action_space)     # 有幾種行動可選
        self.n_features = 2     # 板子往右行動
        self.RL = QLearningTable(actions=list(range(self.n_actions)))       # 每次走不同行動
        self.observation = 0        # 這個位置的狀態
        self.status = "GAME_ALIVE"  # 遊戲狀態
        self.state = [self.observation]     # 位置狀態for
        self.state_ = [self.observation]    # 位置狀態for
        self.resetTime = 0          # 計算重置次數
        self.accum = 0              # 為對的路徑加權分數

        print("Initial ml script")

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        # 判斷何時重置遊戲
        if scene_info["status"] == "GAME_OVER" or scene_info["status"] == "GAME_PASS":
            return "RESET"

        def check():        # 收集狀態
            self.observation = "0"      # 狀態改為字串
            if self.ball_vel_y > 0:     # 如果球往下移動
                st_x = self.ball_pos_x  # 紀錄球的x座標
                st_y = self.ball_pos_y  # 紀錄球的y座標
                st_p = self.platform_1P     # 紀錄球拍x座標
                '''
                if self.ball_vel_x > 0 :
                    if self.ball_vel_y > 0:
                        st_dir = 0
                    else:
                        st_dir = 1
                else: 
                    if self.ball_vel_y > 0:
                        st_dir = 2
                    else:
                        st_dir = 3
                '''

                # self.observation = str(st_x) + '_' +  str(st_y)+ '_' + str(st_p) +'_' + str(st_dir)
                # 紀錄球x座標、球y座標、玩家x座標、球的x速度、球的y速度
                self.observation = str(st_x) + '_' + str(st_y) + '_' + str(st_p) + '_' + str(
                    self.ball_vel_x) + '_' + str(self.ball_vel_y)

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

        def step(self, state):      # 計算獎勵
            # reward function
            # 如果球往下掉 且球距離板子y座標在10pix內 且球x距離板子x中心在20pix以內時:
            if self.ball_vel_y > 0 and self.ball_pos_y > 390 and abs(self.platform_1P + 20 - self.ball_pos_x) < 20:
                self.accum += 1     # 每一個frame的加權分數
                self.reward = 500 * self.accum  # 獎勵*加權分數
            else:   # 否則
                self.reward = 0     # 獎勵為零
            # print(self.reward, end=' ')
            '''
            you can design your reward function here !

            '''

            return self.reward  # 返回獎勵
        # 更新變數
        self.ball_vel_x = scene_info["ball"][0] - self.previous_ball[0]
        self.ball_vel_y = scene_info["ball"][1] - self.previous_ball[1]
        self.ball_pos_x = scene_info["ball"][0]
        self.ball_pos_y = scene_info["ball"][1]
        self.platform_1P = scene_info["platform"][0]
        self.platform_1P_y = scene_info["platform"][1]

        self.previous_ball = scene_info["ball"]
        # 檢查位置狀態
        check()

        self.state_ = [self.observation]    # 獲得位置狀態資訊
        self.reward = step(self, self.state_)       # 獲得此狀態的獎勵
        action = self.RL.choose_action(str(self.state))     # 選擇此狀態板子要執行的行動
        self.RL.learn(str(self.state), self.action, self.reward, str(self.state_))  # 學習此位置狀態
        self.action = action    # 獲取板子要執行的行動
        self.state = self.state_    # 更新位置的狀態資訊
        # 判斷何時自動重置遊戲
        if scene_info["status"] == "GAME_OVER" or scene_info["status"] == "GAME_PASS":
            return "RESET"

        return self.action_space[action]    # 返回板子要執行的行動

    def reset(self):        # 重置遊戲
        """
        Reset the status
        """
        self.accum = 0      # 加權重置
        self.ball_served = False    # 發球為否
        self.resetTime += 1     # 重置次數+1
        if self.resetTime > 10:     # 每重置10次時
            print(self.RL.q_table)  # 印出記錄到的所有狀態資料
            self.RL.q_table.to_pickle('games/arkanoid/log/qtable.pickle')   # 將狀態資料儲存進pickle檔
            # self.RL.plot_cost()
            print("Save Qtable")    # 印出儲存完畢字串提醒
            self.resetTime = 0      # 重置遊戲次數重新紀錄
        pass
