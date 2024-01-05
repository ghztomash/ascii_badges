
from machine import ADC, Pin
from picographics import PicoGraphics
import micropython
import time

# Constants for automatic brightness adjustment.
# Below about 3/8ths, the backlight is entirely off. The top of the range is OK.
BACKLIGHT_LOW = micropython.const(0.45)
BACKLIGHT_HIGH = micropython.const(1.0)

# The luminance sensor seems to cover the whole 16-bit range pretty well from
# buried in shadow to bright phone torch in its face, but setting a lower high
# point will make it generally bias brighter in calm room lighting, and a higher
# low will use the darkest backlight without needing to completely hard-mask the
# sensor in complete darkness.
LUMINANCE_LOW = micropython.const(384)
LUMINANCE_HIGH = micropython.const(2048)  # 65535 to use the full range.

# If on battery, and the supply voltage drops below this, force minimum
# backlight brightness.
# The bottom of the Tufty2040 input range is 3.0v, so values below that likely
# will not trigger before it cuts out.
LOW_BATTERY_VOLTAGE = micropython.const(3.1)
EMPTY_BATTERY_VOLTAGE = micropython.const(2.5)
FULL_BATTERY_VOLTAGE = micropython.const(3.7)

CONVERSION_FACTOR = micropython.const(3.3 / (65535))

# Pins and analogue-digital converters we need to set up to measure sensors.
lux_vref_pwr = Pin(27, Pin.OUT)
lux = ADC(26)
vbat_adc = ADC(29)
vref_adc = ADC(28)
temp_adc = ADC(4)
usb_power = Pin(24, Pin.IN)

# Returns a tuple of the raw luminance value, and the brightness to now use.
def auto_brightness(previous: float) -> (float, float):
    luminance = lux.read_u16()
    luminance_frac = max(0.0, float(luminance - LUMINANCE_LOW))
    luminance_frac = min(1.0, luminance_frac / (LUMINANCE_HIGH - LUMINANCE_LOW))
    backlight = BACKLIGHT_LOW + (luminance_frac * (BACKLIGHT_HIGH - BACKLIGHT_LOW))
    # Use the previous value to smooth out changes to reduce flickering.
    # The "32" value here controls how quickly it reacts (larger = slower).
    # The rate at which the main loop calls us also affects that!
    backlight_diff = backlight - previous
    backlight = previous + (backlight_diff * (1.0 / 16.0))
    return (luminance, backlight)


# Returns a tuple of voltage (fake value if on USB), "is on USB", and "is low".
def measure_battery() -> (float, bool, bool):
    if usb_power.value():
        return (5.0, True, False)

    # See the battery.py example for how this works.
    vdd = 1.24 * (65535 / vref_adc.read_u16())
    vbat = ((vbat_adc.read_u16() / 65535) * 3 * vdd)

    low_battery = False
    if vbat < LOW_BATTERY_VOLTAGE:
        low_battery = True

    return (vbat, False, low_battery)

def battery_percentage(vbat: float) -> int:
    # Map the battery voltage to a percentage.
    if vbat < EMPTY_BATTERY_VOLTAGE:
        return 0
    if vbat > FULL_BATTERY_VOLTAGE:
        return 100

    percentage = 100 * ((vbat - EMPTY_BATTERY_VOLTAGE) / (FULL_BATTERY_VOLTAGE - EMPTY_BATTERY_VOLTAGE))
    if percentage > 100:
        percentage = 100
    if percentage < 0:
        percentage = 0

    return int(percentage)

def measure_temperature() -> float:
    # See the temperature.py example for how this works.
    vtemp = temp_adc.read_u16() * CONVERSION_FACTOR
    return 27 - (vtemp - 0.706) / 0.001721

class TuftyBoard:
    def __init__(self, display):
        self.display = display
        self.backlight = BACKLIGHT_LOW
        self.luminance = LUMINANCE_LOW
        self.vbat = LOW_BATTERY_VOLTAGE
        self.on_usb = False
        self.low_battery = False
        self.bat_percent = 0
        self.fps = 0.0
        self.temp = 0.0
        self.last_frame_time = time.ticks_ms() / 1000.0
    
    def tick(self):
        # Turn on VREF and LUX only while we measure things.
        lux_vref_pwr.value(1)
        (self.vbat, self.on_usb, self.low_battery) = measure_battery()
        self.bat_percent = battery_percentage(self.vbat)
        if self.on_usb:
            self.backlight = BACKLIGHT_HIGH
        elif self.low_battery:
            self.backlight = BACKLIGHT_LOW
        (self.luminance, self.backlight) = auto_brightness(self.backlight)
        lux_vref_pwr.value(0)

        self.temp = measure_temperature()

        # Set the new backlight value.
        self.display.set_backlight(self.backlight)

        # Calculate time difference
        current_time = time.ticks_ms() / 1000.0
        delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        # Calculate frames per second
        self.fps = 1.0 / (delta_time + 1e-10)

    def get_battery(self):
        return (self.vbat, self.on_usb, self.low_battery)

    def get_brightness(self):
        return (self.luminance, self.backlight)

    def get_battery_percentage(self):
        return self.bat_percent

    def get_fps(self):
        return self.fps

    def draw_fps(self, scale=1):
        if not self.on_usb:
            return
        self.display.text("fps: {:.2f}".format(self.fps), 0, 0, scale=scale)
    
    def get_temperature(self):
        return self.temp