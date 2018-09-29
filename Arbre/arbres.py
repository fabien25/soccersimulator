from soccersimulator import settings,SoccerTeam, Simulation, show_simu, KeyboardStrategy
from soccersimulator import Strategy, SoccerAction, Vector2D, load_jsonz,dump_jsonz,Vector2D
import logging
from arbres_utils import build_apprentissage,affiche_arbre,DTreeStrategy,apprend_arbre,genere_dot
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier
import os.path
from football import *

#######
## Constructioon des equipes
#######

team1 = SoccerTeam("team1")
strat_j1 = KeyboardStrategy()
strat_j1.add('a',mon_dribbleur())
strat_j1.add('z',mon_fonceur())
team1.add("Jexp 1",strat_j1)
team1.add("Jexp 2",StaticStrategy())

team2 = SoccerTeam("team2")
team2.add("rien 1", StaticStrategy())
team2.add("rien 2", StaticStrategy())


### Transformation d'un etat en features : state,idt,idp -> R^d
def my_get_features(state,idt,idp):
    """ extraction du vecteur de features d'un etat, ici distance a la balle, distance au but, distance balle but """
    p_pos= state.player_state(idt,idp).position
    #f1 = p_pos.distance(state.ball.position) #distance a la balle
    #f2= p_pos.distance( Vector2D((2-idt)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)) #distance au but
    f3 = state.ball.position.distance(Vector2D((2-idt)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)) #distance balle-but
    #return [f1,f2,f3]
    return [f3]


def entrainement(fn):
    simu = Simulation(team1,team2)
    show_simu(simu)
    # recuperation de tous les etats
    training_states = strat_j1.states
    # sauvegarde dans un fichier
    dump_jsonz(training_states,fn)

def apprentissage(fn):
    ### chargement d'un fichier sauvegarder
    states_tuple = load_jsonz(fn)
    ## Apprentissage de l'arbre
    data_train, data_labels = build_apprentissage(states_tuple,my_get_features)
    dt = apprend_arbre(data_train,data_labels,depth=10)
    # Visualisation de l'arbre
    affiche_arbre(dt)
    genere_dot(dt,"test_arbre.dot")
    return dt

def jouer_arbre(dt):
    ####
    # Utilisation de l'arbre
    ###
    #dic = {"mon_dribbleur":mon_dribbleur(),"mon_fonceur":mon_fonceur()}
    dic = {"mon_fonceur":mon_fonceur(),"mon_dribbleur":mon_dribbleur()}
    treeStrat1 = DTreeStrategy(dt,dic,my_get_features)
    #treeStrat2 = DTreeStrategy(dt,dic,my_get_features)
    team3 = SoccerTeam("Arbre Team")
    team3.add("Joueur 1",treeStrat1)
    #team3.add("Joueur 2",treeStrat2)
    simu = Simulation(team2,team3)
    show_simu(simu)

if __name__=="__main__":
    fn = "test_states.jz"
    if not os.path.isfile(fn):
        entrainement(fn)
    dt = apprentissage(fn)
    jouer_arbre(dt)
