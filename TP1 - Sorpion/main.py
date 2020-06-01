
import math
import random
import numpy
import matplotlib.pyplot as plt
import statistics

POPULATION = 500

NB_ESSAIS = 100
VARIATION_GENES = 5/100


class Materiau:
    def __init__(self, nom, masse_volumique, module_young, coef_poisson):
        self.nom = nom
        self.masse_volumique = masse_volumique
        self.module_young = module_young
        self.coef_poisson = coef_poisson


class Scorpion:
    # genes
    def __init__(self, longueur_bras, longueur_corde, module_young, coef_poisson, angle_deg, gravite, masse_volumique, base_fleche, hauteur_fleche, longueur_fleche, base_bras, hauteur_bras):
        self.longueur_bras = longueur_bras
        self.longueur_corde = longueur_corde
        self.module_young = module_young
        self.coef_poisson = coef_poisson
        self.angle_deg = angle_deg
        self.gravite = gravite
        self.masse_volumique = masse_volumique
        self.base_fleche = base_fleche
        self.hauteur_fleche = hauteur_fleche
        self.longueur_fleche = longueur_fleche
        self.base_bras = base_bras
        self.hauteur_bras = hauteur_bras
        self.fitness = self.set_fitness()

    def ressort(self):
        return (1/3) * (self.module_young / (1 - 2 * self.coef_poisson))

    def longueur_vide(self):
        if((self.longueur_bras ** 2 - self.longueur_corde ** 2) < 0):
            return 0
        return 1/2 * math.sqrt(self.longueur_bras ** 2 - self.longueur_corde ** 2)

    def longueur_deplacement(self):
        return self.longueur_fleche - self.longueur_vide()

    def energie_impact(self):
        return 1/2 * self.masse_proj() * self.velocite() ** 2

    def masse_proj(self):
        return self.masse_volumique * self.base_fleche * self.hauteur_fleche * self.longueur_fleche

    def velocite(self):
        if(self.masse_proj() == 0):
            return 0
        return math.sqrt((self.ressort() * self.longueur_deplacement() ** 2) / self.masse_proj())

    def portee(self):
        return ((self.velocite() ** 2) / self.gravite)*math.sin(2 * math.radians(self.angle_deg))

    # Limites

    def moment_quadratique(self):
        return (self.base_bras * self.hauteur_bras ** 3)/12

    def force_traction(self):
        return self.ressort() * self.longueur_deplacement()

    def fleche_fmax(self):
        if((48 * self.module_young * self.moment_quadratique()) == 0):
            return 0
        return (self.force_traction()*self.longueur_bras ** 3) / (48 * self.module_young * self.moment_quadratique())

    def is_tir(self):
        return self.longueur_vide() < self.longueur_fleche and self.longueur_corde < self.longueur_bras and not self.is_rupture()

    def is_rupture(self):
        return self.longueur_deplacement() > self.fleche_fmax()

    def set_fitness(self):
        if(self.is_tir() == True):
            return round(self.energie_impact()*self.portee()*2)
        else:
            return round(self.energie_impact()*self.portee()*2)/4

    def equal(self, scorpion):
        return self.longueur_bras == scorpion.longueur_bras and self.longueur_corde == scorpion.longueur_corde and self.module_young == scorpion.module_young and self.coef_poisson == scorpion.coef_poisson and self.angle_deg == scorpion.angle_deg and self.gravite == scorpion.gravite and self.masse_volumique == scorpion.masse_volumique and self.base_fleche == scorpion.base_fleche and self.hauteur_fleche == scorpion.hauteur_fleche and self.longueur_fleche == scorpion.longueur_fleche and self.base_bras == scorpion.base_bras and self.hauteur_bras == scorpion.hauteur_bras
# individus = energie impact ?


materiaux_possibles = [Materiau('acier', 7850, 210, 0.30), Materiau(
    'aluminium', 2700, 62, 0.33), Materiau('caoutchouc naturel', 990, 2.7, 0.4)]
population = []


def generate_population():
    for i in range(POPULATION):
        Materiau = random.choice(materiaux_possibles)
        population.append(Scorpion(random.randrange(0, 100, 1), random.randrange(0, 100, 1), Materiau.module_young,
                                   Materiau.coef_poisson, random.randrange(0, 90, 1), 9.81, Materiau.masse_volumique, random.randrange(0, 100, 1)/100, random.randrange(0, 100, 1)/100, random.randrange(0, 100, 1), random.randrange(0, 100, 1), random.randrange(0, 100, 1)))


def selection():
    population.sort(key=lambda x: x.fitness, reverse=True)
    return population[: round(POPULATION/2)]
    # for x in range(0, round(POPULATION/2)):
    #    print(population[x].fitness)
    #    print(x)
    #    del population[x]


def croisements():
    probs = [i.fitness for i in population]
    probs /= numpy.sum(probs)
    nouvelle_population = []
    for pop in population:
        scorpion2 = numpy.random.choice(population, p=probs)
        bebe_scorpion2 = croisement(pop, scorpion2)
        nouvelle_population.append(bebe_scorpion2)
        while True:
            # print(probs)
            scorpion3 = numpy.random.choice(population, p=probs)
            if(scorpion3 != scorpion2):
                bebe_scorpion3 = croisement(pop, scorpion3)
                nouvelle_population.append(bebe_scorpion3)
                break

    return nouvelle_population


def croisement(scorpion1, scorpion2):
    return Scorpion(scorpion1.longueur_bras, scorpion1.longueur_corde, scorpion1.module_young, scorpion1.coef_poisson, scorpion1.angle_deg, scorpion1.gravite, scorpion1.masse_volumique, scorpion2.base_fleche, scorpion2.hauteur_fleche, scorpion2.longueur_fleche, scorpion2.base_bras, scorpion2.hauteur_bras)


def mutations():
    for i in range(0, len(population)-1):
        if(random.random() <= 0.5):
            population[i].longueur_corde = population[i].longueur_corde + \
                population[i].longueur_corde*VARIATION_GENES
            population[i].longueur_bras = population[i].longueur_bras + \
                population[i].longueur_bras*VARIATION_GENES
            population[i].angle_deg = population[i].angle_deg + \
                population[i].angle_deg*VARIATION_GENES
            population[i].base_fleche = population[i].base_fleche + \
                population[i].base_fleche*VARIATION_GENES
            population[i].hauteur_fleche = population[i].hauteur_fleche + \
                population[i].hauteur_fleche*VARIATION_GENES
            population[i].longueur_fleche = population[i].longueur_fleche + \
                population[i].longueur_fleche*VARIATION_GENES
        else:
            population[i].longueur_corde = population[i].longueur_corde - \
                population[i].longueur_corde*VARIATION_GENES
            population[i].longueur_bras = population[i].longueur_bras - \
                population[i].longueur_bras*VARIATION_GENES
            population[i].angle_deg = population[i].angle_deg - \
                population[i].angle_deg*VARIATION_GENES
            population[i].base_fleche = population[i].base_fleche - \
                population[i].base_fleche*VARIATION_GENES
            population[i].hauteur_fleche = population[i].hauteur_fleche - \
                population[i].hauteur_fleche*VARIATION_GENES
            population[i].longueur_fleche = population[i].longueur_fleche - \
                population[i].longueur_fleche*VARIATION_GENES


def population_contain(scorpion):
    for pop in population:
        if(pop.equal(scorpion)):
            return True


def afficher_population():
    print('POPULATION :' + str(sum_fitness()) + ' / ' + str(max_fitness()))
    # for pop in population:
    # print(pop.fitness)


def max_fitness():
    fitnesses = [i.fitness for i in population]
    return round(numpy.amax(fitnesses)/1000000)


def min_fitness():
    fitnesses = [i.fitness for i in population]
    return round(numpy.amin(fitnesses)/1000000)


def sum_fitness():
    fitnesses = [i.fitness for i in population]
    return round(sum(fitnesses)/1000000)


def avg_fitness():
    fitnesses = [i.fitness for i in population]
    return round(statistics.mean(fitnesses)/1000000)


def start():
    global population
    xAxis = []
    max_fitnesses = []
    avg_fitnesses = []
    min_fitnesses = []
    print('génération de la population')
    generate_population()
    print('fin de génération de la population')

    for i in range(0, NB_ESSAIS):
        print('selection')
        population = selection()
        print(len(population))
        afficher_population()
        print('croisements')
        population = croisements()
        afficher_population()
        print('mutations')
        mutations()
        afficher_population()
        print(len(population))

        xAxis.append(i)  # Remplissage du graph
        max_fitnesses.append(max_fitness())
        avg_fitnesses.append(avg_fitness())
        min_fitnesses.append(min_fitness())
        # if(i == 9):
        #    for pop in population:
        #        if(pop.fitness != 0):
        #            print(pop.fitness)
    # afficher_population()
    #plt.plot(xAxis, max_fitnesses)
    #plt.plot(xAxis, avg_fitnesses)
    #plt.plot(xAxis, sum_fitnesses)

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Génération')
    #ax1.set_ylabel('exp', color=color)
    ax1.plot(xAxis, max_fitnesses, color='tab:red', label='Fitness maximale')
    ax1.plot(xAxis, avg_fitnesses, color='tab:blue', label='Fitness moyenne')
    ax1.plot(xAxis, min_fitnesses, color='tab:green', label='Fitness minimale')
    ax1.legend()
    plt.show()


start()
