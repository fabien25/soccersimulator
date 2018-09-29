from soccersimulator import SoccerTeam
from football import Campeur_proche, Gardien, Fonceur_dribbleur, Passeur, Campeur_proche_v2

#Choix de Strat
def get_team(i):
    team1 = SoccerTeam(name="Fabien25",login="etu1")
    team2 = SoccerTeam(name="Fabien25",login="etu2")
    team4 = SoccerTeam(name="Fabien25",login="etu2")
    if (i==1):
        team1.add("Gollum",Fonceur_dribbleur())
        return team1
    if (i==2):
        team2.add("Samwise_Gamgee",Gardien())
        team2.add("Frodo_Baggins",Campeur_proche())
        return team2
    if (i==4):
        team4.add("Gimli",Gardien())
        team4.add("Aragorn",Campeur_proche())
        team4.add("Legolas",Passeur())
        team4.add("Gandalf",Campeur_proche_v2())
        return team4