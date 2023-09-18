import pickle
import random
import numpy as np
import time
from utilities import experiment
from simulators import combined_partial_info_simulator
from Agent3 import Agent3
from Agent5 import Agent5


class Agent7(Agent3, Agent5):
    '''
    Inherits Agent3 and Agent5
    Agent7 will be made
    to have methods and properties used in partial prey information setting from Agent3
    to have self.prey_beliefs from Agent3
    to have self.initialise_prey_beliefs() from Agent3
    to have self.update_prey_beliefs() from Agent3
    to have self.update_prey_beliefs_after_move() from Agent3
    to have self.survey_for_prey() from Agent3
    to have self.surely_knows_prey from Agent3

    to have methods used in partial predator setting by inheriting Agent5
    to have self.predator_beliefs from Agent5
    to have self.initialise_predator_beliefs() from Agent5
    to have self.update_predator_beliefs() from Agent5
    to have self.update_predator_beliefs_after_move() from Agent5
    to have self.survey_for_predator() from Agent5
    to have self.surely_knows_predator from Agent5

    will override self.agent_movement()
    '''
    def __init__(self, game):
        self.game = game
        self.game.register_agent(self)
        self.agent_loc = self.initialise_agent_location()
        self.initialise_predator_beliefs()
        self.initialise_prey_beliefs()
        # print(self.predator_beliefs)
        # print(self.prey_beliefs)

    def agent_movement(self):
        prey_probs = np.array(self.prey_beliefs)
        prey_possible_locs = list(np.where(prey_probs == prey_probs.max())[0])
        prey_loc = random.choice(prey_possible_locs)

        predator_probs = np.array(self.predator_beliefs)
        predator_possible_locs = list(np.where(predator_probs == predator_probs.max())[0])
        predator_loc = random.choice(predator_possible_locs)

        self.agent_loc = self.select_next_location_odd_agents(prey_loc, predator_loc)

        return self.agent_loc


if __name__ == "__main__":
    agent7_results = {}
    keys = ['Agent', 'no_of_simulations', 'max_steps_allowed', 'Success rate', 'Failure rate',
            'Hangs', '% knowing prey location', '% knowing predator location']
    for key in keys:
        agent7_results[key] = []

    idx = 0
    start = time.time()
    for steps_allowed in range(50, 301, 50):
        result = experiment(Agent7, num_graphs=30, simulation_per_graph=100,
                            max_steps_allowed=steps_allowed, simulator=combined_partial_info_simulator)

        for key, val in result.items():
            agent7_results[key].append(val)

        print(f'% of knowing exact prey location: {agent7_results["% knowing prey location"][idx]}')
        print(f'% of knowing exact predator location: {agent7_results["% knowing predator location"][idx]}')
        idx += 1

    print(agent7_results)
    end = time.time()

    print(f'time taken: {end-start} secs')

    with open('agent7_results.pkl', 'wb') as f:
        pickle.dump(agent7_results, f)