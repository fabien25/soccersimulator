from soccersimulator.strategies  import Strategy
from soccersimulator.mdpsoccer import SoccerTeam, Simulation
from soccersimulator.gui import SimuGUI,show_state,show_simu
from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
import math
#==============================================================================
class MyState(object):
    def __init__(self,state,idteam,idplayer):
        self.state = state
        self.key = (idteam,idplayer)
        self.idteam = idteam
        self.idplayer = idplayer
        self.but_adv= (Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2),Vector2D(0,settings.GAME_HEIGHT/2))
        
    def my_position(self):
        return self.state.player_state(self.key[0],self.key[1]).position
    
    def ball_position(self):
        return self.state.ball.position
    
    def ball_vitesse(self):
        return self.state.ball.vitesse
    
    def step(self):
        return self.state.step      
        
    def je_suis_dans_mon_camp(self):
        if (self.key[0]==1) and (self.my_position().x<=settings.GAME_WIDTH/2):
            return True
        else:
            return False
        if (self.key[0]==2) and (self.my_position().x>=settings.GAME_WIDTH/2):
            return True
        else:
            return False        
    #1v1
    def ennemy_position(self):
        if (self.key[0]==1):
                return self.state.player_state(2,0).position
        if (self.key[0]==2):
                return self.state.player_state(1,0).position
    #1v1
    def ennemy_vitesse(self):
        if (self.key[0]==1):
                return self.state.player_state(2,0).vitesse
        if (self.key[0]==2):
                return self.state.player_state(1,0).vitesse    
    #2v2
    def ally_position(self):
        if (self.key[0]==1):
            if (self.key[1]==0):
                return self.state.player_state(1,1).position
            if (self.key[1]==1):
                return self.state.player_state(1,0).position
            if (self.key[1]==2):
                return self.state.player_state(1,3).position
            if (self.key[1]==3):
                return self.state.player_state(1,2).position  
        if (self.key[0]==2):                
            if (self.key[1]==0):
                return self.state.player_state(2,1).position
            if (self.key[1]==1):
                return self.state.player_state(2,0).position
            if (self.key[1]==2):
                return self.state.player_state(2,3).position
            if (self.key[1]==3):
                return self.state.player_state(2,2).position
    #2v2
    def ally_vitesse(self):
        if (self.key[0]==1):
            if (self.key[1]==0):
                return self.state.player_state(1,1).vitesse
            if (self.key[1]==1):
                return self.state.player_state(1,0).vitesse
            if (self.key[1]==2):
                return self.state.player_state(1,3).vitesse
            if (self.key[1]==3):
                return self.state.player_state(1,2).vitesse 
        if (self.key[0]==2):
            if (self.key[1]==0):
                return self.state.player_state(2,1).vitesse
            if (self.key[1]==1):
                return self.state.player_state(2,0).vitesse
            if (self.key[1]==2):
                return self.state.player_state(2,3).vitesse
            if (self.key[1]==3):
                return self.state.player_state(2,2).vitesse
                
    def get_position_coequipier(self):
        return sorted([ (self.state.player_state(idt,idp).position.distance(self.my_position()),self.state.player_state(idt,idp).position) for idt,idp in self.state.players if idt == self.idteam and idp != self.idplayer])
    
    def get_ennemi(self):
        return sorted([ (self.states[(idt,idp)].position.distance(self.my_position()),self.states[(idt,idp)].position) for idt,idp in self.states.keys() if idt != self.idteam])
    
    def get_vitesse_coequipier(self):
        return sorted([ (self.state.player_state(idt,idp).position.distance(self.my_position()),self.state.player_state(idt,idp).vitesse) for idt,idp in self.state.players if idt == self.idteam and idp != self.idplayer])
    
    def pos_joueur_plus_proche(self):
        L= self.get_position_coequipier()
        Z= self.get_vitesse_coequipier()
        return L[0][1] + Z[0][1]
#==============================================================================
class Comportement:
    def __init__(self,strategie_attack= None,strategie_defense= None, strategie_selection= None):   
        self.strategie_attack = strategie_attack     #Vecteur2D
        self.strategie_defense = strategie_defense   #Vecteur2D
        self.strategie_selection = strategie_selection   #booleen
           
def Joueur(state,comportement):
    if (comportement.strategie_selection(state) == 0):
        return comportement.strategie_attack(state)
    else:
        return comportement.strategie_defense(state)
#==============================================================================
#Strategies
#Basique
def Attaque_fonceur_base(state):
    return aller_courrir_base(state,state.ball_position()+state.ball_vitesse()*5)+shoot(state, state.but_adv[state.key[0]-1])     
     
def Attaque_passeur(state):
    return aller_courrir(state,state.ball_position()+state.ball_vitesse()*5)+shoot(state, state.pos_joueur_plus_proche()) #state.ally_position()+state.ally_vitesse())
    
def Attaque_tireur(state):
    return shoot_tireur(state, state.but_adv[state.key[0]-1])  
 
#Avancee
def Attaque_fonceur_1v1(state):
    if (peut_shooter(state)):
        if state.je_suis_dans_mon_camp():
            if (distance(state.ennemy_position(),state.my_position())<5):
                return aller_courrir_marcher(state,state.ball_position()+state.ball_vitesse()*5)+shoot_but(state, state.but_adv[state.key[0]-1])
            else:
                return aller_courrir_marcher(state,state.ball_position()+state.ball_vitesse()*5)
        else:
            return aller_courrir_marcher(state,state.ball_position()+state.ball_vitesse()*5)+shoot_but(state, state.but_adv[state.key[0]-1])
    else:
        return aller_courrir_marcher(state,state.ball_position()+state.ball_vitesse()*5)
        
        
def Attaque_dribbleur_base(state):
    if (peut_shooter(state)):
        return aller_courrir_marcher_v2(state,state.ball_position()+state.ball_vitesse()*8)+mini_shoot(state, state.but_adv[state.key[0]-1])
    else:
        return aller_courrir_marcher_v2(state,state.ball_position())

def Attaque_dribbleur_1v1(state):
    if (state.step()>2700) and (state.ball_position().x==settings.GAME_WIDTH/2) and (state.ball_position().y==settings.GAME_HEIGHT/2):
        if (peut_shooter(state)):
            return aller_courrir_marcher_v2(state,state.ball_position()+state.ball_vitesse()*8)+mini_shoot(state, state.but_adv[state.key[0]-1]+20)
        else:
            return aller_courrir_marcher_v2(state,state.ball_position()+state.ball_vitesse()*8)
    if (peut_shooter(state)):
        if state.je_suis_dans_mon_camp():
            if (distance(state.ennemy_position(),state.my_position())<5):
                return aller_courrir_marcher(state,state.ball_position()+state.ball_vitesse()*8)+mini_shoot(state, state.but_adv[state.key[0]-1]+20)
            else:
                return aller_courrir_marcher(state,state.ball_position()+state.ball_vitesse()*8)
        else:
            return aller_courrir_marcher(state,state.ball_position()+state.ball_vitesse()*8)+mini_shoot(state, state.but_adv[state.key[0]-1])        
    else:
        return aller_courrir_marcher(state,state.ball_position()+state.ball_vitesse()*8)
        
def Attaque_campeur_static(state):
    if (peut_shooter(state)):
        return aller_camper_static(state,state.ball_position()+state.ball_vitesse()*5)+shoot_but(state, state.but_adv[state.key[0]-1])
    else:
        return aller_camper_static(state,state.ball_position()+state.ball_vitesse()*5)        

def Attaque_campeur_proche(state):
    if (peut_shooter(state)):
        return aller_camper_proche(state,state.ball_position()+state.ball_vitesse()*5)+shoot_but(state, state.but_adv[state.key[0]-1])
    else:
        return aller_camper_proche(state,state.ball_position()+state.ball_vitesse()*5)
        
def Attaque_campeur_proche_v2(state):
    if (peut_shooter(state)):
        return aller_camper_proche_v2(state,state.ball_position()+state.ball_vitesse()*5)+shoot_but(state, state.but_adv[state.key[0]-1])
    else:
        return aller_camper_proche_v2(state,state.ball_position()+state.ball_vitesse()*5)
    
def Attaque_fonceur_2v2(state):
    if (peut_shooter(state)):
        return aller_courrir_marcher_v2(state,state.ball_position()+state.ball_vitesse()*5)+shoot_but(state, state.but_adv[state.key[0]-1])
    else:
        return aller_courrir_marcher_v2(state,state.ball_position()+state.ball_vitesse()*5)  

def Attaque_dribbleur(state):
    if (peut_shooter(state)):
        return aller_courrir_marcher_v2(state,state.ball_position()+state.ball_vitesse()*5)+shoot(state, state.but_adv[state.key[0]-1])
    else:
        return aller_courrir_marcher_v2(state,state.ball_position()+state.ball_vitesse()*5)
        
def Defense_gardien_static(state): 
    if (peut_shooter(state)):
        return aller_gardien_static(state,state.ball_position()+state.ball_vitesse()*5)+shoot(state, state.ally_position()+state.ally_vitesse())
    else:
        return aller_gardien_static(state,state.ball_position()+state.ball_vitesse()*5)
        
def Defense_gardien(state): 
    if (peut_shooter(state)):
        return aller_gardien(state,state.ball_position()+state.ball_vitesse()*5)+shoot(state, state.ally_position()+state.ally_vitesse())    
    else:
        if state.je_suis_dans_mon_camp():
            if (distance(state.ball_position(),state.my_position())<10):
                return aller_courrir_marcher_v2(state,state.ball_position())
            else:
                return aller_gardien(state,state.ball_position()+state.ball_vitesse()*5)   
        else:
            return aller_gardien(state,state.ball_position()+state.ball_vitesse()*5)+shoot(state, state.ally_position()+state.ally_vitesse())
            
def Defense_gardien_contre(state):
    if (distance(state.ball_position(),state.my_position())<20):
        if (peut_shooter(state)):
                return aller_courrir_marcher_v2(state,Vector2D(settings.GAME_WIDTH/2,state.ball_position().y+state.ball_vitesse().y))+shoot(state, state.ally_position()+state.ally_vitesse()) 
        else:
                return aller_courrir_marcher_v2(state,state.ball_position()+state.ball_vitesse())
    else:
        return aller_courrir_marcher_v2(state,Vector2D(settings.GAME_WIDTH/2,state.ball_position().y+state.ball_vitesse().y))
#==============================================================================
#Selection_strat
#Balle dans camps adv ou alliee
def Selection_1(state):
    if (state.key[0]==1):
        if (state.ball_position().x>settings.GAME_WIDTH/2):
            return 0                                                           #Attaque
        else:
            return 1                                                           #Defense
    if (state.key[0]==2):
        if (state.ball_position().x<settings.GAME_WIDTH/2):
            return 0
        else:
            return 1
            
#Balle entre 1/4 et 3/4   
def Selection_2(state):
        if (state.ball_position().x<(3*settings.GAME_WIDTH)/4) and (state.ball_position().x>(settings.GAME_WIDTH)/4) :
            return 0                                                           #Attaque
        else:
            return 1                                                           #Defense
            
#Balle > 3/4 
def Selection_3(state):
    if (state.key[0]==1):
        if (state.ball_position().x>(3*settings.GAME_WIDTH)/4):
            return 0                                                           #Attaque
        else:
            return 1                                                           #Defense
    if (state.key[0]==2):
        if (state.ball_position().x<(settings.GAME_WIDTH)/4):
            return 0                                                           #Attaque
        else:
            return 1                                                           #Defense
#==============================================================================
#Shoots   
def distance (a,b):
    return math.sqrt(((b.x-a.x)**2)+((b.y-a.y)**2))

def peut_shooter(state):
    if (distance(state.ball_position(),state.my_position())<=(settings.BALL_RADIUS+settings.PLAYER_RADIUS)):
        return True
    else:
        return False
    
def shoot(state,p):
    return SoccerAction(Vector2D(),p-state.my_position())

def shoot_tireur(state,p):
    return SoccerAction(Vector2D(),(p-state.my_position())*0.1)
    
def shoot_but(state,p):
    if (Selection_3(state)==0):
            return SoccerAction(Vector2D(),(p-state.my_position())*0.1)
    else:
        return mini_shoot(state,p)         
     
def mini_shoot(state,p):
    return SoccerAction(Vector2D(),(p-state.my_position())*0.03)
#==============================================================================
#Deplacements  
def aller_courrir_base(state,p):
    return SoccerAction(p-state.my_position(),Vector2D())
    
def aller_courrir(state,p):
    if (state.ball_position().x==settings.GAME_WIDTH/2) and (state.ball_position().y==settings.GAME_HEIGHT/2):
        return SoccerAction(Vector2D(),Vector2D())
    else:
        return SoccerAction(p-state.my_position(),Vector2D())
    
def aller_marcher(state,p):                                                    
    v1=p-state.my_position()
    v1.norm=0.05
    return SoccerAction(v1,Vector2D())

def aller_courrir_marcher(state,p):
    if (distance(p,state.my_position())<3):    
        return aller_marcher(state,p)
    else:
        return aller_courrir(state,p)
        
def aller_courrir_marcher_v2(state,p):
    if (distance(p,state.my_position())<3):    
        return aller_marcher(state,p)
    else:
        return aller_courrir_base(state,p) 
        
def aller_camper_static(state,p):
    v2= Vector2D((settings.GAME_WIDTH)/2,(3*settings.GAME_HEIGHT)/4)
    return aller_courrir_marcher_v2(state,v2)        
        
def aller_camper_proche(state,p):
    if (state.key[0]==1):
        if (p.x<(settings.GAME_WIDTH)/4) :
            v2= Vector2D((settings.GAME_WIDTH)/2,(3*settings.GAME_HEIGHT)/4)
        else:
            v2=p
    if (state.key[0]==2):
        if (p.x>(3*settings.GAME_WIDTH)/4) :
            v2= Vector2D((settings.GAME_WIDTH)/2,(3*settings.GAME_HEIGHT)/4)
        else:
            v2=p
    return aller_courrir_marcher_v2(state,v2)
    
def aller_camper_proche_v2(state,p):
    if (state.key[0]==1):
        if (p.x<(settings.GAME_WIDTH)/4) :
            v2= Vector2D((settings.GAME_WIDTH)/2,(settings.GAME_HEIGHT)/4)
        else:
            v2=p
    if (state.key[0]==2):
        if (p.x>(3*settings.GAME_WIDTH)/4) :
            v2= Vector2D((settings.GAME_WIDTH)/2,(settings.GAME_HEIGHT)/4)
        else:
            v2=p
    return aller_courrir_marcher_v2(state,v2)    
    
def aller_gardien(state,p):
    if (state.key[0]==1):
        if (state.ball_position().x+state.ball_vitesse().x>=(settings.GAME_WIDTH)/3) :
            v3=state.ball_position()-state.but_adv[state.key[0]]
            v3.norm=8.5
            v2= Vector2D(0,settings.GAME_HEIGHT/2)
            return aller_courrir_marcher_v2(state,v2+v3)       
        else:
            return aller_courrir_marcher_v2(state,p) 
    if (state.key[0]==2):
        if(state.ball_position().x+state.ball_vitesse().x<=(2*settings.GAME_WIDTH)/3):
            v3=state.ball_position()-state.but_adv[state.key[0]-2]
            v3.norm=8.5
            v2= Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)
            return aller_courrir_marcher_v2(state,v2+v3) 
        else:  
            return aller_courrir_marcher_v2(state,p)
            
def aller_gardien_static(state,p):
    if (state.key[0]==1):
        v3=state.ball_position()-state.but_adv[state.key[0]]
        v3.norm=8.5
        v2= Vector2D(0,settings.GAME_HEIGHT/2)
        return aller_courrir_marcher_v2(state,v2+v3)       
    if (state.key[0]==2):
        v3=state.ball_position()-state.but_adv[state.key[0]-2]
        v3.norm=8.5
        v2= Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)
        return aller_courrir_marcher_v2(state,v2+v3) 