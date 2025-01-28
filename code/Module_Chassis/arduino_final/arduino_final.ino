#include <Servo.h>
#include <AFMotor.h>

AF_DCMotor motorFrontLeft(1);
AF_DCMotor motorFrontRight(3);
AF_DCMotor motorBackLeft(2);
AF_DCMotor motorBackRight(4);
Servo myServo;   

const int led = 10;
const int buzzer =  9;
const int echoPin = 2;   
const int trigPin = 7;  
const int servoPin = 5;
int maxSpeed = 255;
int vitesse;
int angle = 0;
bool si_obstacle;
bool si_actif;
bool si_sonner;
bool si_scanner = 0;
int dodge_strategy = 0;

bool interruption_en_cours = false;             // Indique si on gère l'interruption
long distance = 0 ;
                    //AF_DCMotor moteur(4); 
                    //moteur.setSpeed(i);
                    //moteur.run(BACKWARD);
                    //moteur.run(FORWARD); 
                    //myservo.attach(10);
                    //myservo.write(pos);
void setup() {
  pinMode(buzzer,OUTPUT);
  pinMode(led, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  Serial.begin(9600);
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
     vitesse = command.substring(0, firstComma).toInt();      // Vitesse
     angle = command.substring(firstComma + 1, secondComma).toInt();    // Angle
     si_obstacle = command.substring(secondComma + 1, thirdComma).toInt();  // Si obstacle
     si_actif = command.substring(thirdComma + 1, fourthComma).toInt();   // Si actif
     si_sonner = command.substring(fourthComma + 1).toInt();      // Si sonner

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
  //logique pour arreter de  sonner
  digitalWrite(buzzer,LOW);
}

void stopMotors() {
      int stop_speed = 80;
        motorFrontLeft.setSpeed(stop_speed);
        motorFrontRight.setSpeed(stop_speed);
        motorBackLeft.setSpeed(stop_speed);
        motorBackRight.setSpeed(stop_speed);
}

void stopTotal() {
      int stop_speed = 0;
        motorFrontLeft.setSpeed(stop_speed);
        motorFrontRight.setSpeed(stop_speed);
        motorBackLeft.setSpeed(stop_speed);
        motorBackRight.setSpeed(stop_speed);
}

void scan_initial(){
    int scan_speed = 250;
    int scan_delay = 100;

    motorFrontLeft.setSpeed(scan_speed);
    motorFrontRight.setSpeed(scan_speed);
    motorBackLeft.setSpeed(scan_speed);
    motorBackRight.setSpeed(scan_speed);

    while(true){
        Serial.println("je suis dans le while");
        String receivedString = Serial.readStringUntil('\n');
                    // Parse the received string
        parseCommand(receivedString);

        if(angle > 85 && angle < 95){
              return;
        }
        motorFrontLeft.run(FORWARD);
        motorFrontRight.run(BACKWARD);
        motorBackLeft.run(FORWARD);
        motorBackRight.run(BACKWARD);

        delay(scan_delay);
        stopMotors();
    }   
    si_scanner = 1;
}

void turnLeft(){
        motorFrontLeft.run(FORWARD);
        motorFrontRight.run(BACKWARD);
        motorBackLeft.run(FORWARD);
        motorBackRight.run(BACKWARD);
        delay(100);
}

void turnRight(){
        motorFrontLeft.run(BACKWARD);
        motorFrontRight.run(FORWARD);
        motorBackLeft.run(FORWARD);
        motorBackRight.run(BACKWARD);
        delay(100);
}

void eviterObstacle(){
  // logique pour eviter un obstacle
      int dodge_speed = 250;
      int dodge_delay = 50;
      int compteur = 0;

      
      motorFrontLeft.setSpeed(dodge_speed);
      motorFrontRight.setSpeed(dodge_speed);
      motorBackLeft.setSpeed(dodge_speed);
      motorBackRight.setSpeed(dodge_speed);
        Serial.println("on esquive ");
      while(true){
          if(si_obstacle){ 
                if(dodge_strategy == 0){
                          Serial.println("a gauche ");
                      motorFrontLeft.run(FORWARD);
                      motorFrontRight.run(BACKWARD);
                      motorBackLeft.run(BACKWARD);
                      motorBackRight.run(FORWARD);
                }else{
                          Serial.println("a droite ");
                      motorFrontLeft.run(BACKWARD);
                      motorFrontRight.run(FORWARD);
                      motorBackLeft.run(FORWARD);
                      motorBackRight.run(BACKWARD);
                }
              getDistance();
              if (distance > 10){
                  si_obstacle = 0;
              }
          }
          dodge_strategy = !dodge_strategy;
          rouler();
          return;
      }
      
}

void getDistance() {
    digitalWrite(trigPin, LOW);
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

void rouler(){
          String receivedString = Serial.readStringUntil('\n');
          parseCommand(receivedString);

          while( angle > 95 || angle < 85 ) {
              if(angle > 95){
                  turnLeft();
              }     
              if(angle < 5){
                  turnRight();
              }    
          }
        
          motorFrontLeft.setSpeed(maxSpeed);
          motorFrontRight.setSpeed(maxSpeed);
          motorBackLeft.setSpeed(maxSpeed);
          motorBackRight.setSpeed(maxSpeed);
          motorFrontLeft.run(FORWARD);
          motorFrontRight.run(FORWARD);
          motorBackLeft.run(FORWARD);
          motorBackRight.run(FORWARD); 
}


void finish(){
    digitalWrite(led, HIGH);
    sonner();
    delay(1000);
    digitalWrite(led, LOW);
    stop_sonner();
    delay(1000);
}

void loop() {
    if (Serial.available() > 0) {
                  Serial.print("la serial available");
                            // Read the entire line from serial
        String receivedString = Serial.readStringUntil('\n');
                            // Parse the received string
        parseCommand(receivedString);
    
        if (si_sonner){
                  Serial.print("sonner ");
            sonner();
        }else{
                  Serial.print("arreter de sonner ");
            stop_sonner();
        }            
        if (si_actif){
                  Serial.print("si c'est actif ");
            if(! si_scanner){
                  Serial.print(" ca doit scanner ");
                  scan_initial();
            }
            rouler();
                  Serial.print(" ca roule ");
            if (distance < 10){
                stopTotal();
                  Serial.print("arreter les moteurs ");
                if(si_obstacle){
                  Serial.print("eviter l'obstacle ");
                    eviterObstacle();
                }
                if(! si_obstacle){
                  Serial.print(" c'est terminer ");
                    finish();
                }
            }
        }
    }
}
