from typing import Literal, List
from random import randint, choice
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from variables import Variables
from numpy import linspace, mean
from pprint import pprint

VARIABLES = Variables()

class Organism:
    def __init__(self, type: Literal["pred", "prey"], gen: int, genome: dict=None):
        self.genome = {} if genome is None else genome
        self.gen = gen
        self.type = type
        self.variables = VARIABLES
        self.setup()
        
    def setup(self):
        if self.gen == 1:
            self.generate_new_genome()
        else:
            self.mutate_genome()
        
        self.energy_level = self.genome["starting energy level"]
        self.minimum_energy_level = self.genome["minimum energy level to survive"]
        if self.type == "pred":
            self.combat_level = self.genome["attack level"]
        elif self.type == "prey":
            self.combat_level = self.genome["defence level"]
        self.spontaneous_death_chance = self.genome["spontaneous death chance"]
        
    def generate_new_genome(self):
        self.genome = {}
        if self.type == "pred":
            self.genome["reproduction chance"] = randint(self.variables.var13, self.variables.var14)
            self.genome["offspring amount"] = randint(self.variables.var15, self.variables.var16)
            self.genome["spontaneous death chance"] = randint(self.variables.var17, self.variables.var18)
            self.genome["starting energy level"] = randint(self.variables.var19, self.variables.var20)
            self.genome["minimum energy level to survive"] = randint(self.variables.var21, self.variables.var22)
            self.genome["attack level"] = randint(self.variables.var23, self.variables.var24)
        elif self.type == "prey":
            self.genome["reproduction chance"] = randint(self.variables.var1, self.variables.var2)
            self.genome["offspring amount"] = randint(self.variables.var3, self.variables.var4)
            self.genome["spontaneous death chance"] = randint(self.variables.var5, self.variables.var6)
            self.genome["starting energy level"] = randint(self.variables.var7, self.variables.var8)
            self.genome["minimum energy level to survive"] = randint(self.variables.var9, self.variables.var10)
            self.genome["defence level"] = randint(self.variables.var11, self.variables.var12)
    
    def mutate_genome(self):
        if randint(1, 100) <= self.variables.var27:
            self.generate_new_genome()
    
    def reproduce(self):
        offspring = []
        if randint(1, 100) <= self.genome["reproduction chance"]:
            for _ in range(self.genome["offspring amount"]):
                if self.energy_level >= self.minimum_energy_level:
                    offspring.append(Organism(self.type, self.gen+1, self.genome))
                    self.energy_level -= 1
                else:
                    break # no point running pointless repetitions of the loop if they can't reproduce
        return offspring
    
    def add_energy(self, amount):
        self.energy_level += amount

def determine_result_of_percentage_chance(chance: int, start=1, end=100):
    """Give chance as percentage.Eg for 50%, pass chance as 50. For 3%, pass chance as 3\n\nReturns True if chance occurs, else False"""
    return True if randint(start, end) <= chance else False

def check_organism_has_enough_energy(prey: List[Organism], predators: List[Organism]):
    orig_prey = len(prey)
    orig_predators = len(predators)
    prey = [x for x in prey if x.energy_level >= x.minimum_energy_level]
    predators = [x for x in predators if x.energy_level >= x.minimum_energy_level]
    return prey, predators, orig_prey-len(prey), orig_predators-len(predators)

def determine_combat_winner(predator: Organism, prey: Organism):
    """Returns pred if predator is better in combat, else prey if it is a draw/prey wins"""
    chance_of_predator_win = 20 + predator.combat_level - prey.combat_level
    return "pred" if randint(1, 100) <= chance_of_predator_win else "prey"

def add_energy_to_prey(prey: List[Organism]):
    prey_amount_to_half_energy_added = 10_000
    prey_amount_to_quater_energy_added = 20_000
    prey_amount_to_remove_quater_energy = 50_000
    prey_amount_to_remove_half_energy = 70_000
    to_add = VARIABLES.var26
    
    if len(prey) >= prey_amount_to_remove_half_energy:
        to_add = -to_add
    elif len(prey) >= prey_amount_to_remove_quater_energy:
        to_add = -(to_add / 4)
    elif len(prey) >= prey_amount_to_quater_energy_added:
        to_add = to_add // 4
    elif len(prey) >= prey_amount_to_half_energy_added:
        to_add = to_add // 2
        
    for x in prey:
        x.add_energy(to_add)

def simulate_overcrowding(prey):
    max_capacity_for_population = 1000
    if len(prey) >= max_capacity_for_population:
        new_prey = []
        new_prey = [x for x in prey if determine_result_of_percentage_chance(25)]
        for x in prey:
            if determine_result_of_percentage_chance(25):
                new_prey.append(x)
            else:
                total_prey_killed += 1
        prey = [x for x in new_prey]
        del new_prey
    
# simulation counters
predators = [Organism("pred", 1) for _ in range(VARIABLES.var28)]
prey = [Organism("prey", 1) for _ in range(VARIABLES.var29)]
current_generation = 1

# values for print statemets
overall_starting_prey = len(prey)
overall_starting_predators = len(predators)
overall_total_predators_killed = 0
overall_total_prey_killed = 0
generation_average_combat_levels = {}
generation_average_combat_levels["prey, {}".format(1)] = mean([x.combat_level for x in prey])
generation_average_combat_levels["predator, {}".format(1)] = mean([x.combat_level for x in predators])
generation_population_count_prey = {1:len(prey)}
generation_population_count_predator = {1:len(predators)}

while True:
    # values for print statemets
    starting_prey = len(prey)
    starting_predators = len(predators)
    total_predators_killed = 0
    total_prey_killed = 0
    
    # remove energy from predators
    for x in predators:
        x.add_energy(VARIABLES.var33)
    
    # add energy to prey
    add_energy_to_prey(prey)
            
    # chance of killing prey if too many - simulate overcrowding

    
    
    # destroy organisms with a too low energy level
    prey, predators, prey_killed, pred_killed = check_organism_has_enough_energy(prey, predators)
    total_prey_killed += prey_killed
    total_predators_killed += pred_killed
    # generation_population_count_prey[current_generation-0.8] = len(prey)
    # generation_population_count_predator[current_generation-0.8] = len(predators)
    
    
    # reproduce
    new_predators = []
    new_prey = []
    for x in predators:
        new_predators += x.reproduce()
    for x in prey:
        new_prey += x.reproduce()
    new_predators_produced = len(new_predators) # for stats
    new_prey_produced = len(new_prey) # for stats
    generation_average_combat_levels["prey, {}".format(current_generation+1)] = mean([x.combat_level for x in new_prey])
    generation_average_combat_levels["predator, {}".format(current_generation+1)] = mean([x.combat_level for x in new_predators])
    
    predators += new_predators
    prey += new_prey
    # generation_population_count_prey[current_generation-0.6] = len(prey)
    # generation_population_count_predator[current_generation-0.6] = len(predators)
    del new_predators
    del new_prey
    
    
    # destroy organisms with a too low energy level
    prey, predators, prey_killed, pred_killed = check_organism_has_enough_energy(prey, predators)
    total_prey_killed += prey_killed
    total_predators_killed += pred_killed
    # generation_population_count_prey[current_generation-0.4] = len(prey)
    # generation_population_count_predator[current_generation-0.4] = len(predators)
    
    
    # hunting
    if len(predators) > len(prey):
        # removes surplus predators from predator list, puts them into
        # their own list
        surplus = len(predators) - len(prey)
        surplus_predators = predators[-surplus:]
        predators = predators[:len(prey)]
    else:
        surplus_predators = None   
    new_prey = []
    new_predators = []
    for i, x in enumerate(predators):
        winner = determine_combat_winner(x, prey[i])
        if winner == "prey": 
            new_prey.append(prey[i])
            if randint(1, 100) <= 50:
                new_predators.append(x)
            else:
                total_predators_killed += 1
        else:
            # simulate transfer of energy
            x.energy_level += prey[i].energy_level*VARIABLES.var30
            total_prey_killed += 1
            new_predators.append(x)
    new_prey += prey[i:]
    prey = [x for x in new_prey]
    predators = [x for x in new_predators]
    del new_prey
    del new_predators
    if surplus_predators is not None:
        # for x in surplus_predators:
        #     if randint(1, 100) <= VARIABLES.var31:
        #         if len(prey) > 0:
        #             prey_choice = choice(prey)
        #         else:
        #             break
        #         winner = determine_combat_winner(x, prey_choice)
        #         if winner == "pred":
        #             x.energy_level += prey_choice.energy_level*VARIABLES.var30
        #             prey.remove(prey_choice)
        #             total_prey_killed += 1
        #             predators.append(x)
        #         elif winner == "prey":
        #             if randint(1, 100) <= 50:
        #                 predators.append(x)
        #             else:
        #                 total_predators_killed += 1
        del surplus_predators
    # generation_population_count_prey[current_generation-0.2] = len(prey)
    # generation_population_count_predator[current_generation-0.2] = len(predators)
 
    
    # spontaneous death
    new_prey = []
    new_predators = []
    for x in prey:
        if randint(1, 100) > x.spontaneous_death_chance:
            new_prey.append(x)
        else:
            total_prey_killed += 1
    for x in predators:
        if randint(1, 100) > x.spontaneous_death_chance:
            new_predators.append(x)
        else:
            total_predators_killed += 1
            
    prey = [x for x in new_prey]
    predators = [x for x in new_predators]
    del new_prey
    del new_predators
    
    # Tracking stats
    overall_total_predators_killed += total_predators_killed
    overall_total_prey_killed += total_prey_killed
    
    # end of cycle print statements
    print("Generation {} complete".format(current_generation))
    # print("Starting Prey in this generation: {}".format(starting_prey))
    # print("Starting Predators in this generation: {}".format(starting_predators))
    # print("New prey produced this generation: {}".format(new_prey_produced))
    # print("New predators produced this generation: {}".format(new_predators_produced))
    # print("Total prey killed this generation: {}".format(total_prey_killed))
    # print("Total predators killed this generation: {}".format(total_predators_killed))
    # print("New Prey count: {}".format(len(prey)))
    # print("New Predator count: {}".format(len(predators)))
    # print("###################################")
    with open("pred.txt", "a") as f:
        f.write("{}\t{}\n".format(current_generation, len(predators)))
    with open("prey.txt", "a") as f:
        f.write("{}\t{}\n".format(current_generation, len(prey)))    
    generation_population_count_prey[current_generation] = len(prey)
    generation_population_count_predator[current_generation] = len(predators)
    
    tobreak = False
    if len(prey) <= 0:
        print("Simulation Over.")
        print("All prey died")
        print("Total predators remanining: {}".format(len(predators)))
        tobreak = True
    
    if len(predators) <= 0:
        print("Simulation Over.")
        print("All predators died")
        print("Total prey remanining: {}".format(len(prey)))
        tobreak = True
    
    if current_generation == VARIABLES.var32 or tobreak:   
        
        remaining_from_each_gen = {}
        for i in range(VARIABLES.var32):
            remaining_from_each_gen["Prey, {}".format(i+1)] = len([x for x in prey if x.gen == i+1])
            remaining_from_each_gen["Predators, {}".format(i+1)] = len([x for x in predators if x.gen == i+1])
           
        print("\nSimulation Over, reached generation max")
        print("Combat levels, generation by generation: ")
        pprint(generation_average_combat_levels)
        print("\n")
        print("Combat levels remaining after this generation")
        print("Prey: {}".format(mean([x.combat_level for x in prey])))
        print("Predators: {}".format(mean([x.combat_level for x in predators])))
        print("\n")
        print("Remaining count from each generation: ")
        pprint(remaining_from_each_gen)
        with open("results.txt", "w") as f:
            f.write("GENOMES OF PREDATORS\n")
            for x in predators:
                f.write(str(x.genome) + str(x.gen) + "\n")
            f.write("\n\n\n\n\n\n\n\n\n\nGENOMES OF PREY\n")
            for x in prey:
                f.write(str(x.genome) + "\n")
        prey_gen, prey_count = zip(*generation_population_count_prey.items())
        predator_gen, predator_count = zip(*generation_population_count_predator.items())
        new_prey_count = []
        new_predator_count = []
        for x in prey_count:
            new_prey_count.append(x/10)
        for x in predator_count:
            new_predator_count.append(x/10)
        prey_count = new_prey_count
        predator_count = new_predator_count
        del new_prey_count
        del new_predator_count
        
        prey_interpolation = interp1d(prey_gen, prey_count, kind="cubic")
        prey_gen = linspace(min(prey_gen), max(prey_gen), 500)
        prey_count = prey_interpolation(prey_gen)
        
        predator_interpolation = interp1d(predator_gen, predator_count, kind="cubic")
        predator_gen = linspace(min(predator_gen), max(predator_gen), 500)
        predator_count = predator_interpolation(predator_gen)
        
        plt.plot(prey_gen, prey_count, color="red", label="Prey")
        plt.plot(predator_gen, predator_count, color="blue", label="Predators")
        plt.xlabel("Generation")
        plt.ylabel("Population count x10")
        plt.legend(loc='upper center')
        plt.show()
        break
    
    current_generation += 1
    
    
    
