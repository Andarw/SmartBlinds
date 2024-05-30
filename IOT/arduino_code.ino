#include<avr/io.h>

#define ANALOG_PIN_A0 0 // we use analog pin 0 to read the values for the voltage sensor
#define ADC_VREF_TYPE 0x40 // AVCC with external capacitor at RFPIN
#define MIN_PULSE_WIDTH  544  // the shortest pulse sent to a servo
#define MAX_PULSE_WIDTH  2400 // the longest pulse sent to a servo 
#define BAUD_RATE 9600

enum class Positon{ // class to bind the inputs of the developer to certain values to protect the hardware
  CLOSED = 50,
  PART_OPEN = 110,
  OPEN = 140
};

void setServoPosition(Positon servoPosition) {

  // Map the degrees to the pulse width (1000 to 2000 microseconds)
  // Calculate pulse width using linear interpolation(fancy words for substituting a value by another using the servo specification :) )
  uint16_t pulse_width = MIN_PULSE_WIDTH + (uint16_t)((uint32_t)servoPosition * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) / 180);

  // Convert pulse width to ticks (16-bit value)
  uint16_t ticks = pulse_width * 2; // Since the timer operates at 2 MHz (16 MHz / 8 prescaler)

  // Set the pulse width
  OCR1A = ticks; // Output Compare Register 1 A, we set the value in ticks that will be compared to the counter value in TCNT1(configured earlyer), this will generate a waveform output on the OC1B pin.
  // which is also maped as the PB2 pin on the AtMega328P and to digital pin 9 on the arduino shield
}

void initTimer0() {

    //set timer 0 into CTC mode by placing 1 into WGM01.  all others are zero
    TCCR0A &= ~(1 << WGM00);  // 0
    TCCR0A |= (1 << WGM01);   // 1 , WGM00(0) and WGM01(1) Clear OC0A on compare match
    TCCR0B &= ~(1 << WGM02);  // 0 , WGM02(0) combined with the previous WGM00 and WGM01 place timer 0 in CTC(clear timer on compare match) mode 

    TCCR0B |= (1 << CS00); // 1
    TCCR0B |= (1 << CS01); // 1
    TCCR0B &= ~(1 << CS02);// 0 set the clock with prescaler 64(CS02(0),CS01(1),CS00(1)) and OCR0A = 249(next line), this tells the hardware to what value to count to, this value is obtained as OCR0A = 16 MHz / (64 x 1 kHz) - 1
    OCR0A = 249;
  // the setings enable the timer to count 1 us, enableing us to implement delay
}

void delayMs(unsigned int delay)
{
    unsigned int count = 0;
 
    TIFR0 |= (1 << OCF0A);  // set the counter flag down

    TCNT0 = 0;  // clear the count register

    // enter a loop to compare count with delay value needed
    while (count < delay)
      {
      if (TIFR0 & (1 << OCF0A))
        { 
        //increment every time the timer raises a flag (counting 1 us flags)
        count++;
        TIFR0 |= (1 << OCF0A);  //set timer to start counting again
        }
      }
}

unsigned int read_adc()
{

ADMUX = ANALOG_PIN_A0 | ADC_VREF_TYPE; // We set ADC Multiplexer Selection Register with the appropriate settings

// Start the AD conversion
ADCSRA |= 0x40; // Set ADC Control and Status Register A as 0x40 which sets ADSC: (ADC Start Conversion) to HIGH

// Wait for the AD conversion to complete
while ((ADCSRA & 0x10)==0); // We wait for ADIF: (ADC Interrupt Flag) to change to 1, this signals the completion of the conversion

ADCSRA |= 0x10;// For safety reasons we set ADIF to 1, while we handle the result of the conversion

return ADCW; // We return the value of the register that holds the result of the conversion on 16 bits ADCW(ADCH|ADCL)

}

// Floats for ADC voltage & Input voltage
float adc_voltage = 0.0; // analog to digital voltage
float in_voltage = 0.0; // reference voltage
 
// // Floats for resistor values in divider (in ohms)
float R1 = 30000.0;
float R2 = 7500.0; 
 
// // Float for Reference Voltage
float ref_voltage = 5.0;
 
// Integer for ADC value
int adc_value = 0;
 
void setup(){

  DDRC = 0xFE; // Set DDRC0 on 0 to make the A0 pin an input pin, as this is an input pin we leave the portC reg not set(Its default is 0)
  DDRB = 0x2; // Set DDRB5 to 1 to make the 9 pin as output pin, pin 9 also coresponds to PWM specification
  initTimer0();

  TCCR1A = (1 << COM1A1) | (1 << WGM11); // Clear OC1A on compare match
  TCCR1B = (1 << WGM13) | (1 << WGM12) | (1 << CS11); // Mode 14(FAST PWM), Prescaler 8

  ICR1 = 39999; // 16MHz / (8 50Hz) - 1, we set the TOP value for the PWM generation using the frequency of the microcontroller (16Mhz), the prescaler value we set earlyer (8) and the frequency at which the Servo Motor SG90 operates (50 Hz)

  Serial.begin(BAUD_RATE); // we set the Baud_rate for the Serial communication, not bare metal as it is used for debuging pourpouses
}

void loop(){
  // Read the Analog Input
  adc_value = read_adc();
  
  // Determine voltage at ADC input
  adc_voltage  = (adc_value * ref_voltage) / 1024.0;
  
  // Calculate voltage at divider input
  in_voltage = adc_voltage*(R1+R2)/R2;

  Serial.println(in_voltage, 2);

    delayMs(5000);

}