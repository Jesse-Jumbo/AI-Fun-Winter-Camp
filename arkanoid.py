"""
The template of the main script of the machine learning process
"""


class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False  # 判斷發球初始為False
        self.previous_ball = (0, 0)  # 球位置初始化在左上角
        self.pred = 100  # 球的x落點初始化在正中間
        self.platform_y = 400  # 板子的y座標
        self.ball_speed_y = 7  # 球的初始速度 (移動的pix)
        self.platform_width = 200  # 螢幕的寬度

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or  # 當遊戲結束或
                scene_info["status"] == "GAME_PASS"):  # 遊戲過關
            return "RESET"  # 自動重新開始遊戲
        if not self.ball_served:  # 如果球還沒發球
            self.ball_served = True  # 自動發球
            command = "SERVE_TO_LEFT"  # 並且是往左發球
        else:
            self.pred = 100  # 預測球的x落點在正中間
            if self.previous_ball[1] - scene_info['ball'][1] > 0:  # 如果球往上走
                pass  # 不動作
            else:  # 否則球是往下走，則執行以下
                distance_paltform_ball_y = self.platform_y - scene_info['ball'][1]  # 計算球拍與球的y座標距離
                ball_speed_x = scene_info['ball'][0] - self.previous_ball[0]  # 從球的前後位置，計算球的速度
                self.pred = scene_info['ball'][0] + (
                            distance_paltform_ball_y // self.ball_speed_y) * ball_speed_x  # 令假設的球的x落點=現在球的x座標+球下個frame的座標(時間(距離/速度)*球的x速度)

            section = (self.pred // self.platform_width)  # 計算球的x落點在幾個螢幕外
            if (section % 2 == 0):  # 若是可整除(代表在螢幕右側)
                self.pred = abs(self.pred - self.platform_width * section)  # 令預測的x落點=原先超出螢幕右側的x落點反射回螢幕內
            else:  # 否則(代表球在螢幕的左側)
                self.pred = self.platform_width - abs(
                    self.pred - self.platform_width * section)  # 令預測的x落點=原先超出螢幕左側的x落點反射回螢幕內

            if scene_info['platform'][0] + 20 + 5 < self.pred:  # 如果板子的x中心座標<球的x落點
                command = "MOVE_RIGHT"  # 板子往右移動
            elif scene_info['platform'][0] + 20 - 5 > self.pred:  # 如果板子的x中心座標>球的x落點
                command = 'MOVE_LEFT'  # 板子往左移動
            else:
                command = 'NONE'  # 否則，不動
        self.previous_ball = scene_info['ball']  # 更新球之前的座標位置=現在的座標位置
        return command  # 返回板子移動的命令

    def reset(self):  # 遊戲結束或通關時，會呼叫的method
        """
        Reset the status
        """
        self.ball_served = False  # 令發球為False


'''
"""
The template of the main script of the machine learning process
"""


class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.previous_ball = (0,0)
        self.pred = 100
        self.platform_y = 400
        self.ball_speed_y = 7
        self.platform_width = 200
        

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
            command = "SERVE_TO_LEFT"
        else:
            self.pred = 100
            if self.previous_ball[1] - scene_info['ball'][1]>0:
                pass
            else:
                distance_paltform_ball_y = self.platform_y - scene_info['ball'][1]
                ball_speed_x = scene_info['ball'][0] - self.previous_ball[0]
                if ball_speed_x >=0 :
                    self.pred = scene_info['ball'][0] + (distance_paltform_ball_y // self.ball_speed_y) * ball_speed_x
                else:
                    #treat all distance as positive
                    self.pred = self.platform_width - scene_info['ball'][0] + abs((distance_paltform_ball_y // self.ball_speed_y) * ball_speed_x)

                section = (self.pred // self.platform_width)
                remain = self.pred % self.platform_width

                if (section % 2 == 0 ):
                    if ball_speed_x >= 0 :
                        # from left top to right bottom
                        self.pred = remain
                    else:
                        # from right top to left bottom
                        self.pred = self.platform_width - remain
                else:
                    if ball_speed_x >= 0 :
                        # from right top to left bottom
                        self.pred = self.platform_width - remain
                    else:
                        # from left top to right bottom
                        self.pred = remain

            if scene_info['platform'][0]+20 + 5<self.pred:
                command = "MOVE_RIGHT"
            elif scene_info['platform'][0]+20-5 > self.pred:
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
'''
