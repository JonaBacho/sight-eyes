#include <Servo.h>

// Pins pour les moteurs
const int MotorA1 = 12;
const int MotorA2 = 13;
const int ENA = 11;
const int MotorB1 = 9;
const int MotorB2 = 10;
const int ENB = 8;

// Pins pour le capteur à ultrasons
const int trigPin = 6;
const int echoPin = 7;

// Servo-moteur
Servo myServo;
const int servoPin = 5;

// Variables pour le suivi de l'obstacle
long minDistance = 9999;
int bestAngle = 0; // Angle du servo vers l'obstacle

void setup() {
  // Configurer les pins des moteurs
  pinMode(MotorA1, OUTPUT);
  pinMode(MotorA2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(MotorB1, OUTPUT);
  pinMode(MotorB2, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Configurer les pins du capteur à ultrasons
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Configurer le servo-moteur
  myServo.attach(servoPin);
  myServo.write(0); // Initialiser le servo à la position centrale

  // Initialiser la communication série
  Serial.begin(9600);
}


void loop() {
  // globalement ce code fait un suiveur
  // If there is data in the serial buffer
  if (Serial.available() > 0) {
    // Read the entire line from serial
    String receivedString = Serial.readStringUntil('\n');
    
    // Parse the received string
    parseAndProcessCommand(receivedString);
  }

}


// Fonction pour mesurer la distance
long getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Calculer la durée du signal réfléchi
  long duration = pulseIn(echoPin, HIGH);

  // Convertir la durée en distance (en cm)
  long distance = duration * 0.034 / 2;
  return distance;
}

// Fonction pour scanner avec le servo
int scanForObstacle() {
  minDistance = 99;
  bestAngle = 0;

  for (int angle = 0; angle <= 180; angle += 1) { // Balayage par pas de 15°
    myServo.write(angle);
    delay(10); // Attendre que le servo atteigne la position

    long distance = getDistance();

    // Mettre à jour si un obstacle plus proche est trouvé
    if (distance > 0 && distance < minDistance) {
      minDistance = distance;
      bestAngle = angle;

    }
  }
      return bestAngle;
}

// Commandes de base
// fonction pour se deplacer vers l'avant
void moveForward(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(MotorA1, HIGH);
  digitalWrite(MotorA2, LOW);
  digitalWrite(MotorB1, HIGH);
  digitalWrite(MotorB2, LOW);
}
// fonction pour se deplacer vers l'arriere
void moveBackward(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(MotorA1, LOW);
  digitalWrite(MotorA2, HIGH);
  digitalWrite(MotorB1, LOW);
  digitalWrite(MotorB2, HIGH);
}
// fonction pour se deplacer vers la gauche
void turnLeft(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(MotorA1, LOW);
  digitalWrite(MotorA2, HIGH);
  digitalWrite(MotorB1, HIGH);
  digitalWrite(MotorB2, LOW);
}
// fonction pour se deplacer vers la droite
void turnRight(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(MotorA1, HIGH);
  digitalWrite(MotorA2, LOW);
  digitalWrite(MotorB1, LOW);
  digitalWrite(MotorB2, HIGH);
}
// fonction pour arreter les moteurs
void stopMotors() {
  digitalWrite(ENA, LOW);
  digitalWrite(ENB, LOW);
}

// Fonction pour ajuster la direction et poursuivre l'obstacle
void pursueObstacle(int angle, long distance) {
  if (distance > 20) { // Obstacle éloigné
    if (angle < 85) { // Obstacle à gauche
      turnLeft(150);
      delay(300);
    } else if (angle > 95) { // Obstacle à droite
      turnRight(150);
      delay(300);
    } else { // Obstacle droit devant
      moveForward(150);
    }
  } else { // Obstacle trop proche
    moveBackward(150);
    delay(300);
    stopMotors();
  }
}


// Function to parse and process the received command
void parseAndProcessCommand(String command) {
  // Split the command into parts
  int firstComma = command.indexOf(',');
  int secondComma = command.lastIndexOf(',');
  
  // Check if we have a valid command with two commas
  if (firstComma != -1 && secondComma != -1 && firstComma != secondComma) {
    // Extract speed
    int speed = command.substring(0, firstComma).toInt();
    
    // Extract angle
    int angle = command.substring(firstComma + 1, secondComma).toInt();
    
    // Extract boolean (convert to true/false)
    bool activeState = (command.substring(secondComma + 1) == "1");
    
    // Optional: Add your specific logic here based on the received values
  move(speed,angle,activeState);
}

// Function that blinks the internal LED a given number of times
void move(int speed, int angle, bool activeState) {
      // Debug print the received values
    Serial.print("Speed: ");
    Serial.print(speed);
    Serial.print(", Angle: ");
    Serial.print(angle);
    myServo.write(angle);
    Serial.print(", Active: ");
    Serial.println(activeState ? "True" : "False");
  }
}
