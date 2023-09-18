import random
from Game import Game
from Agent1 import Agent1
from utilities import experiment
import pickle


class TestAgent(Agent1):

    def __init__(self, game: Game):
        super().__init__(game)

    def agent_movement(self):
        prey_loc = self.game.get_prey_loc()
        neighbors = self.game.get_neighbors(self.agent_loc)

        prey_dist = []

        for neighbor in neighbors:
            prey_dist.append(self.game.shortest_dist(neighbor, prey_loc))

        min_prey_dist = min(prey_dist)
        agent_next_possible_locs = []

        for neighbor, distance in zip(neighbors, prey_dist):
            if distance == min_prey_dist:
                agent_next_possible_locs.append(neighbor)

        self.agent_loc = random.choice(agent_next_possible_locs)
        return self.agent_loc


def simulate(game, agent, predator, prey, max_steps_allowed):
    steps = 0
    success = False
    game_ended = False
    while steps <= max_steps_allowed:
        steps += 1

        # print("**************************************************")

        # print("Agent is at:", game.get_agent_loc())
        agent.agent_movement()
        # print("Agent moved to:", game.get_agent_loc())

        if game.get_agent_loc() == game.get_predator_loc():
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        if game.get_agent_loc() == game.get_prey_loc():
            # print(" Gotcha: WIN ")
            success = True
            game_ended = True
            break

        # print("Prey at:", game.get_prey_loc())
        prey.prey_movement()
        # print("Prey moved to:", game.get_prey_loc())

        if game.get_agent_loc() == game.get_prey_loc():
            # print(" Gotcha: WIN ")
            success = True
            game_ended = True
            break

        # print("Predator at:", game.get_predator_loc())
        predator.predator_movement()
        # print("Predator moved to: ", game.get_predator_loc())

        if game.get_agent_loc() == game.get_predator_loc():
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

    hang = not game_ended
    # print(f'steps took is {steps}')
    return success, steps, hang


if __name__ == "__main__":
    test_agent_results = {}
    keys = ['Agent', 'no_of_simulations', 'max_steps_allowed', 'Success rate', 'Failure rate', 'Hang rate']
    for key in keys:
        test_agent_results[key] = []

    for steps_allowed in range(50, 301, 50):
        result = experiment(TestAgent, num_graphs=30, simulation_per_graph=100,
                            max_steps_allowed=steps_allowed, simulator=simulate)

        for key, val in zip(keys, result):
            test_agent_results[key].append(val)

    print(test_agent_results)

    # with open('TestAgent.pkl', 'wb') as f:
    #     pickle.dump(test_agent_results, f)