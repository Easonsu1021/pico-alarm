from machine import *
from pico_i2c_lcd import *
import utime
import ws2812b



I2C_ADDR     = 63
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1))
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#initialize light off
lcd.backlight_off()

#alarm
set_hour = 20
set_minute = 59
# for detect the alarm 
alarm_check = 1

#buzz alarm setting
buzzPin = 9
buzz = PWM(Pin(buzzPin))

#button
bn = Pin(3,Pin.IN,Pin.PULL_DOWN)

#lcd
numpix = 8
strip = ws2812b.ws2812b(numpix, 0, 2)


def blink():
    while True:
        rainbow()
        utime.sleep(0.1)
        strip.fill(0, 0, 0)
        strip.show()
        utime.sleep(0.1)
        if bn.value() == 1:
            utime.sleep(0.05)
            buzz.duty_u16(0)
            strip.fill(0, 0, 0)
            strip.show()
            lcd.backlight_off()
            global alarm_check
            alarm_check = 0
            break
        
def rainbow():
    strip.set_pixel(0, 139, 0, 0)
    strip.set_pixel(1, 255, 0, 0)
    strip.set_pixel(2, 255, 140, 0)
    strip.set_pixel(3, 255, 255, 0)
    strip.set_pixel(4, 0, 255, 0)
    strip.set_pixel(5, 0, 0, 255)
    strip.set_pixel(6, 75, 0, 130)
    strip.set_pixel(7, 128, 0, 128)
    strip.show()


def alarm():
    buzz.freq(523)

def show_time():
    t = utime.localtime()
    date = "{:<d}/{:0>2d}/{:0>2d}   \n".format(t[0],t[1],t[2])
    time = "{:0<2d}:{:0>2d}:".format(t[3],t[4])
    
    lcd.putstr(date)
    lcd.putstr((time+"{:0>2d}".format(t[5])+'\n'))
    
    return t[3] , t[4]

while True:
    hour, minute = show_time()
    # background light up when push button if is not the alarm time
    if (set_hour != hour) and (set_minute != minute) and bn.value() == 1:
        utime.sleep(0.05)
        lcd.backlight_on()
        utime.sleep(3)
        lcd.backlight_off()
    #alarm_check
    if(set_hour != hour) and (set_minute != minute) and (alarm_check == 0):
        alarm_check = 1
    #alarm
    if(set_hour == hour) and (set_minute == minute) and (alarm_check == 1):
        lcd.backlight_on()
        buzz.duty_u16(60000)
        alarm()
        blink()
