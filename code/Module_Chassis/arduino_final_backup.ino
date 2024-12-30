#include <Servo.h>
#include <AFMotor.h>

AF_DCMotor moteurA1(1);
AF_DCMotor moteurA2(2);
AF_DCMotor moteurB1(3);
AF_DCMotor moteurB2(4);
Servo myservo;   

const int buzzer =  8;
const int echoPin = 7;   
const int trigPin = 6;  
const int servoPin = 5;

int vitesse;
int angle;
bool si_obstacle;
bool si_actif;
bool si_sonner;
bool si_scanner = 0;

bool interruption_en_cours = false; 						// Indique si on gère l'interruption
long distance = 0 ;

										//AF_DCMotor moteur(4); 
										//moteur.setSpeed(i);
										//moteur.run(BACKWARD);
										//moteur.run(FORWARD); 
										//myservo.attach(10);
										//myservo.write(pos);

void setup() {
  										// Configurer les pins du capteur à ultrasons
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  										// Configurer le servo-moteur
  myServo.attach(servoPin);
  myServo.write(0); 								// Initialiser le servo à la position centrale

  										// Initialiser la communication série
  
  pinMode(2, INPUT_PULLUP); 							// Pin utilisée pour détecter si_obstacle
  attachInterrupt(digitalPinToInterrupt(2), eviterObstacle, CHANGE); 		// Déclencher sur tout changement

  
  
  Serial.begin(9600);
  scan_initial();
}


void loop() {
  										// If there is data in the serial buffer
  if (Serial.available() > 0) {
    										// Read the entire line from serial
    String receivedString = Serial.readStringUntil('\n');
    										// Parse the received string
    parseCommand(receivedString);

    if (si_sonner){
		sonner();
    }        
    if (si_actif){
    		if(! si_scanner){
    			scan_initial();
    			si_scanner = 1;
		}
		rouler(vitesse,angle);
		getDistance();
		sendDistance();
		if (distance < 5){
			stop();
			if(si_obstacle){
				eviterObstacle();
			}
			if(! si_obstacle){
				eviterObstacle();
			}
		
		}
    }
    else {
 		 
    	}
    
    
  }

}


void parseCommand(String command) {
  										// Séparer la commande en parties
  int firstComma = command.indexOf(',');
  int secondComma = command.indexOf(',', firstComma + 1);
  int thirdComma = command.indexOf(',', secondComma + 1);
  int fourthComma = command.indexOf(',', thirdComma + 1);

  										// Vérifier que la commande contient bien 5 parties
  if (firstComma != -1 && secondComma != -1 && thirdComma != -1 && fourthComma != -1) {
    										// Extraire les valeurs
     vitesse = command.substring(0, firstComma).toInt(); 			// Vitesse
     angle = command.substring(firstComma + 1, secondComma).toInt(); 		// Angle
     si_obstacle = command.substring(secondComma + 1, thirdComma).toInt(); 	// Si obstacle
     si_actif = command.substring(thirdComma + 1, fourthComma).toInt(); 	// Si actif
     si_sonner = command.substring(fourthComma + 1).toInt(); 			// Si sonner

    										// Utiliser les valeurs dans votre logique
    afficher(vitesse, angle, si_obstacle, si_actif, si_sonner);
  } else {
    										// Gérer les erreurs si le format de la commande est invalide
    Serial.println("Erreur : commande invalide !");
  }
}

										// Exemple de fonction move qui utilise les 5 valeurs
void afficher(int vitesse, int angle, int si_obstacle, int si_actif, int si_sonner) {
  										// Ajoutez ici votre logique de mouvement
  Serial.print("Vitesse : ");
  Serial.println(vitesse);
  Serial.print("Angle : ");
  Serial.println(angle);
  Serial.print("Si obstacle : ");
  Serial.println(si_obstacle);
  Serial.print("Si actif : ");
  Serial.println(si_actif);
  Serial.print("Si sonner : ");
  Serial.println(si_sonner);
}

void sonner(){
	//logique pour sonner
}
void scan_initial(){
	// le robot fait lentement un tour autour de lui meme
}
void eviterObstacle(){
	// logique pour eviter un obstacle
}
void stop(){
}
void rouler(int vitesse, int angle){
	getDistance();
}

void getDistance() {
  digitalWrite(trigPin, LOW);long long getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Calculer la durée du signal réfléchi
  long duration = pulseIn(echoPin, HIGH);

  // Convertir la durée en distance (en cm)
  long distance_f = duration * 0.034 / 2;
  distance = distance_f;
  //return distance;
}
void sendDistance() {
  Serial.print("Distance:");
  Serial.println(distance);
}

