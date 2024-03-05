import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Setup for LED and MCP3008 ADC
LED_PIN = 11
LIGHT_SENSOR_CHANNEL = 0  # Assuming you've connected the light sensor to channel 0
SOUND_SENSOR_CHANNEL = 1  # Assuming you've connected the sound sensor to channel 1
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)

# MCP3008 setup
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def blink_led(times, interval):
    """Blink LED on and off."""
    for _ in range(times):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(interval)

def read_light_sensor(duration, interval):
    """Read light sensor values and determine brightness."""
    end_time = time.time() + duration
    LIGHT_THRESHOLD = 500  # Example threshold, adjust based on your experimentation
    while time.time() < end_time:
        value = mcp.read_adc(LIGHT_SENSOR_CHANNEL)
        if value > LIGHT_THRESHOLD:
            print(f"{value} - bright")
        else:
            print(f"{value} - dark")
        time.sleep(interval)

def read_sound_sensor(duration, interval):
    """Read sound sensor values and detect taps."""
    end_time = time.time() + duration
    SOUND_THRESHOLD = 700  # Example threshold, adjust based on your experimentation
    while time.time() < end_time:
        value = mcp.read_adc(SOUND_SENSOR_CHANNEL)
        print(value)
        if value > SOUND_THRESHOLD:
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.1)  # LED on for 100ms
            GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(interval)

try:
    while True:
        # Step 1: Blink LED 4 times with 500ms intervals
        blink_led(4, 0.5)
        
        # Step 2: Read light sensor for 5 seconds
        read_light_sensor(5, 0.1)
        
        # Step 3: Blink LED 10 times with 200ms intervals
        blink_led(10, 0.2)
        
        # Step 4: Read sound sensor for 5 seconds
        read_sound_sensor(5, 0.1)
finally:
    GPIO.cleanup()  # Clean up GPIO to ensure a clean exit
