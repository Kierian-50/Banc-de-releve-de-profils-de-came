from tools import * #importer tout de tools (communication avec arduino)
import matplotlib.pyplot as plt #import de la librairie matplotlib pour le graphique
import time #import de la librairie temps
from tkinter import * #importer de la librairie tkinter pour les interface graphique
import random #librairie simulation de hazard
import pickle #librairie enregistrement du ficher

def mesurer():
    global timer,valeurs1,valeurs2,temps,timeStart,x0,x1,y0,y1,y2,y3,potValeurs1,potValeurs2,angle,degres,minValeurs1,minValeurs2 #déclaration des variables globales

    #relevé des mesures des pots
    potValeurs1 = (entree('{"cible":"CAN3"}')-minValeurs1)*0.041 #potValeurs1 prend la valeur du potentiomètre de la came d'echappement avec le calcul de reconversion en mm
    #condition "si" qui permet d'éliminer les valeurs négatives impossibles
    if (potValeurs1>0):               #si potValeurs1 supérieur à 0 alors 
        valeurs1.append(potValeurs1)  #valeurs1 prend la valeur de potValeurs1
    else :                            #sinon
        potValeurs1 = 0               #potValeurs1 prend la valeur 0
        valeurs1.append(potValeurs1)  #valeurs2 prend la valeur de potValeurs1 qui est de 0
    
    potValeurs2 = (entree('{"cible":"CAN4"}')-minValeurs2)*0.034 #potValeurs2 prend la valeur du potentiomètre de la came d'admission avec le calcul de reconversion en mm
    #condition "si" qui permet d'éliminer les valeurs négatives impossibles
    if (potValeurs2>0):               #si potValeurs2 supérieur à 0 alors 
        valeurs2.append(potValeurs2)  #valeurs2 prend la valeur de potValeurs2
    else :                            #sinon
        potValeurs2 = 0               #potValeurs2 prend la valeur 0
        valeurs2.append(potValeurs2)  #valeurs2 prend la valeur de potValeurs2 qui est de 0
    
    #
    instant=time.time()-timeStart     # calcul du temps ecoule depuis l'instant initial
    temps.append(instant)             # ajout de instant a la liste des temps
    x1 = x0+1
    
    y1 = 300-(valeurs1[len(valeurs1)-1])*50 #coordonnée de départ :0,300 echelle y 50
    Canevas.create_line(x0, y0, x1, y1, width=2, fill='red') #ligne rouge de la valeurs 1 
    y0=y1
     
    y2 = 300-(valeurs2[len(valeurs2)-1])*50 #coordonnée de départ :0,300 echelle y 50
    y3=y2 #y0 de ma valeurs 2
    Canevas.create_line(x0, y3, x1, y2, width=2, fill='blue') #ligne bleu de la valeur 2
    
    x0=x1
   
    
    timer = Mafenetre.after(20, mesurer)
    
    #fonctionnement moteur
    sortie('{"cible":"moteurCC","consigne":125}') #envoie au moteur la consigne de 200 afin de le faire tourner quand on souhaite mesurer
    
    #récupération et calcul de la position angulaire de la came
    degres = ((entree('{"cible":"impulsions"}')*360)/1272) #la variable degres prend la valeur d'"impulsions" avec la formule qui permet d'obtenir la position angulaire de la poulie
    angle.append(degres) #angle prend la valeur de la variable degres
    

def graphe():
    global valeurs1,valeurs2,temps,degres,angle           #déclaration des variables globales
    fig = plt.figure(1, figsize=(10, 5))                  # taille de la fenetre
    plt.ylabel("Hauteur de la came en mm")                #nom de l'axe des ordonnées
    plt.xlabel("Position angulaire de la came en degrés") #nom de l'axe des abcisses
    plt.grid(True)                                        #affichage de la grille
    plt.title("Courbes de la hauteur des cames en fonction de la position angulaire de la came") #titre de la fenetre
    plt.plot(angle,valeurs1,"r",linewidth=0.8, label='Hauteur de la came d echappement')         # mise en place du label
    plt.plot(angle,valeurs2,"b--", label='Hauteur de la came d admission')                       # mise en place du label
    plt.plot(angle,valeurs1,"r",linewidth=0.8)           # trace la courbe rouge largeur 0.8
    plt.plot(angle,valeurs2,"b--")                       # trace la courbe bleue en pointillé
    plt.legend(loc="upper left")                         # affiche la légende
    plt.show()


def lancerMesure():
    global valeurs1,valeurs2,temps,timeStart,x0,y0,y3 #déclaration des variables globales
    print ("lancement de la mesure")
    valeurs1[:] = [] # vide la liste
    valeurs2[:] = [] # vide la liste
    temps[:] = []    # vide la liste
    angle[:] = []    # vide la liste
    timeStart = time.time()   # mesure de l'instant initial (t=0)
    x0=0
    y0=300
    y3=300 #y0 de ma valeurs 2
    mesurer()
    
def enregistrer():
    global nomFichier,valeurs1,valeurs2,temps #déclaration des variables globales
    print ("enregistrement des mesures")
    dataMesures = [valeurs1,valeurs2,temps,angle]
    fichier = open(nomFichier,'wb')
    pickle.dump(dataMesures,fichier)    # sérialisation
    fichier.close()
    
def lireFichier():
    global nomFichier,valeurs1,valeurs2,temps,angle #déclaration des variables globales
    print ("lecture du fichier des mesures")
    dataMesures = pickle.load(open(nomFichier, 'rb'))
    valeurs1 = dataMesures[0]
    valeurs2 = dataMesures[1]
    temps = dataMesures[2]
    angle = dataMesures[3]
    
def stop():   
    global timer,degres,angle #déclaration des variables globales
    if timer:
        Mafenetre.after_cancel(timer)
        timer = None
    print ("Fin des mesures")    
    sortie('{"cible":"moteurCC","consigne":0}') #envoie au moteur la consigne de 0 pour stopper le moteur quand on appuie sur stop
    (entree('{"cible":"retour"}')) #envoie 'retour' au programme en C qui permet de réinitialiser cptImpulsion
    
def indiceFichier():
    global nomFichier
    nomFichier = 'dataMesures' + str(int(indice.get()))
    texte.set(nomFichier)

def reinitialisationValeurs1():
    global minValeurs1,minValeurs2,releveValeurs1,releveValeurs2
    minValeurs1 = (entree('{"cible":"CAN3"}'))
    #minValeurs2 = (entree('{"cible":"CAN4"}'))

def reinitialisationValeurs2():
    global minValeurs1,minValeurs2,releveValeurs1,releveValeurs2
    #minValeurs1 = (entree('{"cible":"CAN3"}'))
    minValeurs2 = (entree('{"cible":"CAN4"}'))

def reinitialisationAngle():
     (entree('{"cible":"retour"}')) #envoie 'retour' au programme en C qui permet de réinitialiser cptImpulsion

init() #init communication arduino


#tables des valeurs à tracer
#===========================
valeurs1=[]   #table des grandeurs 1 à mesure
valeurs2=[]  #table des grandeurs 2 à mesurer 
temps=[]     #table du temps (abcisses)
angle=[]       #table des grandeurs en abscisse
potValeurs2=[] #initialisation d'une variable
potValeurs1=[] #initialisation d'une variable
degres=[]      #initialisation d'une variable
nomFichier = 'dataMesures'


# Création de la fenêtre principale
Mafenetre = Tk()

Mafenetre.title('Mesures')
Mafenetre.geometry('700x400+400+400')

Canevas = Canvas(Mafenetre, width = 500, height =300, bg ='white')
Canevas.pack(padx =5, pady =10)

# Création et positionnement d'un bouton MESURER
BoutonMesurer = Button(Mafenetre, text ='Mesurer', command = lancerMesure)
BoutonMesurer.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un bouton STOP
BoutonStop = Button(Mafenetre, text ='STOP', command = stop)
BoutonStop.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un bouton ENREGISTRER
BoutonEnregistrer = Button(Mafenetre, text ='Enregistrer', command = enregistrer)
BoutonEnregistrer.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un bouton LIRE FICHIER
BoutonEnregistrer = Button(Mafenetre, text ='Lire Fichier', command = lireFichier)
BoutonEnregistrer.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un bouton GRAPHE
BoutonEnregistrer = Button(Mafenetre, text ='Graphe', command = graphe)
BoutonEnregistrer.pack(side = LEFT, padx = 5, pady = 5)

# Création et positionnement d'un bouton MESURER
BoutonMesurer = Button(Mafenetre, text ='Réinitialisation echappement mini', command = reinitialisationValeurs1)
BoutonMesurer.pack(side = LEFT, padx = 5, pady = 5)

# Création et positionnement d'un bouton MESURER
BoutonMesurer = Button(Mafenetre, text ='Réinitialisation admission mini', command = reinitialisationValeurs2)
BoutonMesurer.pack(side = LEFT, padx = 5, pady = 5)

# Création et positionnement d'un bouton MESURER
BoutonMesurer = Button(Mafenetre, text ='Réinitialisation angle', command = reinitialisationAngle)
BoutonMesurer.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un bouton QUITTER
BoutonQuitter = Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy)
BoutonQuitter.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un widget Label pour le nom de fichier
texte = StringVar()
LabelFichier = Label(Mafenetre, textvariable = texte, fg ='red', bg ='white')
LabelFichier.pack(side = LEFT, padx = 5, pady = 5)
texte.set(nomFichier)

# Création d'un widget Spinbox
indice = StringVar()
boite = Spinbox(Mafenetre,from_=0,to=99,increment=1,textvariable=indice,width=5,command=indiceFichier)
boite.pack(side = LEFT, padx = 5, pady = 5)


Mafenetre.mainloop()