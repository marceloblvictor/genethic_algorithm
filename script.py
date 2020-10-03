import random, math


class GeneticAlgorithm:

    cities_coords = []

    def __init__(self, cities_coords, crossover_rate, mutation_rate, population_size):
        self.cities_coords = cities_coords
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.population = []
        self.generation_stats = {
        "best_individual" : {"index": 0, "value": 1000000000},
        "population_avg": 0,
        }

    # Os genes consistem no índice que a cidade ocupa na lista cities_coords
    def create_initial_individual(self):

        genes = []
        numbers = [x for x in range(0, 100)]
        
        while len(numbers) > 0:
            gene = random.choice(numbers)
            numbers.remove(gene)
            genes.append(gene)
            
        return genes

    # método estático que calcula a distância euclidiana entre dois pontos em um plano
    @staticmethod
    def calculate_distance_between_cities(x1, y1, x2, y2):
        
        return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 2)

    # função de evaluação que retorna a aptidão de um dado indivíduo (cromossomo)
    def calculate_tour_total_distance(self, tour):
        
        total_distance = 0
    

        for i, city in enumerate(tour):
            if i == len(tour) - 1:
                return total_distance
            else:
                x1 = self.cities_coords[city][0]
                y1 = self.cities_coords[city][1]
                x2 = self.cities_coords[tour[i+1]][0]
                y2 = self.cities_coords[tour[i+1]][1]
                total_distance += GeneticAlgorithm.calculate_distance_between_cities(x1, y1, x2, y2)

    # exibe estatísticas de uma geração de cromossomos
    def analyze_and_display_generation_data(self):

        print("\n")

        generation_total_distance = 0
        
        for i, tour in enumerate(self.population):
            
            tour_total_distance = round(self.calculate_tour_total_distance(tour), 2)

            if tour_total_distance < self.generation_stats["best_individual"]["value"]:
                self.generation_stats["best_individual"]["index"] = i
                self.generation_stats["best_individual"]["value"] = tour_total_distance
            
            generation_total_distance += tour_total_distance

        print("\nMédia de distância percorrida nessa geração: ")
        self.generation_stats["population_avg"] = round(generation_total_distance / len(self.population), 2)
        print(self.generation_stats["population_avg"])
        print(f"\nMelhor indivíduo dessa geração percorre uma distância de: {str(self.generation_stats['best_individual']['value'])}")
        print(self.population[self.generation_stats['best_individual']['index']])

    # cria indivíduos iniciais para dar o ponta-pé à evolução genética
    def create_initial_population(self):

        for _ in range(self.population_size):
            new_individual = self.create_initial_individual()
            self.population.append(new_individual)

    # seleciona o casal de indivíduos que dará origem ao novo indivíduo por meio do método do torneio
    def select_couple_by_tournament(self):
        
        population_indexes = [i for i in range(self.population_size)]
        random.shuffle(population_indexes)
        halfpoint = round(self.population_size/2)
        group1 = population_indexes[:halfpoint]
        group2 = population_indexes[halfpoint:]
        
        champion1 = {"index": 500, "value": 100000000}
        champion2 = {"index": 500, "value": 100000000}
        
        for index in group1:
            value = self.calculate_tour_total_distance(self.population[index])
            if value < champion1["value"]:
                champion1["index"] = index
                champion1["value"] = value

        for index in group2:
            
            value = self.calculate_tour_total_distance(self.population[index])
            if value < champion2["value"]:
                if index == self.generation_stats["best_individual"]["index"]: 
                    random_number = random.randint(0, 100)
                    
                    if random_number < 90:
                        champion2["index"] = index
                        champion2["value"] = value
                    else:
                        copy_group2 = group2[:]
                        copy_group2.remove(index)
                        random_index = random.choice(copy_group2)
                        champion2["index"] = random_index
                        champion2["value"] = self.calculate_tour_total_distance(self.population[random_index])

                else:
                    champion2["index"] = index
                    champion2["value"] = value

        

        return (self.population[champion1["index"]], self.population[champion2["index"]])
          
    # gera o casal invocando o método da seleção por torneio, aplica o crossover e a mutação
    def reproduce(self):
        
        parent1, parent2 = self.select_couple_by_tournament()
        descendant1, descendant2 = self.mutate(self.crossover((parent1, parent2)))
    
        return descendant1, descendant2
    
    # realiza o crossover utilizando o método do OX
    def crossover(self, chromossomes):

        random_number = random.randint(0, 100) / 100
        crossover_happens = random_number <= self.crossover_rate   # se o crossover não ocorrer, retorna os dois cromossomos pais
        if not crossover_happens:
            return chromossomes

        chromossome1, chromossome2 = chromossomes
        
        new_chromossome_1 = ["x" for _ in range(len(chromossome1))]
        new_chromossome_2 = ["y" for _ in range(len(chromossome2))]


        cut_point1 = random.randint(1, len(chromossome1) - 2)  # exclui a primeira e a última cidade do ponto de corte
        cut_point2 = random.randint(1, len(chromossome2) - 2) 
        while cut_point2 == cut_point1:
            cut_point2 = random.randint(1, self.population_size - 2)
        
        if cut_point2 < cut_point1:
            cut_point1, cut_point2 = cut_point2, cut_point1

        
        new_chromossome_1[cut_point1:cut_point2 + 1] = chromossome1[cut_point1:cut_point2 + 1]
        new_chromossome_2[cut_point1:cut_point2 + 1] = chromossome2[cut_point1:cut_point2 + 1]
        
        copy_chromossome1 = chromossome1[cut_point2 + 1:] + chromossome1[:cut_point1] + chromossome1[cut_point1:cut_point2 + 1]
        copy_chromossome2 = chromossome2[cut_point2 + 1:] + chromossome2[:cut_point1] + chromossome2[cut_point1:cut_point2 + 1]


        index_new = cut_point2 + 1
        index_copy = 0

        while index_new < len(new_chromossome_1):
            if copy_chromossome2[index_copy] not in new_chromossome_1:
                new_chromossome_1[index_new] = copy_chromossome2[index_copy]
                index_copy += 1
                index_new += 1
            else:
                index_copy += 1

        index_new = 0
        while index_new < cut_point1:
            if copy_chromossome2[index_copy] not in new_chromossome_1:
                new_chromossome_1[index_new] = copy_chromossome2[index_copy]
                index_copy += 1
                index_new += 1
            else:
                index_copy += 1

        index_new = cut_point2 + 1
        index_copy = 0

        while index_new < len(new_chromossome_2):
            if copy_chromossome1[index_copy] not in new_chromossome_2:
                new_chromossome_2[index_new] = copy_chromossome1[index_copy]
                index_copy += 1
                index_new += 1
            else:
                index_copy += 1

        index_new = 0
        while index_new < cut_point1:
            if copy_chromossome1[index_copy] not in new_chromossome_2:
                new_chromossome_2[index_new] = copy_chromossome1[index_copy]
                index_copy += 1
                index_new += 1
            else:
                index_copy += 1

       
        return new_chromossome_1, new_chromossome_2

    # realiza mutação utilizando o método da inversion
    def mutate(self, chromossomes):
        
        chromossome1, chromossome2 = chromossomes

        cut_point1 = random.randint(1, len(chromossome1) - 2)  # exclui a primeira e a última cidade do ponto de corte
        cut_point2 = random.randint(1, len(chromossome2) - 2) 
        while cut_point2 == cut_point1:
            cut_point2 = random.randint(1, self.population_size - 2)
        
        if cut_point2 < cut_point1:
            cut_point1, cut_point2 = cut_point2, cut_point1

        
        slice1 = chromossome1[cut_point1:cut_point2 + 1]
        slice1.reverse()
        mutated_chromossome1 = chromossome1[:cut_point1] + slice1 + chromossome1[cut_point2 + 1:]

        slice2 = chromossome2[cut_point1:cut_point2 + 1]
        slice2.reverse()
        mutated_chromossome2 = chromossome2[:cut_point1] + slice2 + chromossome2[cut_point2 + 1:]
        
        mutated_chromossomes = [mutated_chromossome1, mutated_chromossome2]
       
        # Caso o número aleatório gerado não seja menor que a taxa de mutação, o cromossomo original não mutado será retornado pelo método
        random_number = random.randint(0, 100) / 100
        mutation_happens = random_number <= self.mutation_rate   
        if not mutation_happens:
            mutated_chromossomes[0] = chromossome1

        random_number = random.randint(0, 100) / 100
        mutation_happens = random_number <= self.mutation_rate   
        if not mutation_happens:
            mutated_chromossomes[1] = chromossome2

        return mutated_chromossomes

    # Os dois indivíduos menos aptos são substituídos pelos dois novos cromossomos
    def generation_transition(self, new_chromossomes):

        arr = [(i, self.calculate_tour_total_distance(ind)) for i, ind in enumerate(self.population)]

        two_worst_indexes = [0, 0]

        worst_ind = {"index": 500, "value": 0}

        for ind in arr:
            if ind[1] > worst_ind["value"]:
                worst_ind["index"] = ind[0]
                worst_ind["value"] = ind[1]

        two_worst_indexes[0] = worst_ind["index"]
        arr.pop(worst_ind["index"])

        worst_ind = {"index": 500, "value": 0}

        for ind in arr:
            if ind[1] > worst_ind["value"]:
                worst_ind["index"] = ind[0]
                worst_ind["value"] = ind[1]

        two_worst_indexes[1] = worst_ind["index"]

        new_chromossome1, new_chromossome2 = new_chromossomes

        self.population[two_worst_indexes[0]] = new_chromossome1
        self.population[two_worst_indexes[1]] = new_chromossome2

    def execute(self):

        self.generation_transition(self.reproduce())
    
        

if __name__ == "__main__":

    datContentX = [i.strip() for i in open("coordenadasx.dat").readlines()]
    datContentY = [j.strip() for j in open("coordenadasy.dat").readlines()]
    datContent = tuple(zip(datContentX, datContentY))

    cities_coords = []

    for i in range(len(datContent)):
        
        cities_coords.append((int(datContent[i][0]), int(datContent[i][1])))


    my_gen_algo = GeneticAlgorithm(cities_coords, 0.75, 0.3, 6)
    my_gen_algo.create_initial_population()
    print('Dados da Geração Inicial:')
    my_gen_algo.analyze_and_display_generation_data()
    
    
    # critério de parada: se houver 10 pioras consecutivas na média populacional
    
    current_population_avg = 99999999

    count = 0
    round_number = 2

    while count < 10:

        print("\nDados da Geração " + str(round_number) + ":")

        my_gen_algo.execute()
        my_gen_algo.analyze_and_display_generation_data()

        if my_gen_algo.generation_stats["population_avg"] >= current_population_avg:
            count += 1   
        else:
            count = 0

        current_population_avg = my_gen_algo.generation_stats["population_avg"]
        round_number += 1



     
   
    

    


    
    
    

    
        

    

        
    

   

    

   