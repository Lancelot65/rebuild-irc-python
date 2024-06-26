import regex as re

class IRCClient:
    def __init__(self):
        self.utilisateurs = set()
        self.commande = {
            "NICK": self.NICK,
            "EXIT": self.EXIT,
        }
        self.here = True
        self.loop()

    def is_CHANTYPES(self, chantype : str) -> bool:
        return chantype[0] == "#" or chantype[:2] in ["&#", "#&"]

    def NICK(self, nickname : str):
        if nickname in self.utilisateurs:
            return "ERR_NICKNAMEINUSE"  # 433
        elif self.is_CHANTYPES(nickname) or nickname[:1] == '\'' or nickname[0] == " " or nickname[0].isdigit():
            return "ERR_ERRONEUSNICKNAME"  # 432
        elif nickname == "":
            return "ERR_NONICKNAMEGIVEN"  # 431
        else:
            self.utilisateurs.add(nickname)
            return "NICK_OK"
    

    
    
    def EXIT(self):
        self.here = False
        
    def analyser_input(self, entree : str):
        if entree == "":
            return
        if entree[0] == "/":
            self.check_commande(entree)
        else:
            print("message maybe") 
    
    def check_commande(self, entree : str):
        pattern = r"\/(\S+)"
        match = re.match(pattern, entree)

        if match.group(1) in self.commande:
            self.commande[match.group(1)]("test")
            print(self.utilisateurs)
        else:
            print("invalid commande")

    def loop(self):
        while self.here:
            print("> ", end="")
            self.analyser_input(input())

irc = IRCClient()