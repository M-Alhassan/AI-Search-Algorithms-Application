# ================================= Base Class =================================
class Problem(object):
    def __init__(self, initial_state, goal_state=None):
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    def actions(self, state):
        raise NotImplementedError
    
    def result(self, state, action):
        raise NotImplementedError
    
    def is_goal(self, state):
        if state == self.goal_state:
            return True
        else:
            return False
    
    def action_cost(self, state1, action, state2):
        return 1
    
    def h(self, node):
        return 0
# ================================= Route Problem =================================
class RouteProblem(Problem):
    def __init__(self, initial_state, goal_state=None, map_graph=None, map_coords=None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.map_graph = map_graph
        self.map_coords = map_coords
    
    def actions(self, state):
        reachable_states = []
        for key in self.map_graph:
            if key[0] == state:
                reachable_states.append(key[1])
        return reachable_states

    def result(self, state, action):
        reachable_states = self.actions(state)
        if action in reachable_states:
            return action
        else:
            return state
        
    def action_cost(self, state1, action, state2):
        return self.map_graph[state1, state2]

    # heuristic = Euclidean distance
    def h(self, node):
        if self.is_goal(node.state):
            return 0
        else:
            goal_x = self.map_coords[self.goal_state][0]
            goal_y = self.map_coords[self.goal_state][0]
            current_x = self.map_coords[node.state][0]
            current_y = self.map_coords[node.state][1]
            euclidean_dist = ((goal_x - current_x)**2 + (goal_y - current_y)**2)**0.5
            return euclidean_dist

#================================= Grid Problem =================================
class GridProblem(Problem):
    def __init__(self, initial_state, N, M, wall_coords, food_coords):
        self.N = N
        self.M = M
        self.wall_coords = wall_coords
        self.food_coords = food_coords
        food_eaten = ()
        for food in food_coords:
            food_eaten += (False,)
        self.initial_state = (initial_state, food_eaten)
    
    # returns legal moves list
    def actions(self, state):
        x_coord = state[0][0]
        y_coord = state[0][1]
        moves = ['up', 'down', 'right', 'left'] # all available moves
        wall_coords = self.wall_coords
        # Remove illegal moves from list
        for wall in wall_coords:
            if ((x_coord+1 == wall[0] and y_coord == wall[1]) or x_coord == self.M) and 'right' in moves:
                moves.remove('right')
            if ((x_coord-1 == wall[0] and y_coord == wall[1]) or x_coord == 1) and 'left' in moves:
                moves.remove('left')
            if ((y_coord+1 == wall[1] and x_coord == wall[0]) or y_coord == self.N)  and 'up' in moves:
                moves.remove('up')
            if ((y_coord-1 == wall[1] and x_coord == wall[0]) or y_coord == 1)   and 'down' in moves:
                moves.remove('down')
        if len(moves) == 0:
            return []
        else:    
            return moves

    def result(self, state, action):
        x_coord = state[0][0]
        y_coord = state[0][1]
        stat = list(state[1]) # food status
        # change position
        if action == 'right':
            x_coord +=1
        if action == 'left':
            x_coord -=1
        if action == 'up':
            y_coord +=1
        if action == 'down':
            y_coord -=1
        pos = (x_coord, y_coord)    # new position (x, y)
        # check if food was eaten
        for food_pos in self.food_coords:
            if pos == food_pos:
                stat[self.food_coords.index(food_pos)] = True
        new_state = (pos, tuple(stat))
        return new_state
    
    def is_goal(self, state):
        stat = state[1]
        for food in stat:
            if food == False:
                return False
        return True

    # helper function to calculate the manhattan distance
    def get_manhattan_distance(self, p, q):
        distance = 0
        for p_i,q_i in zip(p,q):
            distance += abs(p_i - q_i)
        return distance

    # heuristic = Manhattan distance
    def h(self, node):
        if self.is_goal(node.state):
            return 0
        pos = node.state[0] #current position (x, y)
        x_coord = node.state[0][0]
        y_coord = node.state[0][1]
        stat = list(node.state[1])
        distances = []
        for food_pos in self.food_coords:
            if not stat[self.food_coords.index(food_pos)]:
                dist = self.get_manhattan_distance(pos, food_pos)
                distances.append(dist)
                #----------- debugging start -----------
                # print('sprite position =',pos)
                # print('target food position =',food_pos)
                # print('distance from sprite:', dist)
                # print('all food coord', self.food_coords)
                # print('food status:', stat)
                #----------- debugging end -----------
        distances.sort()
        #----------- debugging start -----------
        # print('distances = ', distances)
        # print("========== All distances have been calculated =========")
        # print('finding path ... \n\n')
        #----------- debugging end -----------
        return distances[0]


        
    
        
            


################## Test ##################
