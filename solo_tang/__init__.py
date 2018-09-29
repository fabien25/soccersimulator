from soccersimulator import SoccerTeam
from golf import SlalomStrategy, GolfStrategy

def get_golf_team():
    team = SoccerTeam(name="Fabien25",login="etu1")
    team.add("John",GolfStrategy())
    return team

def get_slalom_team1():
    team1 = SoccerTeam(name="Fabien25",login="etu1")
    team1.add("John",SlalomStrategy())
    return team1

def get_slalom_team2():
    team2 = SoccerTeam(name="Fabien25",login="etu1")
    team2.add("John",SlalomStrategy())
    team2.add("John",SlalomStrategy())
    return team2
