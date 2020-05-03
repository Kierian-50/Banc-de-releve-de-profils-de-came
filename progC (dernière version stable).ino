//bibliothèque
#include <ArduinoJson.h> //inclut la bibliothèque "ArduinoJson.h"

//potentimètre :
#define poto A3 //la broche A3 prend le nom de poto (pour les potentiomètres)
#define pote A4 //la broche A4 prend le nom de pote (pour les potentiomètres)

  float PoteValeur ; //je déclare une variable qui peut prendre des valeurs décimales
  float PotoValeur ; //je déclare une variable qui peut prendre des valeurs décimales
  float AnalogPote ; //je déclare une variable qui peut prendre des valeurs décimales
  float AnalogPoto ; //je déclare une variable qui peut prendre des valeurs décimales

//motoréducteur : 
#define OUT_1 9       
#define OUT_2 6       
#define codeur1 3     
#define codeur2 7     

unsigned long impulsion;         //durée de l'impulsion sur le capteur
int commandePWM;                 //vitesse souhaitée entre 0 et 255
float vitesse;                   //je déclare une variable "vitesse" qui peut avoir des virgules
float ecart;                     //je déclare une variable "ecart" qui peut avoir des virgules
float consigne = 0;              // Je déclare la variable de consigne et je lui donne la valeur de 40 correspondant à 40 tr/min

//transmission avec le programme python
char car;                        //initialisation du caractère du nom de car
String messageSerie;

long topPulse;                   //initialisation de la variable topPulse

//comptage
long cptImpulsion = 0;           //initialisation de la variable impultions comptées

int Degres = 0;                  //initialisation de la variable Degres
int Tour = 0;                    //initialisation de la variable Tour 


void setup() {
  Serial.begin(115200);          //Initialisation de la communication avec la console
  pinMode(OUT_1, OUTPUT);   
  pinMode(OUT_2, OUTPUT);   
  pinMode(codeur1, INPUT_PULLUP);   
  pinMode(codeur2, INPUT_PULLUP); 
  digitalWrite(OUT_2,LOW);       // Sortie choix du OUT_2 de rotation
  commandePWM =0;                //la variable commandePWM = 0
   
  //comptage
  attachInterrupt(digitalPinToInterrupt(3), compte, CHANGE);//interrompre le programme pour compter chaque impulsion du codeur sur le pin 3 avec le sous programme "compte" et il compte a chaque changement d'état
  
 }
void loop() {   
  FonctionnementMoteur(); // appelle le sous programme FonctionnementMoteur()
 //transmission avec le programme en python
 //lecture du messqage en serie 
  if (Serial.available() > 0){
    car = char(Serial.read());
    messageSerie += car;
  }

  if(car==125){ //fin d'une requete "}"
    car = '*'; // different de fin de ligne

    String reponse = "";
    //extraction de la bibliothèque Json
    DynamicJsonBuffer jsonBuffer;
    String input = messageSerie;
    JsonObject& root = jsonBuffer.parseObject(input);


    if (strcmp("moteurCC", root["cible"])  == 0){ //strcmp permet de comparer deux chaînes de caractères => il compare si la cible est "moteurCC"
      consigne = root["consigne"];                //si oui 
      topPulse=micros();                          //la variable topPulse = micros
    }
    
    else if (strcmp("CAN3", root["cible"]) == 0) reponse = analogRead(A3);      //si la cible est 'CAN3' alors donner l'état de A3
    
    else if (strcmp("CAN4", root["cible"]) == 0) reponse = analogRead(A4);      //si la cible est 'CAN4' alors donner l'état de A4
      
    else if (strcmp("impulsions", root["cible"])  == 0) reponse = cptImpulsion; //si la cible est 'impulsions' alors donner le nombre d'impulsion compter avec cptImpulsion

    else if (strcmp("retour", root["cible"]) == 0) {
      cptImpulsion = 0; // si la cible est 'retour' alors cpt impulsion = 0
      reponse = cptImpulsion;
    }
    
     

    if (reponse !="") Serial.print(reponse + "\n");
    messageSerie = "";  // Remise à zéro du message
  }

  
}

void FonctionnementMoteur() {                     //sous programme du fonctionnement du moteur avec régulation de vitesse
  vitesse = 1000000 * 60 / (6 * 53 * impulsion);  //calcul de la vitesse en fonction des codeurs incrementaux
  ecart = consigne - vitesse;                     //calcul de l'écart entre la consigne et la vitesse reel (le tout est en tr/min)
  commandePWM = min(254,5*ecart);                 /*la consigne que l'on va donner au moteur est "commandePWM". On multiplie par 5 pour amplifier le signal et etre plus précis.
  On dit aussi que la valeur de l'écart ne peut pas être supérieur à 254.*/
  commandePWM = max(0,commandePWM);               //on dit que la valeur minimal est 0. 
  analogWrite(OUT_1,commandePWM);                 //envoi de la valeur vers la sortie PWM 
}

void compte(){                                    //sous programme compte qui permet de compte les impulsions
  cptImpulsion ++;                                // à chaque impulsion le programme compte + 1
  impulsion = micros()-topPulse;
  topPulse = micros();
  
}
