import pickle
import random
import time
from collections import defaultdict
from copy import copy
from Agent1 import Agent1
import numpy as np
from Game import Game
from utilities import experiment
from simulators import partial_predator_info_simulator


class Agent5(Agent1):
    '''
        Inherits Agent1, that will make Agent5
        to have self.agent_loc from Agent1
        to have self.game from Agent1
        to have self.initialise_agent_location() from Agent1
        to have self.select_next_location_odd_agents() from Agent1
        will override self.agent_movement() from Agent1

        and define new methods required for partial predator information setting
    '''

    def __init__(self, game: Game):
        super().__init__(game)
        self.predator_beliefs = None
        self.initialise_predator_beliefs()

    def initialise_predator_beliefs(self):
        self.predator_beliefs = [0.] * self.game.get_num_nodes()
        self.predator_beliefs[self.game.get_predator_loc()] = 1.

    def update_predator_beliefs(self, knowledge_node, is_predator_present):

        # If agent knows, predator is present at knowledge_node, make it's beliefs as 1 and
        # make remaining all nodes to have 0
        if is_predator_present:
            # print('yes')
            self.predator_beliefs = [0.] * self.game.get_num_nodes()
            self.predator_beliefs[knowledge_node] = 1.
            return copy(self.predator_beliefs)

        pr_knowledge_node = self.predator_beliefs[knowledge_node]

        # predator not found at knowledge_node
        # P(predator at node | survey failed to find predator at knowledge_node)
        #                           = P(predator at node) * 1/(1 - p(predator at knowledge_node))

        for node in self.game.get_nodes_list():
            if node == knowledge_node:
                self.predator_beliefs[node] = 0.
            else:
                self.predator_beliefs[node] = self.predator_beliefs[node] / (1-pr_knowledge_node)

        return copy(self.predator_beliefs)

    def update_predator_beliefs_after_move(self):
        num_nodes = self.game.get_num_nodes()
        probs = [0.] * num_nodes
        agent_loc = self.agent_loc

        for cur_node in self.game.get_nodes_list():
            neighbors = self.game.get_neighbors(cur_node)
            neighbor_dist = defaultdict(list)

            for neighbor in neighbors:
                distance = self.game.shortest_dist(neighbor, agent_loc)
                neighbor_dist[distance].append(neighbor)

            min_dist_list = neighbor_dist[min(neighbor_dist)]

            for shortest_choice_node in min_dist_list:
                alpha = 1/(len(min_dist_list))
                probs[shortest_choice_node] += (0.6 * alpha * self.predator_beliefs[cur_node])

            for neighbor in neighbors:
                alpha = 1/(self.game.get_degree(neighbor))
                probs[cur_node] += (0.4 * alpha * self.predator_beliefs[neighbor])

        self.predator_beliefs = copy(probs)
        return copy(probs)

    def agent_movement(self):
        predator_probs = np.array(self.predator_beliefs)

        # select the predator location using beliefs agent has
        predator_possible_locs = list(np.where(predator_probs == predator_probs.max())[0])

        predator_loc = random.choice(predator_possible_locs)
        prey_loc = self.game.get_prey_loc()

        self.agent_loc = self.select_next_location_odd_agents(prey_loc, predator_loc)

        return self.agent_loc

    def survey_for_predator(self):
        probs = np.array(self.predator_beliefs)

        # survey the node which has the maximum probability
        survey_options = np.where(probs == probs.max())[0]

        survey_options = list(survey_options)
        survey_node = None
        if len(survey_options) > 1:
            distances = [self.game.shortest_dist(self.agent_loc, node)
                         for node in survey_options]
            min_distance = min(distances)

            proximity_options = []
            for survey_node, distance in zip(survey_options, distances):
                if distance == min_distance:
                    proximity_options.append(survey_node)

            survey_node = random.choice(proximity_options)
        else:
            survey_node = survey_options[0]

        is_predator_present = self.game.get_predator_loc() == survey_node

        return survey_node, is_predator_present

    def surely_knows_predator(self):
        beliefs = self.predator_beliefs

        if max(beliefs) == 1.:
            return True

        return False


if __name__ == "__main__":
    agent5_results = {}
    keys = ['Agent', 'no_of_simulations', 'max_steps_allowed', 'Success rate', 'Failure rate',
            'Hangs', '% knowing prey location', '% knowing predator location']
    for key in keys:
        agent5_results[key] = []

    idx = 0
    start = time.time()
    for steps_allowed in range(50, 301, 50):

        result = experiment(Agent5, num_graphs=30, simulation_per_graph=100,
                            max_steps_allowed=steps_allowed, simulator=partial_predator_info_simulator)

        for key, val in result.items():
            agent5_results[key].append(val)

        print(f'% of knowing exact predator location: {agent5_results["% knowing predator location"][idx]}')
        idx += 1

    print(agent5_results)
    end = time.time()

    print(f'time taken: {end - start} secs')

    with open('agent5_results.pkl', 'wb') as f:
        pickle.dump(agent5_results, f)