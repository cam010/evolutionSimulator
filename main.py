from typing import Literal, List, Tuple
from random import randint, choice
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from variables import Variables
from numpy import linspace, mean

VARIABLES = Variables()


class Organism:
    def __init__(self, type: Literal["pred", "prey"], gen: int, genome: dict = None, orig_parent_genome=None):
        self.genome = {} if genome is None else genome
        self.GEN = gen
        self.TYPE = type
        self.VARIABLES = VARIABLES
        self.orig_parent_genome = orig_parent_genome
        self.setup()

    def setup(self):
        if self.GEN == 1:
            self.generate_new_genome()
        else:
            self.mutate_genome()

        self.ENERGY_LEVEL = self.genome["starting energy level"]
        self.MINIMUM_ENERGY_LEVEL = self.genome["minimum energy level to survive"]
        if self.TYPE == "pred":
            self.COMBAT_LEVEL = self.genome["attack level"]
        elif self.TYPE == "prey":
            self.COMBAT_LEVEL = self.genome["defence level"]
        self.SPONTANEOUS_DEATH_CHANCE = self.genome["spontaneous death chance"]

    def generate_new_genome(self):
        self.genome = {}
        if self.TYPE == "pred":
            self.genome["reproduction chance"] = randint(
                self.VARIABLES.VAR13, self.VARIABLES.VAR14
            )
            self.genome["offspring amount"] = randint(
                self.VARIABLES.VAR15, self.VARIABLES.VAR16
            )
            self.genome["spontaneous death chance"] = randint(
                self.VARIABLES.VAR17, self.VARIABLES.VAR18
            )
            self.genome["starting energy level"] = randint(
                self.VARIABLES.VAR19, self.VARIABLES.VAR20
            )
            self.genome["minimum energy level to survive"] = randint(
                self.VARIABLES.VAR21, self.VARIABLES.VAR22
            )
            self.genome["attack level"] = randint(
                self.VARIABLES.VAR23, self.VARIABLES.VAR24
            )
        elif self.TYPE == "prey":
            self.genome["reproduction chance"] = randint(
                self.VARIABLES.VAR1, self.VARIABLES.VAR2
            )
            self.genome["offspring amount"] = randint(
                self.VARIABLES.VAR3, self.VARIABLES.VAR4
            )
            self.genome["spontaneous death chance"] = randint(
                self.VARIABLES.VAR5, self.VARIABLES.VAR6
            )
            self.genome["starting energy level"] = randint(
                self.VARIABLES.VAR7, self.VARIABLES.VAR8
            )
            self.genome["minimum energy level to survive"] = randint(
                self.VARIABLES.VAR9, self.VARIABLES.VAR10
            )
            self.genome["defence level"] = randint(
                self.VARIABLES.VAR11, self.VARIABLES.VAR12
            )
        if self.GEN == 1:
            self.orig_parent_genome = self.genome

    def mutate_genome(self):
        if randint(1, 100) <= self.VARIABLES.VAR27:
            self.generate_new_genome()
        self.genome["original parent genome"] = self.orig_parent_genome

    def reproduce(self) -> List:
        offspring = []
        if randint(1, 100) <= self.genome["reproduction chance"]:
            for _ in range(self.genome["offspring amount"]):
                if self.ENERGY_LEVEL >= self.MINIMUM_ENERGY_LEVEL:
                    offspring.append(Organism(self.TYPE, self.GEN + 1, self.genome, orig_parent_genome=self.orig_parent_genome))
                    self.ENERGY_LEVEL -= 1
                else:
                    break  # no point running pointless repetitions of the loop if they can't reproduce
        return offspring

    def add_energy(self, amount):
        self.ENERGY_LEVEL += amount


class Statistics:
    def __init__(self):
        # Prey
        self.OVERALL_STARTING_PREY = 0
        self.overall_prey_killed = 0
        self.generation_population_count_prey = {}
        self.generation_average_combat_levels_prey = {}
        self.total_prey_remaining = 0
        self.overall_prey_born = 0
        self.remaining_prey_from_each_gen = {}

        # Predators
        self.OVERALL_STARTING_PREDATORS = 0
        self.overall_predators_killed = 0
        self.generation_population_count_predator = {}
        self.generation_average_combat_levels_predator = {}
        self.total_predators_remaining = 0
        self.overall_predators_born = 0
        self.remaining_predators_from_each_gen = {}

        # Other
        self.current_generation = 0

    def show_results(self, predators: List[Organism], prey: List[Organism]):
        self.predators = predators
        self.prey = prey
        self.output_genomes_to_file()
        filename = "final_genomes.txt"
        print("Living Genomes outputted to {}".format(filename))
        self._print()
        self.show_graph()

    def _print(self):
        # Prey
        msg = "Prey:\n"
        msg += "\tStarting Prey: {}\n".format(self.OVERALL_STARTING_PREY)
        msg += "\tTotal Prey Remaining: {}\n".format(self.total_prey_remaining)
        msg += "\tOverall Prey Killed: {}\n".format(self.overall_prey_killed)
        msg += "\tOverall Prey Born: {}\n".format(self.overall_prey_born)
        msg += "\tPopulation of Prey After Each Generation: {}\n".format(
            self.generation_population_count_prey
        )
        msg += "\tAverage Prey Combat Levels Per Generation: {}\n".format(
            self.generation_average_combat_levels_prey
        )
        msg += "\tTotal Prey Count Left From Each Generation: {}\n".format(
            self.remaining_prey_from_each_gen
        )
        print(msg, "\n\n")
        # Predators
        msg = "Predators:\n"
        msg += "\tStarting Predators: {}\n".format(self.OVERALL_STARTING_PREDATORS)
        msg += "\tTotal Predators Remaining: {}\n".format(
            self.total_predators_remaining
        )
        msg += "\tOverall Predators Killed: {}\n".format(self.overall_predators_killed)
        msg += "\tOverall Predators Born: {}\n".format(self.overall_predators_born)
        msg += "\tPopulation of Predators After Each Generation: {}\n".format(
            self.generation_population_count_predator
        )
        msg += "\tAverage Predator Combat Levels Per Generation: {}\n".format(
            self.generation_average_combat_levels_predator
        )
        msg += "\tTotal Predator Count Left From Each Generation: {}\n".format(
            self.remaining_predators_from_each_gen
        )
        print(msg)

    def output_genomes_to_file(self):
        with open("final_genomes.txt", "w") as f:
            f.write("GENOMES OF PREDATORS\n")
            for x in self.predators:
                f.write(str(x.genome) + "Generation Born: " + str(x.GEN) + "\n")
            f.write("\n\n\n\n\n\n\n\n\n\nGENOMES OF PREY\n")
            for x in self.prey:
                f.write(str(x.genome) + "Generation Born: " + str(x.GEN) + "\n")

    def show_graph(self):
        prey_gen, prey_count = zip(*self.generation_population_count_prey.items())
        predator_gen, predator_count = zip(
            *self.generation_population_count_predator.items()
        )

        # interpolation used to make the graph more curved
        prey_interpolation = interp1d(prey_gen, prey_count, kind="cubic")
        prey_gen = linspace(min(prey_gen), max(prey_gen), 500)
        prey_count = prey_interpolation(prey_gen)

        predator_interpolation = interp1d(predator_gen, predator_count, kind="cubic")
        predator_gen = linspace(min(predator_gen), max(predator_gen), 500)
        predator_count = predator_interpolation(predator_gen)

        plt.plot(prey_gen, prey_count, color="red", label="Prey")
        plt.plot(predator_gen, predator_count, color="blue", label="Predators")
        plt.xlabel("Generation")
        plt.ylabel("Population count x1")
        plt.legend(loc="upper center")
        plt.show()


def determine_result_of_percentage_chance(chance: int, start=1, end=100):
    """Give chance as percentage.Eg for 50%, pass chance as 50. For 3%, pass chance as 3\n\nReturns True if chance occurs, else False"""
    return True if randint(start, end) <= chance else False


def check_organism_has_enough_energy(prey: List[Organism], predators: List[Organism]):
    orig_prey = len(prey)
    orig_predators = len(predators)
    prey = [x for x in prey if x.ENERGY_LEVEL >= x.MINIMUM_ENERGY_LEVEL]
    predators = [x for x in predators if x.ENERGY_LEVEL >= x.MINIMUM_ENERGY_LEVEL]
    return prey, predators, orig_prey - len(prey), orig_predators - len(predators)


def determine_combat_winner(predator: Organism, prey: Organism):
    """Returns pred if predator is better in combat, else prey if it is a draw/prey wins"""
    chance_of_predator_win = 20 + predator.COMBAT_LEVEL - prey.COMBAT_LEVEL
    return (
        "pred"
        if determine_result_of_percentage_chance(chance_of_predator_win)
        else "prey"
    )


def add_energy_to_prey(prey: List[Organism]):
    PREY_AMOUNT_TO_HALF_ENERGY_ADDED = 10_000
    PREY_AMOUNT_TO_QUATER_ENERGY_ADDED = 20_000
    PREY_AMOUNT_TO_REMOVE_QUATER_ENERGY = 50_000
    PREY_AMOUNT_TO_REMOVE_HALF_ENERGY = 70_000
    to_add = VARIABLES.VAR26
    prey_amount = len(prey)

    if prey_amount >= PREY_AMOUNT_TO_REMOVE_HALF_ENERGY:
        to_add = -to_add
    elif prey_amount >= PREY_AMOUNT_TO_REMOVE_QUATER_ENERGY:
        to_add = -(to_add / 4)
    elif prey_amount >= PREY_AMOUNT_TO_QUATER_ENERGY_ADDED:
        to_add = to_add // 4
    elif prey_amount >= PREY_AMOUNT_TO_HALF_ENERGY_ADDED:
        to_add = to_add // 2

    for x in prey:
        x.add_energy(to_add)


def simulate_overcrowding(prey) -> Tuple[List[Organism], int]:
    MAX_CAPACITY_FOR_POPULATION = 1000
    prey_amount = len(prey)
    if prey_amount >= MAX_CAPACITY_FOR_POPULATION:
        prey = [x for x in prey if determine_result_of_percentage_chance(25)]
    prey_killed = prey_amount - len(prey)
    return prey, prey_killed


def simulate_spontaneous_death(
    predators: List[Organism], prey: List[Organism]
) -> Tuple[List[Organism], List[Organism], int, int]:
    """Returns: New Predators, New Prey, Predators Killed, Prey Killed"""
    orig_predator_length = len(predators)
    orig_prey_length = len(prey)
    prey = [
        x
        for x in prey
        if not determine_result_of_percentage_chance(x.SPONTANEOUS_DEATH_CHANCE)
    ]
    predators = [
        x
        for x in predators
        if not determine_result_of_percentage_chance(x.SPONTANEOUS_DEATH_CHANCE)
    ]
    predators_killed = orig_predator_length - len(predators)
    prey_killed = orig_prey_length - len(prey)
    return predators, prey, predators_killed, prey_killed


def simulate_reproduction(predators: List[Organism], prey: List[Organism]):
    new_predators = [y for x in predators for y in x.reproduce()]
    new_prey = [y for x in prey for y in x.reproduce()]
    predators_produced = len(new_predators)
    prey_produced = len(new_prey)
    return new_predators, new_prey, predators_produced, prey_produced


def simulate_hunting(predators, prey):
    predator_length = len(predators)
    prey_length = len(prey)
    if predator_length > prey_length:
        # removes surplus predators from predator list, puts them into
        # their own list
        # ABOVE COMMENT FUNCTIONALITY REMOVED, SURPLUS PREDATORS NOW JUST DIE
        predators = predators[:prey_length]

    new_prey = []
    new_predators = []
    for i, x in enumerate(predators):
        winner = determine_combat_winner(x, prey[i])
        if winner == "prey":
            new_prey.append(prey[i])
            CHANCE_OF_PREY_KILLING_PREDATOR = 50
            if determine_result_of_percentage_chance(CHANCE_OF_PREY_KILLING_PREDATOR):
                new_predators.append(x)
        else:
            # simulate transfer of energy
            x.ENERGY_LEVEL += prey[i].ENERGY_LEVEL * VARIABLES.VAR30
            new_predators.append(x)

    new_prey += prey[i:]  # this adds all prey that wasn't "attacked" to the list
    predators_killed = predator_length - len(new_predators)
    prey_killed = prey_length - len(new_prey)
    return new_predators, new_prey, predators_killed, prey_killed


######################
## SIMULATION SETUP ##
######################
predators = list([Organism("pred", 1) for _ in range(VARIABLES.VAR28)])
prey = [Organism("prey", 1) for _ in range(VARIABLES.VAR29)]
current_generation = 1

######################
## STATISTICS SETUP ##
######################
stats = Statistics()
stats.OVERALL_STARTING_PREY = VARIABLES.VAR28
stats.OVERALL_STARTING_PREDATORS = VARIABLES.VAR29
stats.generation_average_combat_levels_prey[1] = mean([x.COMBAT_LEVEL for x in prey])
stats.generation_average_combat_levels_predator[1] = mean(
    [x.COMBAT_LEVEL for x in predators]
)
stats.generation_population_count_prey[1] = len(prey)
stats.generation_population_count_predator[1] = len(predators)

######################################################
################ MAIN LOOP ###########################
######################################################

while True:
    # Stage 1 -> Add/Remove energy
    # Stage 2 -> Simulate overcrowding
    # Destroy organisms that have a too low energy level
    # Stage 3 -> Reproduction
    # Destroy organisms that have a too low energy level
    # Stage 4 -> Hunting
    # Stage 5 -> Spontaneous Death

    # values for stats
    starting_prey = len(prey)
    starting_predators = len(predators)
    predators_killed_this_generation = 0
    prey_killed_this_generation = 0

    ############################
    ######### STAGE 1 ##########
    ############################
    ##### Energy Transfers #####
    ############################
    # remove energy from predators
    for x in predators:
        x.add_energy(VARIABLES.VAR33)

    # add energy to prey
    add_energy_to_prey(prey)

    ############################
    ######### STAGE 2 ##########
    ############################
    ####### Overcrowding #######
    ############################
    prey, prey_killed = simulate_overcrowding(prey)
    prey_killed_this_generation += prey_killed

    ############################
    ### Destroying Organisms ###
    ############################
    # destroy organisms with a too low energy level
    prey, predators, prey_killed, pred_killed = check_organism_has_enough_energy(
        prey, predators
    )
    prey_killed_this_generation += prey_killed
    predators_killed_this_generation += pred_killed

    ############################
    ######### STAGE 3 ##########
    ############################
    ###### Reproduction ########
    ############################
    (
        new_predators,
        new_prey,
        new_predators_produced,
        new_prey_produced,
    ) = simulate_reproduction(predators, prey)
    predators += new_predators
    prey += new_prey

    # for stats
    stats.overall_predators_born += new_predators_produced
    stats.overall_prey_born += new_prey_produced
    stats.generation_average_combat_levels_prey[current_generation + 1] = round(
        mean([x.COMBAT_LEVEL for x in new_prey]), 2
    )
    stats.generation_average_combat_levels_predator[current_generation + 1] = round(
        mean([x.COMBAT_LEVEL for x in new_predators]), 2
    )
    del new_predators
    del new_prey

    ############################
    ### Destroying Organisms ###
    ############################
    prey, predators, prey_killed, pred_killed = check_organism_has_enough_energy(
        prey, predators
    )
    prey_killed_this_generation += prey_killed
    predators_killed_this_generation += pred_killed

    ############################
    ######### STAGE 4 ##########
    ############################
    ######### Hunting ##########
    ############################
    predators, prey, predators_killed, prey_killed = simulate_hunting(predators, prey)
    predators_killed_this_generation += predators_killed
    prey_killed_this_generation += prey_killed

    ############################
    ######### STAGE 5 ##########
    ############################
    #### Spontaneous Deaths ####
    ############################
    predators, prey, predators_killed, prey_killed = simulate_spontaneous_death(
        predators, prey
    )
    predators_killed_this_generation += predators_killed
    prey_killed_this_generation += prey_killed

    ############################
    ######### STAGE 6 ##########
    ############################
    ## Finish And Post Cycles ##
    ############################

    # end of cycle outputs
    print("Generation {} complete".format(current_generation))

    # Tracking stats
    stats.overall_predators_killed += predators_killed_this_generation
    stats.overall_prey_killed += prey_killed_this_generation
    stats.generation_population_count_prey[current_generation+1] = len(prey)
    stats.generation_population_count_predator[current_generation+1] = len(predators)

    end_sim = False
    if len(prey) <= 0 or len(predators) <= 0:
        end_sim = True
        stats.total_prey_remaining = len(prey)
        stats.total_predators_remaining = len(predators)

    if current_generation == VARIABLES.VAR32 or end_sim:
        for i in range(VARIABLES.VAR32):
            stats.remaining_prey_from_each_gen[i + 1] = len(
                [x for x in prey if x.GEN == i + 1]
            )
            stats.remaining_predators_from_each_gen[i + 1] = len(
                [x for x in predators if x.GEN == i + 1]
            )
        stats.current_generation = current_generation
        stats.total_predators_remaining = len(predators)
        stats.total_prey_remaining = len(prey)
        print(
            "Simulation Over at generation: {}\nOutputting Statistics...\n\n".format(
                current_generation
            )
        )
        stats.show_results(predators, prey)
        break

    # Increment generation
    current_generation += 1
