from collections import defaultdict
from Environment import Graph
from Prey import Prey
from Predator import Predator
from Game import Game
from statistics import mean



def experiment(Agentclass, num_graphs, simulation_per_graph, max_steps_allowed, simulator):
    num_simulations = num_graphs * simulation_per_graph
    success_rates = []
    hang_rates = []
    failure_rates = []
    exactly_knows_prey = 0
    exactly_knows_predator = 0
    total_steps = 0
    hangs_num = 0
    for i in range(num_graphs):
        game = Game()
        G = Graph(50, game)
        results = []
        hangs = []


        for j in range(simulation_per_graph):
            predator = Predator(game)
            prey = Prey(game)
            agent = Agentclass(game)
            result, steps, hang, n_knows_prey, n_knows_predator \
                = simulator(game, agent, predator, prey, max_steps_allowed)
            # steps_dist[steps] += 1
            results.append(result)
            hangs.append(hang)

            exactly_knows_prey += n_knows_prey
            exactly_knows_predator += n_knows_predator
            total_steps += steps

        success_rate = sum(results) / len(results)
        hang_rate = sum(hangs) / len(hangs)
        failure_rate = 1 - (success_rate + hang_rate)
        # hang_num += len(hangs)

        success_rates.append(success_rate)
        hang_rates.append(hang_rate)
        failure_rates.append(failure_rate)

    overall_success_rate = round(mean(success_rates), 4)
    overall_hang_rate = round(mean(hang_rates), 4)
    overall_failure_rate = round(mean(failure_rates), 4)
    # total_hangs = hangs_num

    rates = [overall_success_rate, overall_failure_rate, overall_hang_rate]

    print('--------------- Configuration for this experiment ---------------')
    print(f'Agent is of type: {type(agent).__name__}')
    print(f'Number of simulations: {num_simulations}')
    print(f'Maximum number of steps allowed in a game(steps threshold): {max_steps_allowed}')
    print('-----------------------------------------------------------------')

    print(f'Results of this experiment ({type(agent).__name__}) as follows...\n')
    print("{:<15} {:<15} {:<15}".format('Success rate', 'Failure rate', 'Hang rate'))
    print("{:<15} {:<15} {:<15}".format(*rates))
    print()

    perc_knowing_prey = round(100*(exactly_knows_prey / total_steps), 2)
    perc_knowing_predator = round(100*(exactly_knows_predator / total_steps), 2)

    simulation_result = {'Agent': type(agent).__name__,
                         'no_of_simulations': num_simulations,
                         'max_steps_allowed': max_steps_allowed,
                         'Success rate': overall_success_rate*100,
                         'Failure rate': overall_failure_rate*100,
                         'Hangs': int(overall_hang_rate*3000),
                         '% knowing prey location': perc_knowing_prey,
                         '% knowing predator location': perc_knowing_predator}

    return simulation_result
