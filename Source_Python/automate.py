# version 2: correction d'un bug dans la fonction minimisation
import copy as cp


class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules et "E" pour epsilon, 
    et "O" pour l'automate vide
    """
    
    def __init__(self, expr="O"):
        """
        construit un automate élémentaire pour une expression régulière expr 
            réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """
        
        # alphabet
        self.alphabet = list("abc")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in (self.alphabet + ["O", "E"]):
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            # langage vide
            self.n = 1
        elif expr == "E":
            self.n = 1
        else:
            self.n = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final = []
        elif expr == "E":
            self.final = [0]
        else:
            self.final = [1]
        # transitions: dico indicé par (état, caractère) qui donne la liste des états d'arrivée
        self.transition =  {} if (expr in ["O", "E"]) else {(0,expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name = "" if expr == "O" else "(" + expr + ")" 
        
    def __str__(self):
        """affichage de l'automate par fonction print"""
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"
        for k,v in self.transition.items():    
            res += str(k) + ": " + str(v) + "\n"
        res += "*********************************"
        return res
    
    def ajoute_transition(self, q0, a, qlist):
        """ ajoute la liste de transitions (q0, a, q1) pour tout q1 
            dans qlist à l'automate
            qlist est une liste d'états
        """
        if not isinstance(qlist, list):
            raise TypeError("Erreur de type: ajoute_transition requiert une liste à ajouter")
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            self.transition.update({(q0, a): qlist})
    
    
def concatenation(a1, a2): 
    """Retourne l'automate qui reconnaît la concaténation des 
    langages reconnus par les automates a1 et a2"""

    a = automate("O")  #initialisation du nouvel automate, O reprèsente le langage vide
    a.name = "(" + a1.name + "." + a2.name + ")"   #le nom du nouvel automate, par exemple si a1 = L1 et L2 = a2 alors a = (L1 . L2)

    d2 = a1.n     #décalage des états de a2, a2 devra commencer à d2 pour éviter les conflits
    a.n = a1.n + a2.n   #nombre d'états du nouvel automate 
    a.final = []    #initialisation des états finaux du nouvel automate

    for (q,c), dests in a1.transition.items() :     #boucle pour parcourir toutes les transitions à partir de l'etat de départ q 
        a.transition[(q,c)] = dests[:]    #copie de la transition dans notre nouvel automate

    for (q,c), dests in a2.transition.items():   #pareil mais pour a2
        a.transition[(q + d2, c)] = [x + d2 for x in dests]   #on recopie les transitions de a2 tout en decakant de d2 pour éviter les conflits
    
    for f in a1.final :
        a.ajoute_transition(f, "E", [d2])   #ajoute d'une transition epsilon de l'etat final f vers l'etat initial de a2 qui est d2
    
    a.final = [f + d2 for f in a2.final]     #ajout des etats finaux du nouvel automate

    return a


def union(a1, a2):
    """Retourne l'automate qui reconnaît l'union des 
    langages reconnus par les automates a1 et a2""" 
    a = automate("O")  #initialisation du nouvel automate
    a.name = "(" + a1.name + "+" + a2.name + ")"   #le nom du nouvel automate, par exemple si a1 = L1 et L2 = a2 alors a = (L1 + L2)

    d1 = 1    #a1 commence à l'état 1
    d2 = 1 + a1.n   #a2 doit commencer après a1

    a.n = a1.n + a2.n + 1  #nombre total d'états = nbr d'etats de a1 + de a2 + un nouvel etats initial qui enverra des transitions E vers mes autres etats initiaux 

    a.final = []   #initialisation etats finaux

    for (q,c), dests in a1.transition.items() :     #boucle pour parcourir toutes les transitions à partir de l'etat de départ q 
        a.transition[(q+d1 ,c)] = [x +d1 for x in dests]    #copie de la transition dans notre nouvel automate

    for (q,c), dests in a2.transition.items():   #pareil mais pour a2
        a.transition[(q + d2, c)] = [x + d2 for x in dests]   #on recopie les transitions de a2 tout en decakant de d2 pour éviter les conflits
    
    a.transition[(0,"E")] = [d1,d2]   #on rajoute les 2 transitions E vers les etats initiaux 

    a.final += [f + d1 for f in a1.final]  #ajout des états finaux (on doit décaler les 2 )
    a.final += [f + d2 for f in a2.final]


    return a


def etoile(a):
    """Retourne l'automate qui reconnaît l'étoile de Kleene du 
    langage reconnu par l'automate a""" 
    a1 = automate("O")
    a1.name = "(" + a.name + ")*"

    d=1
    a1.n = a.n + 1

    a1.final = [0]

    for (q,c), dests in a.transition.items() :
        a1.transition[(q + d,c)] = [x+d for x in dests]
    
    a1.transition[(0,"E")] = [d]

    for f in a.final:
        a1.ajoute_transition(f +d, "E", [d])
        a1.ajoute_transition(f+d, "E", [0])

    return a1


def acces_epsilon(a):
    """ retourne la liste pour chaque état des états accessibles par epsilon
        transitions pour l'automate a
        res[i] est la liste des états accessible pour l'état i
    """
    # on initialise la liste résultat qui contient au moins l'état i pour chaque état i
    res = [[i] for i in range(a.n)]
    for i in range(a.n):
        candidats = list(range(i)) + list(range(i+1, a.n))
        new = [i]
        while True:
            # liste des epsilon voisins des états ajoutés en dernier:
            voisins_epsilon = []
            for e in new:
                if (e, "E") in a.transition.keys():
                    voisins_epsilon += [j for j in a.transition[(e, "E")]]
            # on calcule la liste des nouveaux états:
            new = list(set(voisins_epsilon) & set(candidats))
            # si la nouvelle liste est vide on arrête:
            if new == []:
                break
            # sinon on retire les nouveaux états ajoutés aux états candidats
            candidats = list(set(candidats) - set(new))
            res[i] += new 
    return res


def supression_epsilon_transitions(a):
    """ retourne l'automate équivalent sans epsilon transitions
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    res.n = a.n
    res.final = a.final
    # pour chaque état on calcule les états auxquels il accède
    # par epsilon transitions.
    acces = acces_epsilon(a)
    # on retire toutes les epsilon transitions
    res.transition = {c: j for c, j in a.transition.items() if c[1] != "E"}
    for i in range(a.n):
        # on ajoute i dans les états finals si accès à un état final:
        if (set(acces[i]) & set(a.final)):
            if i not in res.final:
                res.final.append(i)
        # on ajoute les nouvelles transitions en parcourant toutes les transitions
        for c, v in a.transition.items():
            if c[1] != "E" and c[0] in acces[i]:
                res.ajoute_transition(i, c[1], v)
    return res
        
        
def determinisation(a):
    """ retourne l'automate équivalent déterministe
        la construction garantit que tous les états sont accessibles
        automate d'entrée sans epsilon-transitions
    """
    a = cp.deepcopy(a) #on copie l'automate pour ne pas perdre l'original

    automate_det = automate("O")

    automate_det.name = a.name   #on garde le meme nom
    automate_det.alphabet = a.alphabet

    etats_det = [[0]]   #liste des états déterministes

    automate_det.transition = {}
    automate_det.final = []

    i = 0

    while i < len(etats_det) :    #parcourt tant qu'il existe un etat deterministe non traité
        etats_cour = etats_det[i]  #liste des états non déterministe
        for lettre in a.alphabet :  #on va parcourir les transitions pour chaque symbole de l'alphabet
            etats_arrivee = []
            for etat in etats_cour :    #on parcourt chaque etat de l'AFN present dans l'etat courant
                if (etat, lettre) in a.transition :   #on verifie si il existe une transition depuis cet etat avec cette lettre
                    for etat_suivant in a.transition[(etat, lettre)] :      #on parcourt tout les etats atteignables depuis cet etat
                        if etat_suivant not in etats_arrivee :     #on évite les doublons
                            etats_arrivee.append(etat_suivant) 
            if etats_arrivee != []:    #verifie si il existe au moins une transition
                if etats_arrivee not in etats_det : #on ajoute l'etat deterministe s'il y est pas
                    etats_det.append(etats_arrivee)

                i_arrivee = etats_det.index(etats_arrivee)

                automate_det.transition[(i, lettre)] = [i_arrivee]
        
        i += 1 
    automate_det.n =len(etats_det)

    for j, ensemble in enumerate(etats_det) :     #nouveaux etats finaux
        if set(ensemble) & set(a.final):
            automate_det.final.append(j)

    return automate_det
    
    
def completion(a):
    """ retourne l'automate a complété
        l'automate en entrée doit être déterministe
    """
    a = cp.deepcopy(a)  #on copie l'automate pour ne pas perdre l'original

    puits = False  #on initialise une variable puits à false car on est pas sur d'avoir besoin d'un puit
    i_puits = a.n  #indice du futur puit si besoin

    for etat in range(a.n) :  #on parcourt tout les états de a 
        for lettre in a.alphabet : 
            if(etat, lettre) not in a.transition :  #boucle qui cherche les cas ou la transition n'existe pas
                puits = True #on a donc besoin d'un puit
                a.transition[(etat, lettre)] = [i_puits]  #on ajoute la transition inexistante

    if puits : #si y a besoin d'un puit alors 
        for lettre in a.alphabet : 
            a.transition[(i_puits, lettre)] = [i_puits]

        a.n += 1   #on ajoute l'etat puit


    return a


###################################################
# version corrigée de la fonction de minimisation #
###################################################

def minimisation(a):
    """ retourne l'automate minimum
        a doit être déterministe complet
        algo par raffinement de partition (algo de Moore)
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    
    # Étape 1 : partition initiale = finaux / non finaux
    part = [set(a.final), set(range(a.n)) - set(a.final)]
    # on retire les ensembles vides
    part = [e for e in part if e != set()]  
    
    # Étape 2 : raffinement jusqu’à stabilité
    modif = True
    while modif:
        modif = False
        new_part = []
        for e in part:
            # sous-ensembles à essayer de séparer
            classes = {}
            for q in e:
                # signature = tuple des indices des blocs atteints pour chaque lettre
                signature = []
                for c in a.alphabet:
                    for i, e2 in enumerate(part):
                        if a.transition[(q, c)][0] in e2:
                            signature.append(i)
                # on ajoute l'état q à la clef signature calculée
                classes.setdefault(tuple(signature), set()).add(q)
            if len(classes) > 1:
                # s'il y a >2 signatures différentes on a séparé des états dans e
                modif = True
                new_part.extend(classes.values())
            else:
                new_part.append(e)
        part = new_part
    # on réordonne la partition pour que le premier sous-ensemble soit celui qui contient l'état initial
    for i, e in enumerate(part):
        if 0 in e:
            part[0], part[i] = part[i], part[0]
            break
 
     
    # Étape 3 : on construit le nouvel automate minimal
    mapping = {}
    # on associe à chaque état q le nouvel état i
    # obtenu comme étant l'indice du sous-ensemble de part
    for i, e in enumerate(part):
        for q in e:
            mapping[q] = i

    res.n = len(part)
    res.final = list({mapping[q] for q in a.final if q in mapping})
    for i, e in enumerate(part):
        # on récupère un élément de e:
        representant = next(iter(e))
        for c in a.alphabet:
            q = a.transition[(representant, c)][0]
            res.transition[(i, c)] = [mapping[q]]
    return res
    

def tout_faire(a):
    a1 = supression_epsilon_transitions(a)
    a2 = determinisation(a1)
    a3 = completion(a2)
    a4 = minimisation(a3)
    return a4


def egal(a1, a2):
    """ retourne True si a1 et a2 sont isomorphes
        a1 et a2 doivent être minimaux
    """
    if a1.n != a2.n :  #si ce n'est pas le meme nombre d'etat alors pas le meme automate 
        return False

    if set(a1.final) != set(a2.final) :   #verifie si l'on a les memes etats finaux
        return False
    
    for etat in range(a1.n) :
        for lettre in a1.alphabet : 
            if(etat,lettre) not in a1.transition or (etat,lettre) not in a2.transition:
                return False
            if a1.transition[(etat, lettre)] != a2.transition[(etat, lettre)]:
                return False


    return True


# TESTS UNITAIRES
if __name__ == "__main__":
    print(" AUTOMATE MINIMAL POUR (E.a)")
    
    # Creation de l'automate de Thompson
    exp = concatenation(automate("E"), automate("a"))
    
    # Transformation via les  fonctions
    minimal = tout_faire(exp)
    
    print(minimal)





a = automate("a")
b = automate("b")
c = completion(a)

assert c.n == a.n or c.n == a.n + 1














