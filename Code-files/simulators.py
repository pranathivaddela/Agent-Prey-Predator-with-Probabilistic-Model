import random



def complete_info_simulator(game, agent, predator, prey, max_steps_allowed):
    ''' For given agent, predator and prey in mentioned game, this function will simulate the
    Circle of life using the methods of participant objects (agent, prey & predator)
            in COMPLETE INFORMATION SETTING.

        This simulator is used for Agent1 and Agent2 objects only.

    :return  result of this simulation.
            steps_took - steps_took to complete this simulation
                            (used to calculate % of knowing predator or prey)
            success - (boolean, specifying the result of agent in this simulation)
            hang - (boolean, specifies whether the game has ended
                                (either agent catches prey or predator catches agent) or not
            n_knows_prey - specifies in how many steps agent knows about
                            exact location of prey in this simulation
            n_knows_predator - specifies in how many steps agent knows about
                                exact location of predator in this simulation
    '''
    steps_took = 0
    success = False
    game_ended = False

    n_knows_prey = 0
    n_knows_predator = 0
    while steps_took <= max_steps_allowed:
        steps_took += 1

        # print("Agent is at:", game.get_agent_loc())
        agent.agent_movement()
        # print("Agent moved to:", game.get_agent_loc())

        # check if agent entered into predator's cell
        if game.get_agent_loc() == game.get_predator_loc():
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        # check if agent entered into prey's cell
        if game.get_agent_loc() == game.get_prey_loc():
            # print(" Gotcha: WIN ")
            success = True
            game_ended = True
            break

        # print("Prey at:", game.get_prey_loc())
        prey.prey_movement()
        # print("Prey moved to:", game.get_prey_loc())

        # check if agent entered into prey's cell
        if game.get_agent_loc() == game.get_prey_loc():
            # print(" Gotcha: WIN ")
            success = True
            game_ended = True
            break

        # print("Predator at:", game.get_predator_loc())
        predator.predator_movement()
        # print("Predator moved to: ", game.get_predator_loc())

        # check if agent entered into predator's cell
        if game.get_agent_loc() == game.get_predator_loc():
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

    # if game not ended in max_steps_allowed, it means a hang
    hang = not game_ended
    # In complete information setting agent knows location of prey and predator in every step
    n_knows_prey = n_knows_predator = steps_took

    return success, steps_took, hang, n_knows_prey, n_knows_predator


def partial_prey_info_simulator(game, agent, predator, prey, max_steps_allowed):
    ''' For given agent, predator and prey in mentioned game, this function will simulate the
        Circle of life using the methods of participant objects (agent, prey & predator)
                in PARTIAL PREY INFORMATION SETTING.

            This simulator is used for Agent3 and Agent4 objects only.

        :return  result of this simulation.
                steps_took - steps_took to complete this simulation
                                (used to calculate % of knowing predator or prey)
                success - (boolean, specifying the result of agent in this simulation)
                hang - (boolean, specifies whether the game has ended
                                    (either agent catches prey or predator catches agent) or not
                n_knows_prey - specifies in how many steps agent knows about
                                exact location of prey in this simulation
                n_knows_predator - specifies in how many steps agent knows about
                                    exact location of predator in this simulation
        '''
    steps_took = 0
    success = False
    game_ended = False

    n_knows_prey = 0
    n_knows_predator = 0

    while steps_took <= max_steps_allowed:
        steps_took += 1

        survey_node, is_prey_present = agent.survey_for_prey()
        probs = agent.update_prey_beliefs(survey_node, is_prey_present)
        # print(1, sum(probs), steps)
        #print(sum(probs))

        agent.agent_movement()

        if agent.agent_loc == predator.predator_loc:
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        if agent.agent_loc == prey.prey_loc:
            # print(" Gotcha: WIN ")
            game_ended = True
            success = True
            break

        probs = agent.update_prey_beliefs(agent.get_location(), is_prey_present=False)
        # print(2, sum(probs), steps)
        #print(sum(probs))

        n_knows_prey += agent.surely_knows_prey()

        # print("Prey at:", prey.prey_loc)
        prey.prey_movement()
        # print("Prey moved to:", prey.prey_loc)

        if agent.agent_loc == prey.prey_loc:
            # print(" Gotcha: WIN ")
            game_ended = True
            success = True
            break

        # print("Predator at:", predator.predator_loc)
        predator.predator_movement()
        # print("Predator moved to: ", predator.predator_loc)

        if agent.agent_loc == predator.predator_loc:
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        probs = agent.update_prey_beliefs_after_move()
        # print(3, sum(probs), steps)
        #print(sum(probs))

    hang = not game_ended
    n_knows_predator = steps_took

    return success, steps_took, hang, n_knows_prey, n_knows_predator


def partial_predator_info_simulator(game, agent, predator, prey, max_steps_allowed):
    '''
    this function will simulate the
        Circle of life using the methods of participant objects (agent, prey & predator)
                in PARTIAL PREDATOR INFORMATION SETTING.

            This simulator is used for Agent5 and Agent6 objects only.
        return success, steps_took, hang, n_knows_prey, n_knows_predator
    '''
    steps_took = 0
    success = False
    game_ended = False

    n_knows_predator = 0
    n_knows_prey = 0

    while steps_took <= max_steps_allowed:
        steps_took += 1

        survey_node, is_predator_present = agent.survey_for_predator()

        probs = agent.update_predator_beliefs(survey_node, is_predator_present)
        # print(1, sum(probs), steps, game.graph.re)
        #print(sum(probs))

        agent.agent_movement()

        if agent.agent_loc == predator.predator_loc:
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        if agent.agent_loc == prey.prey_loc:
            # print(" Gotcha: WIN ")
            game_ended = True
            success = True
            break

        probs = agent.update_predator_beliefs(agent.get_location(), is_predator_present=False)
        # print(2, sum(probs), steps, game.graph.re)
        #print(sum(probs))

        n_knows_predator += agent.surely_knows_predator()

        prey.prey_movement()

        if agent.agent_loc == prey.prey_loc:
            # print(" Gotcha: WIN ")
            game_ended = True
            success = True
            break

        predator.distracted_predator_movement()

        if agent.agent_loc == predator.predator_loc:
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        probs = agent.update_predator_beliefs_after_move()
        # print(3, sum(probs), steps, game.graph.re)
        #print(sum(probs))

    hang = not game_ended
    n_knows_prey = steps_took

    return success, steps_took, hang, n_knows_prey, n_knows_predator


def combined_partial_info_simulator(game, agent, predator, prey, max_steps_allowed):
    '''
        this function will simulate the
        Circle of life using the methods of participant objects (agent, prey & predator)
                in COMBINED PARTIAL INFORMATION SETTING.

            This simulator is used for Agent7 and Agent8 objects only.

        return success, steps_took, hang, n_knows_prey, n_knows_predator
    '''
    steps_took = 0
    success = False
    game_ended = False

    n_knows_prey = 0
    n_knows_predator = 0

    while steps_took <= max_steps_allowed:
        steps_took += 1

        if agent.surely_knows_predator():
            survey_node, is_prey_present = agent.survey_for_prey()
            probs = agent.update_prey_beliefs(survey_node, is_prey_present)
            #print(sum(probs))
        else:
            survey_node, is_predator_present = agent.survey_for_predator()
            probs = agent.update_predator_beliefs(survey_node, is_predator_present)
            #print(sum(probs))

            is_prey_present = (game.get_prey_loc() == survey_node)
            probs = agent.update_prey_beliefs(survey_node, is_prey_present)
            #print(sum(probs))

        # 3. agent moves to a node according to calculated beliefs
        # print("Agent is at:", agent.agent_loc)
        agent.agent_movement()
        # print("Agent moved to:", agent.agent_loc)

        if agent.agent_loc == predator.predator_loc:
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        if agent.agent_loc == prey.prey_loc:
            # print(" Gotcha: WIN ")
            game_ended = True
            success = True
            break

        # Agent gains knowledge from the new position
        # updates the beliefs according to acquired knowledge
        probs = agent.update_prey_beliefs(agent.get_location(), is_prey_present=False)
        #print(sum(probs))

        probs = agent.update_predator_beliefs(agent.get_location(), is_predator_present=False)
        #print(sum(probs))

        n_knows_prey += agent.surely_knows_prey()
        n_knows_predator += agent.surely_knows_predator()

        # print("Prey at:", prey.prey_loc)
        prey.prey_movement()
        # print("Prey moved to:", prey.prey_loc)

        if agent.agent_loc == prey.prey_loc:
            # print(" Gotcha: WIN ")
            game_ended = True
            success = True
            break

        # print("Predator at:", predator.predator_loc)
        predator.distracted_predator_movement()
        # print("Predator moved to: ", predator.predator_loc)

        if agent.agent_loc == predator.predator_loc:
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        probs = agent.update_prey_beliefs_after_move()
        #print(sum(probs))

        probs = agent.update_predator_beliefs_after_move()
        # print(sum(probs))

    hang = not game_ended

    return success, steps_took, hang, n_knows_prey, n_knows_predator


def faulty_drone_simulator(game, agent, predator, prey, max_steps_allowed):
    '''
            this function will simulate the
            Circle of life using the methods of participant objects (agent, prey & predator)
                    in COMBINED PARTIAL INFORMATION SETTING, where agent is using FAULTY DRONE.

                This simulator is used for FaultyAgent7 and FaultyAgent8 objects only.

            return success, steps_took, hang, n_knows_prey, n_knows_predator
        '''
    steps_took = 0
    success = False
    game_ended = False

    n_knows_prey = 0
    n_knows_predator = 0

    while steps_took <= max_steps_allowed:
        steps_took += 1

        if agent.surely_knows_predator():
            survey_node, is_prey_present = agent.faulty_survey_for_prey()
            probs = agent.update_prey_beliefs(survey_node, is_prey_present)
            # print(sum(probs))
        else:
            survey_node, is_predator_present = agent.faulty_survey_for_predator()
            probs = agent.update_predator_beliefs(survey_node, is_predator_present)


            is_prey_present = (game.get_prey_loc() == survey_node)
            probs = agent.update_prey_beliefs(survey_node, is_prey_present)
            # print(sum(probs))

        # 3. agent moves to a node according to calculated beliefs
        # print("Agent is at:", agent.agent_loc)
        agent.agent_movement()
        # print("Agent moved to:", agent.agent_loc)

        if agent.agent_loc == predator.predator_loc:
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        if agent.agent_loc == prey.prey_loc:
            # print(" Gotcha: WIN ")
            game_ended = True
            success = True
            break

        # Agent gains knowledge from the new position
        # updates the beliefs according to acquired knowledge
        probs = agent.update_prey_beliefs(agent.get_location(), is_prey_present=False)

        probs = agent.update_predator_beliefs(agent.get_location(), is_predator_present=False)

        n_knows_prey += agent.surely_knows_prey()
        n_knows_predator += agent.surely_knows_predator()

        # print("Prey at:", prey.prey_loc)
        prey.prey_movement()
        # print("Prey moved to:", prey.prey_loc)

        if agent.agent_loc == prey.prey_loc:
            # print(" Gotcha: WIN ")
            game_ended = True
            success = True
            break

        # print("Predator at:", predator.predator_loc)
        predator.distracted_predator_movement()
        # print("Predator moved to: ", predator.predator_loc)

        if agent.agent_loc == predator.predator_loc:
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        probs = agent.update_prey_beliefs_after_move()

        probs = agent.update_predator_beliefs_after_move()

    hang = not game_ended

    return success, steps_took, hang, n_knows_prey, n_knows_predator


def smart_simulator_for_faulty_drone(game, agent, predator, prey, max_steps_allowed):
    '''
        this function will simulate the
        Circle of life using the methods of participant objects (agent, prey & predator)
            in COMBINED PARTIAL INFORMATION SETTING,
            where agent is using FAULTY DRONE and updating beliefs according to the faulty surveys.

        This simulator is used for IntelligentAgent7 and IntelligentAgent8 objects only.

        return success, steps_took, hang, n_knows_prey, n_knows_predator
    '''
    steps_took = 0
    success = False
    game_ended = False

    n_knows_prey = 0
    n_knows_predator = 0

    while steps_took <= max_steps_allowed:
        steps_took += 1

        if agent.surely_knows_predator():
            survey_node, is_prey_present = agent.faulty_survey_for_prey()
            probs = agent.update_prey_beliefs(survey_node, is_prey_present, True)
            #print(sum(probs))
        else:
            survey_node, is_predator_present = agent.faulty_survey_for_predator()
            probs = agent.update_predator_beliefs(survey_node, is_predator_present, True)
            #print(sum(probs))

            is_prey_present = (game.get_prey_loc() == survey_node)
            # if is_prey_present:
            #     if random.uniform(0, 1) <= 0.1:
            #         is_prey_present = False
            probs = agent.update_prey_beliefs(survey_node, is_prey_present, False)
            #print(sum(probs))

        # 3. agent moves to a node according to calculated beliefs
        # print("Agent is at:", agent.agent_loc)
        agent.agent_movement()
        # print("Agent moved to:", agent.agent_loc)

        if agent.agent_loc == predator.predator_loc:
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        if agent.agent_loc == prey.prey_loc:
            # print(" Gotcha: WIN ")
            game_ended = True
            success = True
            break

        # Agent gains knowledge from the new position
        # updates the beliefs according to acquired knowledge
        probs = agent.update_prey_beliefs(agent.get_location(), False, False)
        # print(sum(probs))

        probs = agent.update_predator_beliefs(agent.get_location(), False, False)
        # print(sum(probs))

        n_knows_prey += agent.surely_knows_prey()
        n_knows_predator += agent.surely_knows_predator()

        # print("Prey at:", prey.prey_loc)
        prey.prey_movement()
        # print("Prey moved to:", prey.prey_loc)

        if agent.agent_loc == prey.prey_loc:
            # print(" Gotcha: WIN ")
            game_ended = True
            success = True
            break

        # print("Predator at:", predator.predator_loc)
        predator.distracted_predator_movement()
        # print("Predator moved to: ", predator.predator_loc)

        if agent.agent_loc == predator.predator_loc:
            # print("Predator got the Agent : LOST")
            game_ended = True
            break

        probs = agent.update_prey_beliefs_after_move()
        # print(sum(probs))

        probs = agent.update_predator_beliefs_after_move()
        #print(sum(probs))

    hang = not game_ended

    return success, steps_took, hang, n_knows_prey, n_knows_predator