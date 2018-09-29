from soccersimulator import GolfState,Golf,Parcours1,Parcours2,Parcours3,Parcours4
from soccersimulator import SoccerTeam,show_simu
from soccersimulator import Strategy,SoccerAction,Vector2D,settings

GOLF = 0.001
SLALOM = 10.


class DemoStrategy(Strategy):
    def __init__(self):
        super(DemoStrategy,self).__init__("Demo")
    def compute_strategy(self,state,id_team,id_player):
        """ zones : liste des zones restantes a valider """
        zones = state.get_zones(id_team)
        if len(zones)==0:
            """ shooter au but """
            return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                    Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
        """ zone : carre de zone avec z.position angle bas,gauche et z.l longueur du cote
            centre du carre : zone.position+Vector2D(z.l/2.,z.l/2.)
            zone.dedans(point) : teste si le point est dans la zone
        """
        zone = zones[0]
        """ si la ball est dans une zone a valider """
        if zone.dedans(state.ball.position):
            return SoccerAction()
        """ sinon """
        distance = state.player_state(id_team,id_player).position.distance(zone.position+zone.l/2.)
        return SoccerAction()
                    
                    
class SlalomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Slalom")
    def compute_strategy(self,state,id_team,id_player):
        #liste des zones a valider
        zones = state.get_zones(id_team)
        #si la liste est vide
        if len(zones)==0:
            """ shooter au but """
            return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                    Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)        
        else:
            zone = zones[0]
            #si la balle est dans une zone
            if zone.dedans(state.ball.position):
                #shoot au but
                if len(zones)==0:
                    return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
                
                #ou si il reste dautre zone
                else:
                    return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                    zone.position-state.ball.position)    
                
            #si la balle nest pas dans une zone        
            else:
                #shoot au but
                if len(zones)==0:
                    return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
                #ou si il reste dautre zone
                else:
                    return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                        zone.position-state.ball.position)  
                    
#class GolfStrategy(Strategy):
#    def __init__(self):
#        Strategy.__init__(self,"golf")
#        self.comportement=Comportement(golf,golf,Selection_1)
#    def compute_strategy(self,state,id_team,id_player):
#        #liste des zones a valider
#        zones = state.get_zones(id_team)
#        #si la liste est vide
#        if len(zones)==0:
#            """ shooter au but """
#            return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
#                    Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
#        else:
#            zone = zones[0]
#            #si la balle est dans une zone
#            if zone.dedans(state.ball.position):
#                #shoot au but
#                if len(zones)==0:
#                    return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
#                
#                #ou si il reste dautre zone
#                else:
#                    return Joueur(MyState(state,id_team,id_player),self.comportement) 
#                
#            #si la balle nest pas dans une zone        
#            else:
#                #shoot au but
#                if len(zones)==0:
#                    return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
#                #ou si il reste dautre zone
#                else:
#                    return Joueur(MyState(state,id_team,id_player),self.comportement)  
                    
class GolfStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Slalom")
    def compute_strategy(self,state,id_team,id_player):
        #liste des zones a valider
        zones = state.get_zones(id_team)
        #si la liste est vide
        if len(zones)==0:
            """ shooter au but """
            return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                    Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)        
        else:
            zone = zones[0]
            #si la balle est dans une zone
            if zone.dedans(state.ball.position):
                #shoot au but
                if len(zones)==0:
                    return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
                
                #ou si il reste dautre zone
                else:
                    return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                    (zone.position-state.ball.position)*0.03)    
                
            #si la balle nest pas dans une zone        
            else:
                #shoot au but
                if len(zones)==0:
                    return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
                #ou si il reste dautre zone
                else:
                    return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                        (zone.position-state.ball.position)*0.03)  

#team1 = SoccerTeam()
#team2 = SoccerTeam()
#team1.add("John",GolfStrategy())
#team2.add("John",DemoStrategy())
#simu = Parcours1(team1=team1,vitesse=GOLF)
#show_simu(simu)
#simu = Parcours2(team1=team1,vitesse=GOLF)
#show_simu(simu)
#simu = Parcours3(team1=team1,vitesse=SLALOM)
#show_simu(simu)
#simu = Parcours4(team1=team1,team2=team2,vitesse=SLALOM)
#show_simu(simu)

#golf passer et sarreter dans les carres puis marquer    OK
#slalom = juste passer   OK
