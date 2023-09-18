import time
import numpy as np
import random
import pickle
from Game import Game
from Agent2 import Agent2
from Agent5 import Agent5
from utilities import experiment
from simulators import partial_predator_info_simulator


class Agent6(Agent2, Agent5):
    '''
        Inherits Agent2, and Agent5 that will make Agent6 to mimic Agent5 along with functionalities of Agent2
        Agent6 will be made

        to have methods used in partial predator setting by inheriting Agent5
        to have self.predator_beliefs from Agent5
        to have self.initialise_predator_beliefs() from Agent5
        to have self.update_predator_beliefs() from Agent5
        to have self.update_predator_beliefs_after_move() from Agent5
        to have self.survey_for_predator() from Agent5
        to have self.surely_knows_predator from Agent5

        to have methods to perform better than Agent3 using methods inherited from Agent2
        to have self.estimate_future_prey_loc() from Agent2
        to have self.select_next_location_even_agents() from Agent2
        will override self.agent_movement()
    '''
    def __init__(self, game: Game):
        Agent5.__init__(self, game)

    def agent_movement(self):
        predator_probs = np.array(self.predator_beliefs)
        predator_possible_locs = list(np.where(predator_probs == predator_probs.max())[0])

        predator_loc = random.choice(predator_possible_locs)
        prey_loc = self.game.get_prey_loc()
        future_prey_loc = self.estimate_future_prey_loc(prey_loc)

        self.agent_loc = self.select_next_location_even_agents(future_prey_loc, predator_loc)
        return self.agent_loc


if __name__ == "__main__":
    agent6_results = {}
    keys = ['Agent', 'no_of_simulations', 'max_steps_allowed', 'Success rate', 'Failure rate',
            'Hangs', '% knowing prey location', '% knowing predator location']
    for key in keys:
        agent6_results[key] = []

    idx = 0
    start = time.time()
    for steps_allowed in range(50, 301, 50):
        result = experiment(Agent6, num_graphs=30, simulation_per_graph=100,
                            max_steps_allowed=steps_allowed, simulator=partial_predator_info_simulator)

        for key, val in result.items():
            agent6_results[key].append(val)

        print(f'% of knowing exact predator location: {agent6_results["% knowing predator location"][idx]}')
        idx += 1

    print(agent6_results)
    end = time.time()

    print(f'time taken: {end - start} secs')

    with open('agent6_results.pkl', 'wb') as f:
        pickle.dump(agent6_results, f)