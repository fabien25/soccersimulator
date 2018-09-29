from soccersimulator import KeyboardStrategy
from soccersimulator import Strategy
from soccersimulator import SoccerTeam, Simulation
from soccersimulator import SimuGUI,show_state,show_simu
from soccersimulator import Vector2D, SoccerState, SoccerAction, PlayerState, Ball
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from soccersimulator import mdpsoccer
from soccersimulator import show_simu,load_jsonz
from football import *
import numpy as np
import random
import logging
import sys

logger = logging.getLogger("Tireur")

#Distance pour laquel le shoot (p-state.my_position())*0.1 a le plus de chance de rentrer
class ShootSearch(object):
    MAX_STEP = 40
    def __init__(self):
        self.strat = Tireur()
        team1 = SoccerTeam("team1")
        team1.add("Tireur",self.strat)
        team2 = SoccerTeam("team2")
        #team2.add("Nothing",Strategy())
        self.simu = Simulation(team1,team2,max_steps=1000000)
        self.simu.listeners+=self
        self.discr_step = 20 #discr_step  : pas de discretisation du parametre
        self.nb_essais = 10  #nb_essais : nombre d'essais par parametre
    def start(self,visu=True):
        if visu :
            show_simu(self.simu)
        else:
            self.simu.start()
    def begin_match(self,team1,team2,state):
        """ initialise le debut d'une simulation"""
        self.res = dict() #res : dictionnaire des Resultats
        self.last = 0 #last : step du dernier round pour calculer le round de fin avec MAX_STEP
        self.but = 0  #but : nombre de but pour ce parametre
        self.cpt = 0 #cpt : nombre d'essais pour ce parametre
        self.params = [x for x in  np.linspace(10,70,self.discr_step)] #params : liste des parametres a tester
        self.idx=0 #idx : identifiant du parametre courant

    def begin_round(self,team1,team2,state):
        """ engagement : position random du joueur et de la balle """
        #position = Vector2D(np.random.random()*settings.GAME_WIDTH/2.+settings.GAME_WIDTH/2.,np.random.random()*settings.GAME_HEIGHT)
        position = Vector2D(settings.GAME_WIDTH-self.params[self.idx],np.random.random()*settings.GAME_HEIGHT)
        self.simu.state.states[(1,0)].position = position.copy()
        self.simu.state.states[(1,0)].vitesse = Vector2D()
        self.simu.state.ball.position = position.copy()
        #self.strat.norm = self.params[self.idx]
        self.last = self.simu.step
    def update_round(self,team1,team2,state):
        """ si pas maximal atteint, fin du tour"""
        if state.step>self.last+self.MAX_STEP:
            self.simu.end_round()
    def end_round(self,team1,team2,state):
        if state.goal>0:
            self.but+=1
        self.cpt+=1
        if self.cpt>=self.nb_essais:
            self.res[self.params[self.idx]] = self.but*1./self.cpt
            print("nb_but/nb_shoot:",self.res[self.params[self.idx]])
            print("Position du joueur en x:",str(settings.GAME_WIDTH-self.params[self.idx]))
            print("=================")                  
            #logger.debug("parametre %s : %f" %((str(self.params[self.idx]),self.res[self.params[self.idx]])))
            self.idx+=1
            self.but=0
            self.cpt=0
        """ si plus de parametre, fin du match"""
        if self.idx>=len(self.params):
            self.simu.end_match()
#==============================================================================
#Simulation
#Creation d'une equipe
#team1 = SoccerTeam(name="team1",login="etu1")
#team2 = SoccerTeam(name="team2",login="etu2")

#Choix de Strat
##1v1
#team1.add("Fonceur_dribbleur",Fonceur_dribbleur())
#team2.add("Fonceur",Fonceur())
#
#2v2
#team1.add("Gardien",Gardien())
#team1.add("Campeur_proche",Campeur_proche())
#team2.add("Fonceur",Fonceur())
#team2.add("Gardien",Gardien())

#4v4
#team1.add("Gardien",Gardien())
#team1.add("Campeur_proche",Campeur_proche())
#team1.add("Passeur",Passeur())
#team1.add("Campeur_proche_v2",Campeur_proche_v2())
#
#team2.add("Gardien",Gardien())
#team2.add("Campeur_proche",Campeur_proche())
#team2.add("Passeur",Passeur())
#team2.add("Campeur_proche_v2",Campeur_proche_v2())


#Creation d'une partie
#simu = Simulation(team1,team2, max_steps=2000)
#Jouer et afficher la partie
#show_simu(simu) 

#Distance pour laquel le shoot (p-state.my_position())*0.1 a le plus de chance de rentrer
#Shootsearch
tireur = ShootSearch()
tireur.start()
#==============================================================================
### Strategie aleatoire
#class FonceStrategy(Strategy):
#    def __init__(self):
#        super(FonceStrategy,self).__init__("Fonce")
#    def compute_strategy(self,state,id_team,id_player):
#        return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
#                Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
#
#class StaticStrategy(Strategy):
#    def __init__(self):
#        super(StaticStrategy,self).__init__("Static")
#    def compute_strategy(self,state,id_team,id_player):
#        return SoccerAction()
##        
#team1 = SoccerTeam("team1")
#team2 = SoccerTeam("team2")
#
#strat_j1 = KeyboardStrategy()
#strat_j1.add('6',Campeur_proche())
#strat_j1.add('8',Passeur())
#strat_j1.add('a',StaticStrategy())
#strat_j1.add('z',FonceStrategy())
#
#strat_j2 = KeyboardStrategy()
#strat_j2.add('4',Campeur_proche())
#strat_j2.add('9',Passeur())
#strat_j2.add('u',StaticStrategy())
#strat_j2.add('i',FonceStrategy())
#
#team1.add("Jexp 1",strat_j1)
##team1.add("Jexp 2",StaticStrategy())
#
#team2.add("rien 1", strat_j2)
##team2.add("rien 2", StaticStrategy())
#
#simu = Simulation(team1,team2, max_steps=10000)
#show_simu(simu)
