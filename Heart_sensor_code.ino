#include <Wire.h>
#include "MAX30100_PulseOximeter.h"

#define REPORTING_PERIOD_MS     1000

PulseOximeter pox;
uint32_t tsLastReport = 0;

// Callback (this runs every time a pulse is detected)
void onBeatDetected() {
    Serial.println("Beat! ❤️");
}

void setup() {
    Serial.begin(115200);
    
    // This part is the "secret sauce" for the MAX30100
    // It turns on internal pull-ups for SDA (21) and SCL (22)
    pinMode(21, INPUT_PULLUP);
    pinMode(22, INPUT_PULLUP);
    
    Serial.print("Initializing pulse oximeter..");

    Wire.begin(21, 22);

    if (!pox.begin()) {
        Serial.println("FAILED");
        for(;;);
    } else {
        Serial.println("SUCCESS");
    }
    pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop() {
    // Make sure to call update as fast as possible
    pox.update();

    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        Serial.print("Heart rate:");
        Serial.print(pox.getHeartRate());
        Serial.print("bpm / SpO2:");
        Serial.print(pox.getSpO2());
        Serial.println("%");

        tsLastReport = millis();
    }
}