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

void loop() {
  // globalement ce code fait un suiveur
  myServo.write(90);
  int distance = getDistance();
  if (distance > 50) {
      moveForward(255);
      delay(300);
  }else{
       stopMotors(); 
  }

}