
import math
import random
import numpy

POPULATION = 100

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
        self.fitness = 0

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
# individus = energie impact ?


materiaux_possibles = [Materiau('acier', 7850, 210, 0.30), Materiau(
    'aluminium', 2700, 62, 0.33), Materiau('caoutchouc naturel', 990, 2.7, 0.4)]
population = []


def generate_population():
    for i in range(POPULATION):
        Materiau = random.choice(materiaux_possibles)
        population.append(Scorpion(random.randrange(0, 100, 1), random.randrange(0, 100, 1), Materiau.module_young,
                                   Materiau.coef_poisson, random.randrange(0, 90, 1), 9.81, Materiau.masse_volumique, random.randrange(0, 100, 1)/100, random.randrange(0, 100, 1)/100, random.randrange(0, 100, 1), random.randrange(0, 100, 1), random.randrange(0, 100, 1)))


def set_fitnesses():
    for pop in population:
        if(pop.is_tir() == True):
            pop.fitness = pop.energie_impact()*pop.portee()*2
        else:
            pop.fitness = 0


def selection():
    population.sort(key=lambda x: x.fitness, reverse=True)
    for x in range(round(POPULATION/2), POPULATION-1):
        del population[round(POPULATION/2)]


def croisements():
    probs = [i.fitness for i in population]
    probs /= numpy.sum(probs)
    nouvelle_population = []
    for pop in population:
        scorpion2 = numpy.random.choice(population, p=probs)
        bebe_scorpion = croisement(pop, scorpion2)
        nouvelle_population.append(bebe_scorpion)
        while True:
            scorpion3 = numpy.random.choice(population, p=probs)
            if(scorpion3.fitness != scorpion2.fitness):
                bebe_scorpion2 = croisement(pop, scorpion3)
                if(bebe_scorpion2 not in nouvelle_population):
                    nouvelle_population.append(bebe_scorpion2)
                    break

    return nouvelle_population


def croisement(scorpion1, scorpion2):
    return Scorpion(scorpion1.longueur_bras, scorpion1.longueur_corde, scorpion1.module_young, scorpion1.coef_poisson, scorpion1.angle_deg, scorpion1.gravite, scorpion1.masse_volumique, scorpion2.base_fleche, scorpion2.hauteur_fleche, scorpion2.longueur_fleche, scorpion2.base_bras, scorpion2.hauteur_bras)


def mutations():
    for i in range(0, len(population)-1):
        if(decision(0.5)):
            population[i].longueur_corde += 1


def afficher_population():
    print('POPULATION :' + str(avg_fitness()) + ' / ' + str(max_fitness()))
    # for pop in population:
    # print(pop.fitness)


def decision(probability):
    return random.random() < probability


def max_fitness():
    fitnesses = [i.fitness for i in population]
    return numpy.amax(fitnesses)


def avg_fitness():
    fitnesses = [i.fitness for i in population]
    return numpy.mean(fitnesses)


def start():
    global population
    generate_population()
    for i in range(0, 10):
        set_fitnesses()
        selection()
        population = croisements()
        set_fitnesses()
        mutations()
        afficher_population()
    # afficher_population()


start()
