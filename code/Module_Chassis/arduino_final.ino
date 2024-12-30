#include <Servo.h>
#include <AFMotor.h>

AF_DCMotor moteurFrontLeft(1);
AF_DCMotor moteurFrontRight(3);
AF_DCMotor moteurBackLeft(2);
AF_DCMotor moteurBackRight(4);
Servo myservo;   

const int buzzer =  8;
const int echoPin = 7;   
const int trigPin = 6;  
const int servoPin = 5;
int maxSpeed = 255;
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
  myServo.write(90); 								// Initialiser le servo à la position centrale

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
    }else{
     		stop_sonner();
    }        
    if (si_actif){
    		if(! si_scanner){
    			scan_initial(vitesse);
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
	digitalWrite(buzzer,HIGH);
}
void stop_sonner(){
	//logique pour sonner
	digitalWrite(buzzer,LOW);
}
void scan_initial(int vitesse){
	// le robot fait lentement un tour autour de lui meme

	si_scanner = 1;
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


void rouler(int vitesse, int angle) {
  // Conversion de l'angle en radians
  float rad = angle * PI / 180.0;

  // Calcul des vitesses pour chaque moteur
  float frontLeftSpeed = sin(rad) + cos(rad);   // Avant gauche
  float frontRightSpeed = sin(rad) - cos(rad);  // Avant droit
  float backLeftSpeed = sin(rad) - cos(rad);    // Arrière gauche
  float backRightSpeed = sin(rad) + cos(rad);   // Arrière droit

  // Mise à l'échelle des vitesses pour respecter la plage [-255, 255]
  float maxMagnitude = max(max(abs(frontLeftSpeed), abs(frontRightSpeed)),
                           max(abs(backLeftSpeed), abs(backRightSpeed)));
  if (maxMagnitude > 1.0) {
    frontLeftSpeed /= maxMagnitude;
    frontRightSpeed /= maxMagnitude;
    backLeftSpeed /= maxMagnitude;
    backRightSpeed /= maxMagnitude;
  }

  // Application des vitesses aux moteurs
  setMotorSpeed(motorFrontLeft, frontLeftSpeed);
  setMotorSpeed(motorFrontRight, frontRightSpeed);
  setMotorSpeed(motorBackLeft, backLeftSpeed);
  setMotorSpeed(motorBackRight, backRightSpeed);
  
  getDistance();
}

// Fonction utilitaire pour régler la vitesse d’un moteur
void setMotorSpeed(AF_DCMotor &motor, float speed) {
  if (speed > 0) {
    motor.setSpeed(speed * maxSpeed);
    motor.run(FORWARD);
  } else if (speed < 0) {
    motor.setSpeed(-speed * maxSpeed);
    motor.run(BACKWARD);
  } else {
    motor.run(RELEASE);
  }
}

// Fonction pour arrêter tous les moteurs
void stopMotors() {
  motorFrontLeft.run(RELEASE);
  motorFrontRight.run(RELEASE);
  motorBackLeft.run(RELEASE);
  motorBackRight.run(RELEASE);
}


void turnAround() {
  // Faire tourner sur place les roues dans des directions opposées
  motorFrontLeft.run(FORWARD);
  motorFrontRight.run(BACKWARD);
  motorBackLeft.run(FORWARD);
  motorBackRight.run(BACKWARD);

  // Régler la vitesse
  motorFrontLeft.setSpeed(maxSpeed);
  motorFrontRight.setSpeed(maxSpeed);
  motorBackLeft.setSpeed(maxSpeed);
  motorBackRight.setSpeed(maxSpeed);

  // Attendre suffisamment de temps pour compléter le demi-tour
  delay(1000); // Ajuste ce délai en fonction des capacités de ton robot

  // Arrêter les moteurs après le demi-tour
  stopMotors();
}

