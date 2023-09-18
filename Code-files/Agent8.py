import time
import numpy as np
import random
import pickle
from Agent2 import Agent2
from Agent7 import Agent7
from utilities import experiment
from simulators import combined_partial_info_simulator


class Agent8(Agent2, Agent7):
    '''
    Agent8 will inherit Agent2 and Agent7

    Agent8 will have methods used in Combined Partial Information setting by inheriting Agent7

    to have methods to perform better than Agent7 using methods inherited from Agent2
        to have self.estimate_future_prey_loc() from Agent2
        to have self.select_next_location_even_agents() from Agent2
        will override self.agent_movement()
    '''
    def __init__(self, game):
        Agent7.__init__(self, game)

    def agent_movement(self):
        prey_probs = np.array(self.prey_beliefs)
        prey_possible_locs = list(np.where(prey_probs == prey_probs.max())[0])
        prey_loc = random.choice(prey_possible_locs)

        predator_probs = np.array(self.predator_beliefs)
        predator_possible_locs = list(np.where(predator_probs == predator_probs.max())[0])
        predator_loc = random.choice(predator_possible_locs)

        future_prey_loc = self.estimate_future_prey_loc(prey_loc)

        self.agent_loc = self.select_next_location_even_agents(future_prey_loc, predator_loc)
        return self.agent_loc


if __name__ == "__main__":
    agent8_results = {}
    keys = ['Agent', 'no_of_simulations', 'max_steps_allowed', 'Success rate', 'Failure rate',
            'Hangs', '% knowing prey location', '% knowing predator location']

    for key in keys:
        agent8_results[key] = []

    idx = 0
    start = time.time()
    for steps_allowed in range(50, 301, 50):
        result = experiment(Agent8, num_graphs=30, simulation_per_graph=100,
                            max_steps_allowed=steps_allowed, simulator=combined_partial_info_simulator)

        for key, val in result.items():
            agent8_results[key].append(val)

        print(f'% of knowing exact prey location: {agent8_results["% knowing prey location"][idx]}')
        print(f'% of knowing exact predator location: {agent8_results["% knowing predator location"][idx]}')
        idx += 1

    print(agent8_results)
    end = time.time()

    print(f'time taken: {end-start} secs')

    with open('agent8_results.pkl', 'wb') as f:
        pickle.dump(agent8_results, f)