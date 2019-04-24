from mcpi import minecraft
from mcpi import block
from mcpi import vec3
from random import randint
import time

mc=minecraft.Minecraft.create()

# plaie créée par Maxime: la cage de TNT
def Max():

    Temps=30 #délai entre 2 tentatives
    TNT=2 #couches de TNT à poser
    AIR=0 #nombre de joueurs en vol

    # récupération des joueurs connectés
    joueurs=mc.getPlayerEntityIds()
    TotalJoueur=len(joueurs)

    while AIR != TotalJoueur:
        # tous les joueurs ne sont pas en vol
        mc.postToChat("Debut de la plaie, Bonne chance ;)")
        AIR=0
        for ID in joueurs:
            mc.entity.getPos(ID)
            pos=mc.entity.getPos(ID)
            mc.getBlock(pos.x,pos.y-1,pos.z)
        
            if mc.getBlock(pos.x,pos.y-1,pos.z) !=0:
                # le joueur n'est pas en vol
                mc.setBlocks(pos.x-TNT,pos.y-TNT,pos.z-TNT,pos.x+TNT,pos.y+TNT,pos.z+TNT,46,1)
                mc.postToChat("Ha Ha Ha")
                time.sleep(Temps)

            else:
                # le joueur est en vol
                AIR=AIR+1
                mc.postToChat("Bien joue !")
                time.sleep(Temps)
    
        # mise à jour de la liste des joueurs
        joueurs=mc.getPlayerEntityIds()
        TotalJoueur=len(joueurs)

    mc.postToChat("Fin de la plaie")
    
# plaie créée par Laurent: l'évaporation de l'eau
def Lau():

    # créé un bloc de laine de couleur aléatoire à la position
    def creer_bloc(pos):
        couleur = randint(0,15)
        mc.setBlock(pos.x,pos.y,pos.z,35,couleur)

    # teste si un bloc particulier existe autour d'une position
    def existe_autour(pos,id_block):
        for x in range(-1,2):
            for y in range(-1,2):
                for z in range(-1,2):
                    if mc.getBlock(pos.x+x,pos.y+y,pos.z+z) == id_block:
                        return True
        return False

    # transforme les blocs d'un type présent dans id_blocks_src autour d'une position par un block spécifique + affichage d'un message
    def transforme_autour(pos,id_blocks_src,id_block_dest,message):
        for x in range(-1,2):
            for y in range(-1,2):
                for z in range(-1,2):
                    if mc.getBlock(pos.x+x,pos.y+y,pos.z+z) in id_blocks_src:
                        mc.setBlock(pos.x+x,pos.y+y,pos.z+z,id_block_dest)
                        mc.postToChat(message)

    # créé un vecteur définissant une direction horizontale spécifique
    def choisir_direction():
        return vec3.Vec3(randint(-1,1),0,randint(-1,1))

    # déplace le bloc d'une position dans une direction
    def deplacer_bloc(pos,direction):
        new_pos = vec3.Vec3(pos.x+direction.x,pos.y+direction.y,pos.z+direction.z)
        creer_bloc(new_pos)
        return new_pos

    
    pos = vec3.Vec3(randint(-30,30),-1,randint(-30,30))
    creer_bloc(pos)
    print(pos)
    mc.postToChat("-=-= lancement evap'eau =-=-")

    pos_prec = pos
    direction = vec3.Vec3(0,0,0)
    nombre_deplacement = 0

    while not existe_autour(pos,103):
        # pas de pastèque à proximité immédiate

        # l'eau est transformée en air
        transforme_autour(pos,[8,9],0,"pouf! evaporee...")
        # changement de direction tous les 10 déplacements
        if nombre_deplacement % 10 == 0:
            direction = choisir_direction()
        # on garde deux blocs pour la plaie, le bloc précédent est remplacé par une paquerette
        if pos_prec != pos:
            mc.setBlock(pos_prec.x,pos_prec.y,pos_prec.z,37)
        pos_prec = pos
        pos = deplacer_bloc(pos_prec,direction)
        nombre_deplacement = nombre_deplacement +1
        time.sleep(1)

    mc.postToChat("-=-= evap'eau terminee =-=-")
    
# plaie créée par Aymeric: la lave extensible
def Aym():
    
    # teste si tous les joueurs sont sur des pastèques
    def joueurs_pasteque():
        joueurs = mc.getPlayerEntityIds()
        for joueur in joueurs:
            pos = mc.entity.getPos(joueur)
            if mc.getBlock(pos.x,pos.y-1,pos.z) != 103:
                return False
        return True

    # recherche d'un bloc d'eau
    eau = 0
    while eau != 9:
        x = randint(-127,127)
        z = randint(-127,127)
        eau = mc.getBlock(x,-1,z)

    print("l'eau :" + str(eau) )
    print(x)
    print(z)

    temp1 = 10
        
    # création d'un bloc de lave sur l'eau
    mc.postToChat("[JOKER] La plaie est lancee bonne chance !")
    mc.setBlock(x,0,z,block.LAVA_FLOWING.id)

    larg = 1 #étendue de la lave
    blocl = 1 #nombre de blocs de lave créé ce tour-ci

    while blocl > 0 and not joueurs_pasteque():
        # au moins un bloc créé au dernier tour et les joueurs ne sont pas tous sur une pastèque: on étend la zone couverte par la lave
        blocl = 0
        for modif in range( -larg, larg + 1 ):
            if mc.getBlock(x + larg ,-1,modif + z) in [9,4]:
                mc.setBlock(x + larg ,0,modif + z,block.LAVA_FLOWING.id)
                blocl = blocl + 1
            
            if mc.getBlock(x - larg ,-1,modif + z) in [9,4]:
                mc.setBlock(x - larg ,0,modif + z,block.LAVA_FLOWING.id)
                blocl = blocl + 1
        
        for modif in range(1-larg , larg):
            if mc.getBlock(modif + x,-1, z + larg) in [9,4]:
                mc.setBlock(modif + x,0, z + larg,block.LAVA_FLOWING.id)
                blocl = blocl + 1
            
            if mc.getBlock(modif + x,-1, z - larg) in [9,4]:
                mc.setBlock(modif + x,0, z - larg,block.LAVA_FLOWING.id)
                blocl = blocl + 1
        
        print(larg)
        
        larg = larg + 1
        time.sleep(temp1)

    mc.postToChat("[JOKER] La plaie est terminee! Il y a eu " + str(larg) + " vagues")

# plaie créée par Thibaud: l'ascenseur
def Thib():

    # choix d'un joueur au hasard
    entityId = mc.getPlayerEntityIds()
    joueurChoisi = randint(0,len(entityId)-1)
    pos = mc.entity.getPos(entityId[joueurChoisi])

    # création d'une structure autour du joueur 
    mc.setBlock(pos.x,pos.y-1,pos.z,1)
    mc.setBlock(pos.x-1,pos.y,pos.z,1)
    mc.setBlock(pos.x,pos.y,pos.z-1,1)
    mc.setBlock(pos.x+1,pos.y,pos.z,1)
    mc.setBlock(pos.x,pos.y,pos.z+1,1)

    modif = 0

    while pos.y - modif < -200:
        # la position du joueur modifiée est dans la map
        modif = modif + 1

        # suppression de la structure précédente
        mc.setBlock(pos.x,pos.y-1+1-modif,pos.z,0)
        mc.setBlock(pos.x-1,pos.y+1-modif,pos.z,0)
        mc.setBlock(pos.x,pos.y+1-modif,pos.z-1,0)
        mc.setBlock(pos.x+1,pos.y+1-modif,pos.z,0)
        mc.setBlock(pos.x,pos.y+1-modif,pos.z+1,0)
        
        # création de la structure à la position modifiée
        mc.setBlock(pos.x,pos.y-1-modif,pos.z,1)
        mc.setBlock(pos.x-1,pos.y-modif,pos.z,1)
        mc.setBlock(pos.x,pos.y-modif,pos.z-1,1)
        mc.setBlock(pos.x+1,pos.y-modif,pos.z,1)
        mc.setBlock(pos.x,pos.y-modif,pos.z+1,1)

        # déplacement du joueur à la position modifiée
        mc.entity.setPos(entityId[joueurChoisi],pos.x,pos.y-modif,pos.z)
        time.sleep(0.1)

# exécutio d'une plaie au hasard
Start=randint(1,4)

if Start ==1:
    Max()
if Start ==2:
    Lau()
if Start ==3:
    Aym()
if Start ==4:
    Thib()

