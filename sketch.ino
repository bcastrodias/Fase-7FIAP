#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Definição de pinos
#define BUTTON_K_PIN 14   // Pino do botão para Potássio (K)
#define BUTTON_P_PIN 27   // Pino do botão para Fósforo (P)
#define DHT_PIN 4         // Pino de dados do DHT22
#define DHT_TYPE DHT22    // Tipo de sensor DHT
#define LED_PIN 18        // Pino para o LED (indica rega)
#define DEBOUNCE_DELAY 50 // Tempo de debounce em milissegundos

// Escalas para K e P no gráfico
const int SCALE_K = 50;
const int SCALE_P = 75;

// Inicialização do sensor DHT e do LCD
DHT dht(DHT_PIN, DHT_TYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Estados dos nutrientes no solo
bool isKPresent = false;
bool isPPresent = false;

// Estados dos botões
bool lastButtonKState = HIGH, lastButtonPState = HIGH;
bool currentButtonKState = HIGH, currentButtonPState = HIGH;

unsigned long lastDebounceTimeK = 0, lastDebounceTimeP = 0;
unsigned long lastUpdateTime = 0;

void setup() {
  Serial.begin(115200); // Inicializa o monitor serial

  // Configura os pinos
  pinMode(BUTTON_K_PIN, INPUT_PULLUP);
  pinMode(BUTTON_P_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);

  // Inicializa dispositivos
  dht.begin();
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Inicializando...");
  delay(2000);
  lcd.clear();
}

void loop() {
  // Verifica os botões
  checkButton(BUTTON_K_PIN, isKPresent, currentButtonKState, lastButtonKState, lastDebounceTimeK);
  checkButton(BUTTON_P_PIN, isPPresent, currentButtonPState, lastButtonPState, lastDebounceTimeP);

  // Atualização periódica do LCD e Serial Plotter
  if (millis() - lastUpdateTime >= 2000) {
    lastUpdateTime = millis();
    updateSensorsAndDisplay();
  }
}

void updateSensorsAndDisplay() {
  // Lê a umidade
  float humidity = dht.readHumidity();

  // Verifica erro no sensor
  if (isnan(humidity)) {
    updateLCD("Erro DHT", "Verificar!");
    return;
  }

  // Determina o status de rega
  String regaStatus = (humidity < 30.0) ? "Regando" : "OK";
  digitalWrite(LED_PIN, (humidity < 30.0) ? HIGH : LOW);

  // Atualiza o LCD
  updateLCD(
    "Umidade: " + String(humidity, 1) + "%",
    "K:" + String(isKPresent ? "1" : "0") +
    " P:" + String(isPPresent ? "1" : "0") + " " + regaStatus
  );

  // Envia dados ao Serial Plotter
  sendToSerialPlotter(humidity, isKPresent, isPPresent);
}

void checkButton(int buttonPin, bool &nutrientState, bool &currentState, bool &lastState, unsigned long &lastDebounceTime) {
  int reading = digitalRead(buttonPin);

  // Gerencia debounce
  if (reading != lastState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY && reading != currentState) {
    currentState = reading;
    if (currentState == LOW) {
      nutrientState = !nutrientState;
    }
  }

  lastState = reading;
}

void updateLCD(const String &line1, const String &line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

void sendToSerialPlotter(float humidity, bool kPresent, bool pPresent) {
  Serial.print("plot:");
  Serial.print(humidity);  // Umidade
  Serial.print(", ");
  Serial.print(kPresent ? SCALE_K : 0); // Escala de K
  Serial.print(", ");
  Serial.println(pPresent ? SCALE_P : 0); // Escala de P
}
