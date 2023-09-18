import time
import numpy as np
import random
import pickle
from Agent8 import Agent8
from utilities import experiment
from simulators import faulty_drone_simulator


class FaultyAgent8(Agent8):
    '''
     FaultyAgent8 will have methods used in Combined Partial Information setting by inheriting Agent8
     along with methods which have better way to select a node to move forward in even numbered agents.

    and define two new methods for faulty survey for both prey and predator
    '''
    def __init__(self, game):
        super().__init__(game)

    def faulty_survey_for_prey(self):
        survey_node, is_prey_present = self.survey_for_prey()

        if is_prey_present:
            make_faulty = (random.uniform(0, 1) <= 0.1)
            if make_faulty:
                return survey_node, not is_prey_present
            else:
                return survey_node, is_prey_present

        return survey_node, is_prey_present

    def faulty_survey_for_predator(self):
        survey_node, is_predator_present = self.survey_for_predator()

        if is_predator_present:
            make_faulty = (random.uniform(0, 1) <= 0.1)
            if make_faulty:
                return survey_node, not is_predator_present
            else:
                return survey_node, is_predator_present

        return survey_node, is_predator_present


if __name__ == "__main__":
    agent8_results = {}
    keys = ['Agent', 'no_of_simulations', 'max_steps_allowed', 'Success rate', 'Failure rate',
            'Hangs', '% knowing prey location', '% knowing predator location']

    for key in keys:
        agent8_results[key] = []

    idx = 0
    start = time.time()
    for steps_allowed in range(50, 301, 50):
        result = experiment(FaultyAgent8, num_graphs=30, simulation_per_graph=100,
                            max_steps_allowed=steps_allowed, simulator=faulty_drone_simulator)

        for key, val in result.items():
            agent8_results[key].append(val)

        print(f'% of knowing exact prey location: {agent8_results["% knowing prey location"][idx]}')
        print(f'% of knowing exact predator location: {agent8_results["% knowing predator location"][idx]}')
        idx += 1

    print(agent8_results)
    end = time.time()

    print(f'time taken: {end-start} secs')

    with open('faulty_agent8_results.pkl', 'wb') as f:
        pickle.dump(agent8_results, f)