# class xxxx():
# any class you may create here

class MLPlay:
    def __init__(self):
        self.other_cars_position = []
        self.coins_pos = []
        print("Initial ml script")

        #####################################################
        #                                                   #
        # initializing anything in the begining of the game #
        #                                                   #
        #####################################################

        ###############################################
        #                                             #
        # If play the game by model, read model here. #
        #                                             #
        ###############################################

    # def xxxx():
    # any function you may create here

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if scene_info.__contains__("coin"):
            self.coin_pos = scene_info["coin"]

        ###############################################
        #                                             #
        # pure rule / rule + model to control the car #
        #                                             #
        ###############################################

        """
        There are seven commands you can use.
        """
        # return ["SPEED"]
        # return ["MOVE_LEFT"]
        # return ["MOVE_RIGHT"]
        # return ["BRAKE"]
        # return ["MOVE_RIGHT", "SPEED"]
        # return ["MOVE_LEFT", "SPEED"]
        # return []

        """scene_info: {
                        "frame": 25,
                        "id": 1,
                        "x":20,
                        "y": 260,
                        "all_cars_pos": [
                            (20,260),
                            (20,260)
                        ],
                        "distance": 27,
                        "velocity":0.9,
                        "coin_num":0,
                        "coin":[
                            (825,460),
                        ],
                        "status": "GAME_ALIVE"
                        }       
        """

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass

