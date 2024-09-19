import gamelib
import random
import math
import warnings
from sys import maxsize
import json


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.

  
Points each turn when spending 1 point every turn
8.0 3.0
10.2 2.2
11.9 1.7
13.2 1.3
14.1 0.9
14.8 0.7
15.4 0.6
15.8 0.4
16.1 0.3
16.3 0.2
17.5 1.2
18.4 0.9
19.0 0.6
19.5 0.5
19.9 0.4
20.2 0.3
20.4 0.2
20.5 0.1
20.6 0.1
20.7 0.1
21.8 1.1
22.6 0.8
23.2 0.6
23.6 0.4
24.0 0.4
24.2 0.2
24.4 0.2
24.5 0.1
24.6 0.1
24.7 0.1
25.8 1.1
26.6 0.8
27.2 0.6
27.6 0.4
28.0 0.4
28.2 0.2
28.4 0.2
28.5 0.1
28.6 0.1
28.7 0.1
29.8 1.1
30.6 0.8
31.2 0.6
31.6 0.4
32.0 0.4
32.2 0.2
32.4 0.2
32.5 0.1
32.6 0.1
32.7 0.1


"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        self.scored_on_locations = []
        
        self.VWALLS = [[0, 13], [1, 12], [2, 11], [3, 10], [4, 9], [5, 8], [7, 6], [6, 7], [8, 5], [9, 4], [10, 3], [11, 3], [12, 3], [13, 2], [14, 2], [15, 3], [16, 4], [20, 8], [19, 7], [18, 6], [17, 5], [20, 9], [20, 10], [20, 12], [21, 13], [22, 13], [23, 13], [25, 13],[27,13]]
        self.FUNNEL = [[11,3],[12,3],[13,2],[14, 2],[15, 3],[16, 4],[17, 5],[18, 6],[19, 7],[20, 8],[21, 9], [22, 10],[24,12],[25,13]]
        self.FUNNELTURRENTS = [[23, 12], [22, 12], [21, 12], [21, 10], [21, 9], [22, 10], [24, 12],[24, 13]] 
        self.BASTIONWALLS=[[4, 12], [5, 13],[6,12]]
        self.BASTIONTURRENTS = [[5, 12], [5, 11], [6, 11]]
        self.FIRSTUPGRADES = [[21, 10], [21, 12], [20, 12], [20, 10], [21, 13], [22, 12], [22, 10], [22, 13], [23, 12], [20, 9], [21, 9], [0, 13], [1, 12], [2, 11], [3, 10], [4, 9], [5, 8], [4, 12], [5, 12], [6, 11], [5, 13], [5, 11],[6,12]]
        self.SUPPORTS = [[13, 3], [14, 3], [14, 4], [15, 4], [13, 4], [14, 5], [15, 5], [14, 6], [15, 6], [16, 6], [16, 5], [17, 6], [18, 7], [17, 7], [16, 7], [12, 4], [13, 5], [11, 4], [12, 5], [13, 6], [14, 7], [15, 7], [13, 7], [12, 7], [12, 6], [11, 5], [10, 4], [10, 5], [11, 6]]
        self.gate = [26,12]
        self.sideGate = [21,11]
        self.PrevEnemyMP = 0
        self.side = 0 #0 is standard gameplay, 1 is Counter right side funnel, -1 is counter left side funnel
        self.pathGate = True#TRUE IS CLOSED, FALSE IS OPEN
        self.prevBreaches = []
        self.condition = 0 #Enemy MP, Location, Time
        self.biggestBreach = 0
        self.rightSide = False


    def on_turn(self, turn_state):
        self.game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(self.game_state.turn_number))
        self.game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.
        
        #ANALYZE FOR COUNTERING FUNNEL
        if self.game_state.turn_number == 0:
            self.game_state.attempt_spawn(WALL,self.gate)
            
            
            
#All locations: [[[23, 9], 105], [[23, 9], 105], [[22, 8], 147], [[22, 8], 147], [[21, 7], 105], [[21, 7], 105], [[19, 5], 147], [[19, 5], 147], [[19, 5], 147], [[21, 7], 105], 
# [[21, 7], 105], [[20, 6], 147], [[20, 6], 147], [[20, 6], 147], [[21, 7], 105], [[21, 7], 105], [[19, 5], 147], [[19, 5], 147], [[19, 5], 147], [[24, 10], 105], [[23, 9], 147], 
# [[23, 9], 147], [[23, 9], 147], [[21, 7], 105], [[21, 7], 105], [[19, 5], 147], [[19, 5], 147], [[19, 5], 147]]

        
        

        #INTERCEPTOR DEFENSE
        #self.game_state.attempt_spawn(INTERCEPTOR,[9,4],1+int(self.game_state.get_resource(1,1)/5))
        
        #ANALYZE ENEMY ATTACK PATTERNS
        
        # Breaches = self.scored_on_locations
        # if Breaches:
        #     if self.prevBreaches:
        #         diff = len(Breaches) - self.prevBreaches
        #     else:
        #         diff = len(Breaches)

        #     if diff >= 5:
        #         self.condition = self.PrevEnemyMP - 1
        #         if diff > self.biggestBreach:
        #             self.biggestBreach = diff
        #             self.rightSide = self.CheckRighttSide()



        # self.PrevEnemyMP = self.game_state.get_resource(1,1)

        # if self.game_state.get_resource(1,1) >= self.condition and self.rightSide:
        #     self.game_state.attempt_spawn(INTERCEPTOR, [24,10],self.game_state.get_resource(1,1)/3)
        
        #ATTACK PLAN
        linedUp = True
         


        for place in self.FUNNEL:
            if not self.game_state.game_map[place[0],place[1]]:
                if place in self.FUNNELTURRENTS:
                    if not self.game_state.attempt_spawn(TURRET,place):
                        linedUp = False
                elif not self.game_state.attempt_spawn(WALL,place):
                    linedUp = False


        
        if self.game_state.get_resource(1) >= 10:
            if linedUp:
                if self.pathGate:
                    self.game_state.attempt_remove(self.gate)
                    self.pathGate = False
                else:
                    if self.game_state.game_map[26,14]:
                        self.game_state.attempt_spawn(INTERCEPTOR,[24,10],4)
                        self.game_state.attempt_spawn(SCOUT,[11,2],self.game_state.number_affordable(SCOUT))
                    elif self.game_state.game_map[26,15] and self.game_state.game_map[25,14] and self.game_state.game_map[25,16]:
                        self.game_state.attempt_spawn(INTERCEPTOR,[24,10],4)
                        self.game_state.attempt_spawn(SCOUT,[11,2],self.game_state.number_affordable(SCOUT))
                    elif not self.game_state.game_map[26,14] and (not self.game_state.game_map[27,14] or not self.game_state.game_map[26,15]):
                        self.game_state.attempt_spawn(SCOUT,[11,2],self.game_state.number_affordable(SCOUT))  
                    else:
                        self.game_state.attempt_spawn(SCOUT,[11,2],3)
                        self.game_state.attempt_spawn(DEMOLISHER,[23,9],3)
                        self.game_state.attempt_spawn(SCOUT,[11,2],self.game_state.number_affordable(SCOUT))
                    self.game_state.attempt_spawn(WALL,self.sideGate)
                    self.game_state.attempt_remove(self.sideGate)
            else:
                self.game_state.attempt_spawn(WALL, self.gate)
                self.pathGate = True
        else:
            self.game_state.attempt_spawn(WALL, self.gate)
            self.pathGate = True
        

        

        #EVERY TURN
        #STRUCTTURES
        self.MainDef()

        self.replaceWalls()
        self.additionalSupports()
        self.game_state.attempt_upgrade([wall for wall in self.VWALLS if wall[1] >= 8])
        self.game_state.attempt_spawn(TURRET,[[x,12] for x in range(6,19)])
        self.game_state.attempt_spawn(WALL,[[x,13] for x in range(6,19)])
        self.game_state.attempt_upgrade([[x,13] for x in range(6,19)] + [[x,12] for x in range(6,19)])


        self.game_state.submit_turn()

    # def CheckRighttSide(self):
    #     counter = 0
    #     tempList = [x[0] for x in self.scored_on_locations]
    #     for i in tempList:
    #         curr_frequency = tempList.count(i)
    #         if(curr_frequency> counter):
    #             counter = curr_frequency
    #             cord = i
    #     # frames = 0
    #     # for breach in self.scored_on_locations:
    #     #     if breach[0] == cord:
    #     #         frames += breach[1]
    #     return cord in self.game_state.game_map.BOTTOM_RIGHT + [[13, 0], [12, 1], [11, 2]]
    #     #, frames/counter

    def FlipCord(Cords):
        if type(Cords) == list:
            returnList = []
            for cord in Cords:
                returnList.append([abs(27-cord[0]),cord[1]])
        else:
            return [abs(27-cord[0]),cord[1]]
        


    def MainDef(self):
        self.game_state.attempt_spawn(WALL,self.VWALLS)
        self.game_state.attempt_spawn(TURRET,self.FUNNELTURRENTS)
        self.game_state.attempt_spawn(WALL,self.BASTIONWALLS)
        self.game_state.attempt_spawn(TURRET,self.BASTIONTURRENTS)
        self.game_state.attempt_upgrade(self.FIRSTUPGRADES)
        


        
    
    def replaceWalls(self):
        for location in self.VWALLS + self.BASTIONWALLS:
            if self.game_state.game_map[location]:
                unit = self.game_state.game_map[location][0]
                if unit.health < unit.max_health*.25:
                    self.game_state.attempt_remove(location)
        
    


    def additionalSupports(self):
        self.game_state.attempt_spawn(SUPPORT,self.SUPPORTS)
        self.game_state.attempt_upgrade(self.SUPPORTS)

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at in json-docs.html in the root of the Starterkit.
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly, 
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append([location,state["turnInfo"][2]])
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
