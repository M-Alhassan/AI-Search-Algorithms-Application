import heapq
from node import *

class PriorityQueue:
    def __init__(self, items=(), priority_function=(lambda x: x)):
        self.priority_function = priority_function
        self.pqueue = []
        # add the items to the PQ
        for item in items:
            self.add(item)

    # Add item to PQ with priority-value given by call to priority_function
    def add(self, item):
            pair = (self.priority_function(item), item)
            heapq.heappush(self.pqueue, pair)

    # pop and return item from PQ with min priority-value
    def pop(self):
        return heapq.heappop(self.pqueue)[1]

    # gets number of items in PQ
    def __len__(self):
        return len(self. pqueue)

###################################### Algorithms ######################################

# ================================== Helper functions ==================================

# returns the children nodes of the current node
def expand(problem, node):
    nodes_list = []
    current_state = node.state
    for action in problem.actions(current_state):
        new_state = problem.result(current_state, action)
        cost = node.path_cost + problem.action_cost(current_state, action, new_state)
        child_node = Node(new_state, node, action, cost)
        nodes_list.append(child_node)
    return nodes_list

# returns a list of actions to the given node
def get_path_actions(node):
    if node == None:
        return []
    elif node.parent_node == None:
        return []
    else:
        actions = []
        while node.parent_node != None:
            actions.append(node.action_from_parent)
            node = node.parent_node
        actions.reverse()
        return actions

# returns a list of states to reach the given node from the start
def get_path_states(node):
    if node == None:
        return []
    else:
        states = []
        while node != None:
            states.append(node.state)
            node = node.parent_node
    states.reverse()
    return states

# returns f value for the breadth-first function
def bfs_f(node):
    return node.depth

# returns f vlaue for the depth-first function
def dfs_f(node):
    return (0 - node.depth)

# returns the f value for the uniform-cost funtion
def ucs_f(node):
    # successors = []
    # for child in expand(problem, node):
    #     successors.append(child.path_cost)
    # successors.sort()
    # successors[0]
    return node.path_cost 

# ================================== Search Algorithms ==================================
# note: Best-First search is the base case of the other search algorithms
# all other search algorithms are Best-First with different f values 

#--------------------------- start Best First ------------------------
# implementation of the Best-First search (graph-like)
def best_first_search(problem, f):
    my_node = Node(problem.initial_state)
    frontier = PriorityQueue([my_node], f)
    reached = {problem.initial_state: my_node}  #{state1: node1, state2: node2 ... }
    while len(frontier) > 0:
        current_node = frontier.pop()
        if problem.is_goal(current_node.state):
            return current_node
        for child in expand(problem, current_node):
            s = child.state
            if s not in reached.keys() or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return None

# implementation of Best-First search (tree-like)
def best_first_search_treelike(problem, f):
    my_node = Node(problem.initial_state)
    frontier = PriorityQueue([my_node], f)
    # reached = {problem.initial_state: my_node}  #{state1: node1, state2: node2 ... }
    while len(frontier) > 0:
        current_node = frontier.pop()
        if problem.is_goal(current_node.state):
            return current_node
        for child in expand(problem, current_node):
            s = child.state
            # if s not in reached.keys() or child.path_cost < reached[s].path_cost:
            #     reached[s] = child
            frontier.add(child)
    return None
#--------------------------- end Best First ------------------------

# implementation of Breadth-First search
def breadth_first_search(problem, treelike=False):
    if treelike:
        return best_first_search_treelike(problem, bfs_f)
    else:
        return best_first_search(problem, bfs_f)

# implementation of depth-first search
def depth_first_search(problem, treelike=False):
    if treelike:
        return best_first_search_treelike(problem, dfs_f)
    else:
        return best_first_search(problem, dfs_f)

# implemenation of Uniform-Cost search
def uniform_cost_search(problem, treelike=False):
    if treelike:
        return best_first_search_treelike(problem, ucs_f)
    else:
        return best_first_search(problem, ucs_f)

# implemenation of greedy search
def greedy_search(problem, h, treelike=False):
    if treelike:
        return best_first_search_treelike(problem, f=(lambda n: problem.h(n)))
    else:
        return best_first_search(problem, f=(lambda n: problem.h(n)))

# implementation of A* (A-star) search
def astar_search(problem, h, treelike=False):
    if treelike:
        return best_first_search_treelike(problem, f=(lambda n: n.path_cost + problem.h(n)))
    else:
        return best_first_search(problem, f=(lambda n: n.path_cost + problem.h(n)))
 