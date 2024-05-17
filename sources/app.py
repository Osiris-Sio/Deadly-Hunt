import pyxel
import random
import time

################ Deadly Hunt
## by Les cousins
## by AMEDRO Louis - LAPÔTRE Marylou

class Jeu:
    def __init__(self):
        pyxel.init(256, 256, title="Nuit du Code | Deadly Hunt", fps = 60)
        pyxel.load("2.pyxres")
        self.joueur = Joueur(10, 178)
        self.monstres = []
        self.pieces = []
        self.score = 0
        self.menu = True
        self.time = 0
        self.fin = False
        pyxel.run(self.update, self.draw)
        
           
    def update(self):
        if self.menu :
            if pyxel.btnr(pyxel.KEY_SPACE) :
                self.menu = False
        else :
            if not self.fin :
                #PERSONNAGE
                self.joueur.deplacement()
                self.joueur.saut()
                self.joueur.gravite()
                self.collision_piece()

                #PIECE
                self.apparition_piece()


                #MONSTRE
                self.apparition_monstre()
                for monstre in self.monstres:
                    monstre.deplacement()
                    monstre.deplacer()
                    if self.joueur.attaque(monstre):
                        self.score += 10
                        self.monstres.remove(monstre)
                self.disparition_monstre()
                self.fin = self.collision_monstre()
                if pyxel.frame_count % 60 == 0:
                    self.time += 1
                    
        
    def draw(self):
        pyxel.cls(5)
        self.plateforme()
        if self.menu :
            pyxel.text(110, 30, "Deadly Hunt ", 7)
            pyxel.text(7, 218, "Clique sur Espace pour Jouer ! ", 7)
        else :
            pyxel.text(7, 218, "Score : " + str(self.score), 7)
            pyxel.text(175, 218, "Temps : " + str(self.time) + ' secondes', 7)
            
        if not self.fin :   
            #MONSTRES
            for monstre in self.monstres:
                monstre.dessiner()
            #PERSONNAGE
            self.joueur.dessiner()
            self.joueur.dessine_attaque()
            #PIECE
            for piece in self.pieces :
                piece.dessiner()
        else :
            pyxel.text(110, 30, "GAME OVER", 7)
        
    def apparition_monstre(self):
        if pyxel.frame_count % 120 == 0:
            type_m = random.randint(1, 2)
            d = random.choice(['gauche', 'droite'])
            if type_m == 1:
                self.monstres.append(Monstre(random.randint(0, 240), 0, d, type_m))
            else:
                if d == 'droite':
                    x= -15
                else:
                    x = 255
                self.monstres.append(Monstre(x, 88, d, type_m))
      
    def disparition_monstre(self):
        for monstre in self.monstres:
            if monstre.mort and monstre.action_mort >= 4 or monstre.x < -12 or monstre.x > 256:
                self.monstres.remove(monstre)
                
    def apparition_piece(self):
        if pyxel.frame_count % 600 == 0:
            x = random.randint(0, 250)
            self.pieces.append(Piece(x, 187))
       
    def collision_piece(self):
        for piece in self.pieces:
            if self.joueur.y <= piece.y <= self.joueur.y + 16:
                #gauche
                if self.joueur.x <= piece.x <= self.joueur.x + 11 :
                    self.pieces.remove(piece)
                    self.score += 5
                #droit
                elif self.joueur.x <= piece.x+6 <= self.joueur.x + 11 :
                    self.pieces.remove(piece)
                    self.score += 5
                            
    def collision_monstre(self):
        for monstre in self.monstres:
            if self.joueur.x <= monstre.x <= self.joueur.x + 8 and self.joueur.y -1  <= monstre.y <= self.joueur.y + 1:
                return True
            else: 
                return False
            
            
    def plateforme(self):
        #du bas
        for i in range(10):
            pyxel.blt(-23+i*43, 193, 0, 140, 24, 45, 80)
        
        espace = 45
        #1e
        pyxel.blt(0, 193-espace, 0, 136, 8, 16, 12)
        for i in range(4):
            pyxel.blt(16+16*i, 193-espace, 0, 152, 8, 16, 11)
        pyxel.blt(80, 193-espace, 0, 168, 8, 16, 12)
    
        
        pyxel.blt(162, 193-espace, 0, 136, 8, 16, 12)
        for i in range(4):
            pyxel.blt(178+16*i, 193-espace, 0, 152, 8, 16, 11)
        pyxel.blt(240, 193-espace, 0, 168, 8, 16, 12)
        
        #2e
        pyxel.blt(0, 193-espace*2, 0, 136, 8, 16, 12)
        for i in range(1):
            pyxel.blt(16+16*i, 193-espace*2, 0, 152, 8, 16, 11)
        pyxel.blt(32, 193-espace*2, 0, 168, 8, 16, 12)
        
        pyxel.blt(96, 193-espace*2, 0, 136, 8, 16, 12)
        for i in range(2):
            pyxel.blt(112+16*i, 193-espace*2, 0, 152, 8, 16, 11)
        pyxel.blt(144, 193-espace*2, 0, 168, 8, 16, 12)
        
        pyxel.blt(208, 193-espace*2, 0, 136, 8, 16, 12)
        for i in range(1):
            pyxel.blt(224+16*i, 193-espace*2, 0, 152, 8, 16, 11)
        pyxel.blt(240, 193-espace*2, 0, 168, 8, 16, 12)
        
        #3e
        pyxel.blt(32, 193-espace*3, 0, 136, 8, 16, 12)
        for i in range(10):
            pyxel.blt(48+16*i, 193-espace*3, 0, 152, 8, 16, 11)
        pyxel.blt(208, 193-espace*3, 0, 168, 8, 16, 12)
        
          

#################Joueur####################  
    
class Joueur():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 'droite'
        self.temps_saut = None
        self.animation = None
        self.en_attaque = False 
        
    def collisions_plateformes(self):
        tab_x = [[[32, 224]], [[0, 48], [96, 160], [208, 256]], [[0, 96], [162, 256]]]
        tab_y = [58, 103, 148]
        
        #tab_x = [[[0, 96], [162, 256]], [[0, 48], [96, 160]], [[224, 256], [32, 224]]]
        #tab_y = [[148, 159], [103, 114], [158, 160]]
        
        j = 0
        while j < len(tab_y) :
            if tab_y[j] == self.y + 16 :
                i = 0
                while i < len(tab_x[j]) :
                    if tab_x[j][i][0] < self.x + 5 < tab_x[j][i][1] :
                        return True
                    i += 1
            j += 1
        return False
        
    def gravite(self) :
        if self.temps_saut == None and self.y < 177 and not self.collisions_plateformes() :
            self.y += 1
    
    def deplacement(self) : #0 140
        if pyxel.btn(pyxel.KEY_Q) and self.x > 0:
            self.x -= 2
            self.direction = 'gauche'
        if pyxel.btn(pyxel.KEY_D) and self.x < 242 :
            self.x += 2
            self.direction = 'droite'
        if pyxel.btn(pyxel.KEY_SPACE) and not (140 < self.y + 1 < 152) and self.temps_saut == None :
            self.temps_saut = time.time()
            
    def saut(self) :
        if self.temps_saut != None :
            if time.time() - self.temps_saut < 0.25 :
                self.y -= 2
            if time.time() - self.temps_saut > 0.25 :
                self.y -= 1
            if  time.time() - self.temps_saut > 0.5 :
                self.temps_saut = None
        
    def attaque(self, monstre):
        if self.direction == 'droite' and self.x + 5 <= monstre.x <= self.x + 20 and self.y - 2 <= monstre.y <= self.y + 2 and self.en_attaque:
            return True
        elif self.direction == 'gauche' and self.x - 20 <= monstre.x <= self.x - 5 and self.y - 2 <= monstre.y <= self.y + 2 and self.en_attaque:
            return True
        return False
            
    def dessiner(self):
        if self.direction == 'droite':
            pyxel.blt(self.x , self.y, 0, 2, 8, 12, 16, 5)
        else :
            pyxel.blt(self.x , self.y, 0, 66, 8, 12, 16, 5)
            
    def dessine_attaque(self):
        if self.animation != None and time.time() - self.animation > 0.5 :
            self.animation = None
            self.en_attaque = False
        if pyxel.btnr(pyxel.KEY_M) and not self.en_attaque:
            self.animation = time.time()
            self.en_attaque = True
        
        if self.en_attaque and self.direction == 'droite' :
            pyxel.blt(self.x+11 , self.y-5, 0, 0, 200, 16, 16, 5)
        if self.en_attaque and self.direction == 'gauche':
            pyxel.blt(self.x-14 , self.y-5, 0, 0, 200, -16, 16, 5)
     
    
    
    
##################Monstre####################    
    
class Monstre:
    def __init__(self, x, y, direction, genre):
        self.x = x
        self.y = y
        self.genre = genre
        self.direction = direction
        self.tombe = True
        self.mort = False
        self.action_mort = 0
        
    def deplacement(self):
        if pyxel.frame_count % 60 == 0 and not (self.y > 177) and not self.tombe:
            n = random.randint(0, 1)
            if n == 0:
                self.direction = 'droite'
            else:
                self.direction = 'gauche'
        
    def deplacer(self):
        dep = 0.5
        if self.direction == 'gauche':
            if not pyxel.pget(self.x + 8, self.y + 15) == 0 and not pyxel.pget(self.x + 9, self.y + 15) == 0 :
                self.y += 1
                self.tombe = True
            else:
                self.tombe = False
            if not self.tombe :
                if self.x - dep < 0 and not (self.y > 177) :
                    self.direction = 'droite'
                else:
                    self.x -= dep
        else:
            if not pyxel.pget(self.x + 1, self.y + 15) == 0 and not pyxel.pget(self.x, self.y + 15) == 0:
                self.y += 1
                self.tombe = True
            else :
                self.tombe = False
            if not self.tombe : 
                if self.x + dep > 240 and not (self.y > 177) :
                    self.direction = 'gauche'
                else:
                    self.x += dep
    
    def dessiner(self):
        if self.genre == 1:
            if self.direction == 'gauche':
                if not self.mort :
                    pyxel.blt(self.x, self.y, 0, 67, 57, 11, 15, 5)
                else :
                    pyxel.blt(self.x, self.y, 0, 67 + self.action_mort*15, 89, 11, 15, 5)
                    if pyxel.frame_count % 5 == 0 :
                        self.action_mort += 1 
            else:
                if not self.mort :
                    pyxel.blt(self.x, self.y, 0, 50, 57, 11, 15, 5)
                else :
                    pyxel.blt(self.x, self.y, 0, 2 + self.action_mort*15, 89, 11, 15, 5)
                    if pyxel.frame_count % 5 == 0 :
                        self.action_mort += 1
        else:
            if self.direction == 'gauche':
                if not self.mort :
                    pyxel.blt(self.x, self.y, 0, 67, 152, 11, 16, 5) 
                else:
                    pyxel.blt(self.x, self.y, 0, 3 + self.action_mort*15, 184, 11, 15, 5)
                    if pyxel.frame_count % 5 == 0 :
                        self.action_mort += 1
            else:
                if not self.mort :
                    pyxel.blt(self.x, self.y, 0, 3, 152, 11, 16, 5)
                else :
                    pyxel.blt(self.x, self.y, 0, 3 + self.action_mort*15, 184, 11, 15, 5)
                    if pyxel.frame_count % 5 == 0 :
                        self.action_mort += 1
    
class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.action = 0
        
    def dessiner(self):
        if pyxel.frame_count % 30 == 0:
            self.action = 1
        elif pyxel.frame_count % 15 == 0:
            self.action = 0
        if self.action == 0:
            pyxel.blt(self.x, self.y, 0, 49, 201, 6, 6, 5)
        else :
            pyxel.blt(self.x+1, self.y, 0, 58, 201, 4, 6, 5)
             
Jeu()






