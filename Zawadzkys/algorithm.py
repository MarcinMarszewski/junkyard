from mpi4py import MPI
import numpy as np
import random

from utils import split_list_into_random_chunks


class Algorithm:
    def __init__(self, num_cities=20, pop_size=2, generations=200, mutation_rate=0.2, crossover_rate=0.7, survival_rate=0.1, 
                 start_city=0, ending_cities=[0,1,2], forbidden_routes=[[3,4],[7,10]], number_of_routes=3):
        self.num_cities = num_cities
        self.pop_size = pop_size
        self.generations = generations

        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.survival_rate = survival_rate

        self.start_city = start_city
        self.ending_cities = ending_cities
        self.forbidden_routes = forbidden_routes
        self.number_of_routes = number_of_routes

        self.non_starting_cities = [i for i in range(self.num_cities) if i != self.start_city]

        self.cities = generate_random_cities(self.num_cities)
        self.population = [self.create_specimen() for _ in range(self.pop_size)]

        for specimen in self.population:    #TODO: print [remove]
            print(specimen)

        print("Child:")     #TODO: print [remove]
        print(self.crossover(self.population[0], self.population[1]))  #TODO: print [remove]

    def create_specimen(self):
        specimen = []
        for _ in range(self.number_of_routes):
            route = [self.start_city]
            specimen.append(route)
        
        random.shuffle(self.non_starting_cities)
        routes = split_list_into_random_chunks(self.non_starting_cities, self.number_of_routes)
        for route in routes:
            if route[-1] not in self.ending_cities:
                random_end_city = random.choice(self.ending_cities)
                while random_end_city in route:
                    route.remove(random_end_city)
                route.append(random_end_city)
        for i, route in enumerate(specimen):
            route.extend(routes[i])
        return specimen

    def run(self):
        evals = [[specimen, self.evaluate(specimen)] for specimen in self.population]
        evals.sort(key=lambda x: -x[1])
        new_population = evals[:int(self.pop_size * self.survival_rate)]
        


        # crossover
        # mutate
        # set new population

        ## loop everything
        pass

    def tournament_selection(self, evals, k=2):
        pass

    def mutate(self, specimen):
        if len(specimen) < 2:
            return specimen
        route_a = random.randint(0, len(specimen) - 1)
        route_b = random.randint(0, len(specimen) - 1)
        while route_a == route_b:
            route_b = random.randint(0, len(specimen) - 1)
        if len(specimen[route_a]) < 3 or len(specimen[route_b]) < 2:
            return specimen
        city_a = specimen[route_a][random.randint(1, len(specimen[route_a]) - 2)]
        specimen[route_b].insert(random.randint(1, len(specimen[route_b]) - 2), city_a)
        specimen[route_a].remove(city_a)
        print("Mutated specimen: ", specimen)  #TODO: print [remove]
        

    def crossover(self, parent1, parent2):
        child = []
        for _ in range(self.number_of_routes):
            route = [self.start_city]
            child.append(route)
        
        parent1_cities = [city for route in parent1 for city in route if city != self.start_city]
        parent2_cities = [city for route in parent2 for city in route if city != self.start_city]
        parent1_cities = list(dict.fromkeys(parent1_cities))
        parent2_cities = list(dict.fromkeys(parent2_cities))

        crossover_range = sorted([random.randint(0,self.num_cities-2), random.randint(0,self.num_cities-2)])
        child_cities = parent1_cities[crossover_range[0]:crossover_range[1]+1]
        print("Crossover range:", crossover_range)  #TODO: print [remove]
        print("Parent1 cities:", parent1_cities)  #TODO: print [remove]
        print("Parent2 cities:", parent2_cities)  #TODO: print [remove]
        for city in parent2_cities:
            if city not in child_cities:
                child_cities.append(city)

        print("Child cities:", child_cities)  #TODO: print [remove]
        
        routes = split_list_into_random_chunks(child_cities, self.number_of_routes)
        for route in routes:
            if route[-1] not in self.ending_cities:
                random_end_city = random.choice(self.ending_cities)
                while random_end_city in route:
                    route.remove(random_end_city)
                route.append(random_end_city)
        for i, route in enumerate(child):
            route.extend(routes[i])
        return child

    def evaluate(self, specimen):   #TODO: evaluation for route crossing [implement]
        eval = 0.0
        for route in specimen:
            for i in range(len(route) - 1):
                if [route[i], route[i + 1]] in self.forbidden_routes or [route[i + 1], route[i]] in self.forbidden_routes:
                    eval += float('inf')
                eval += np.linalg.norm(self.cities[route[i]] - self.cities[route[i + 1]])
        return eval



def generate_random_cities(num_cities):
    return np.random.rand(num_cities, 2)


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    algorithm = Algorithm()