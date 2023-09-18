import random
import time
from copy import copy
import pickle

from utilities import experiment
from FaultyAgent8 import FaultyAgent8
from simulators import smart_simulator_for_faulty_drone


class SmartAgent8(FaultyAgent8):
    '''
        Overrides update_predator_beliefs() accounting to faulty drone
        Overrides update_prey_beliefs() accounting to faulty drone
    '''
    def __init__(self, game):
        super().__init__(game)

    # Overriding
    def update_predator_beliefs(self, knowledge_node, is_predator_present, is_survey_knowledge):
        if is_predator_present:
            # print('yes')
            self.predator_beliefs = [0.] * self.game.get_num_nodes()
            self.predator_beliefs[knowledge_node] = 1.
            return copy(self.predator_beliefs)

        pr_knowledge_node = self.predator_beliefs[knowledge_node]
        probs = copy(self.predator_beliefs)

        if is_survey_knowledge:
            for node in self.game.get_nodes_list():
                if node == knowledge_node:
                    probs[node] = 0.1*pr_knowledge_node
                else:
                    probs[node] = (probs[node] / (1 - 0.9*pr_knowledge_node))
        else:
            for node in self.game.get_nodes_list():
                if node == knowledge_node:
                    probs[node] = 0.
                else:
                    probs[node] = probs[node] / (1 - pr_knowledge_node)

        self.predator_beliefs = copy(probs)

        return copy(self.predator_beliefs)

    # Overriding
    def update_prey_beliefs(self, knowledge_node, is_prey_present, is_survey_knowledge):
        if is_prey_present:
            self.prey_beliefs = [0.] * self.game.get_num_nodes()
            self.prey_beliefs[knowledge_node] = 1.
            return copy(self.prey_beliefs)

        pr_knowledge_node = self.prey_beliefs[knowledge_node]

        if is_survey_knowledge:
            for node in self.game.get_nodes_list():
                if node == knowledge_node:
                    self.prey_beliefs[node] = 0.1*pr_knowledge_node
                else:
                    self.prey_beliefs[node] = (self.prey_beliefs[node] / (1 - 0.9*pr_knowledge_node))
        else:
            for node in self.game.get_nodes_list():
                if node == knowledge_node:
                    self.prey_beliefs[node] = 0.
                else:
                    self.prey_beliefs[node] = self.prey_beliefs[node] / (1 - pr_knowledge_node)

        return copy(self.prey_beliefs)


if __name__ == "__main__":
    agent8_results = {}
    keys = ['Agent', 'no_of_simulations', 'max_steps_allowed', 'Success rate', 'Failure rate',
            'Hangs', '% knowing prey location', '% knowing predator location']

    for key in keys:
        agent8_results[key] = []

    idx = 0
    start = time.time()
    for steps_allowed in range(50, 301, 50):
        result = experiment(SmartAgent8, num_graphs=30, simulation_per_graph=100,
                            max_steps_allowed=steps_allowed, simulator=smart_simulator_for_faulty_drone)

        for key, val in result.items():
            agent8_results[key].append(val)

        print(f'% of knowing exact prey location: {agent8_results["% knowing prey location"][idx]}')
        print(f'% of knowing exact predator location: {agent8_results["% knowing predator location"][idx]}')
        idx += 1

    print(agent8_results)
    end = time.time()

    print(f'time taken: {end-start} secs')

    with open('smartagent8_results.pkl', 'wb') as f:
        pickle.dump(agent8_results, f)