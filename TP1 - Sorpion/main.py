
import math
import random

POPULATION = 10

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
        self.note = 0

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
        return self.longueur_vide() < self.longueur_fleche and self.longueur_corde < self.longueur_bras

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


def set_notes():
    for pop in population:
        if(pop.is_tir() == True):
            if(pop.is_rupture() == True):
                pop.note = pop.energie_impact()*pop.portee()*2
            else:
                pop.note = pop.energie_impact()*pop.portee()
        else:
            pop.note = 1


def selection():
    population.sort(key=lambda x: x.note, reverse=True)
    for x in range(round(POPULATION/2), POPULATION):
        population[x] = 0


def croisements():
    for x in range(0, round(POPULATION/2)):
        population[x] = 0


def croisement(scorpion1: Scorpion, scorpion2: Scorpion):


def start():
    generate_population()
    set_notes()
    selection()


start()
