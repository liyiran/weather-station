import datetime
import json
import os
import subprocess

import time
from PIL import ImageFont
from oled.device import ssd1306
from oled.render import canvas
from oled.serial import i2c

serial = i2c(port=1, address=0x3c)
device = ssd1306(serial)
ttf = '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf'
font60 = ImageFont.truetype(ttf, 60)
font42 = ImageFont.truetype(ttf, 42)
font36 = ImageFont.truetype(ttf, 36)
font20 = ImageFont.truetype(ttf, 20)
font12 = ImageFont.truetype(ttf, 12)
delay = 1
zero_c = -273.15


def displayTemp(temp, temp_low, temp_high):
    length = 20
    with canvas(device) as c:
        c.text((20, 0), temp + u"\u00B0", font=font60, fill=255)
        c.text((20 + length, 0), temp_low + u"\u00B0", font=font60, fill=255)
        c.text((60 + length + length, 0), temp_high + u"\u00B0", font=font60, fill=255)
    time.sleep(delay)


def main():
    print("Weather station started")

    while True:
        basedir = os.path.dirname(os.path.realpath(__file__))
        updateFile = os.path.join(basedir, 'update_tick')
        icondir = os.path.join(basedir, 'icons')
        try:
            if os.path.isfile(updateFile):
                print("Update file found, calling weather-update")
                with canvas(device) as drawUpdate:
                    drawUpdate.text((0, 0), "Updating...", font=font20, fill=255)
                subprocess.call([os.path.join(basedir, 'wunderground-update.sh')])
                print("Deleting update file")
                os.unlink(updateFile)

            with open(os.path.join(basedir, 'open-weather-conditions-data.json')) as conditions_data_file:
                conditions_data = json.load(conditions_data_file)

            with open(os.path.join(basedir, 'open-weather-forecast-data.json')) as forecast_data_file:
                forecast_data = json.load(forecast_data_file)

            temp_num = "{:10.2f}".format(float(conditions_data['main']['temp']) + zero_c)
            temp_min = "{:10.2f}".format(float(conditions_data['main']['temp_min']) + zero_c)
            temp_max = "{:10.2f}".format(float(conditions_data['main']['temp_max']) + zero_c)

            # icon = str(conditions_data[u'current_observation'][u'icon'])
            humidity = conditions_data['main'][humidity]
            wind = str(conditions_data['wind']['speed'])
            wind_dir = str(conditions_data['wind']['deg'])
            # gust = str(conditions_data[u'current_observation'][u'wind_gust_kph'])

            # icon_today = str(forecast_data[u'forecast'][u'simpleforecast'][u'forecastday'][0][u'icon'])
            # high_today = str(forecast_data[u'forecast'][u'simpleforecast'][u'forecastday'][0][u'high'][u'celsius'])
            # low_today = str(forecast_data[u'forecast'][u'simpleforecast'][u'forecastday'][0][u'low'][u'celsius'])
            # epoch = int(conditions_data[u'current_observation'][u'local_epoch'])
            # utime = time.strftime('%H:%M', time.localtime(epoch))

            # logo = Image.open(os.path.join(icondir, icon + ".bmp"))
            # logoToday = Image.open(os.path.join(icondir, icon_today + ".bmp"))

            print(temp_num)
            print(temp_min)
            print(temp_max)

            # print(icon)
            # print(icon_today)
            # print(high_today)

            displayTemp(temp_num, temp_min, temp_max)

            # with canvas(device) as drawFeelslike:
            #     drawFeelslike.text((10, 8), feelslike_str + u"\u00B0", font=font42, fill=255)
            # time.sleep(delay)
            # 
            # displayTemp(temp_cur)
            # 
            # with canvas(device) as drawHigh:
            #     drawHigh.text((10, 8), u"\u2191  " + high_today + u"\u00B0", font=font42, fill=255)
            # time.sleep(delay)
            # 
            # displayTemp(temp_cur)
            # 
            # with canvas(device) as drawLow:
            #     drawLow.text((10, 8), u"\u2193  " + low_today + u"\u00B0", font=font42, fill=255)
            # time.sleep(delay)
            # 
            # displayTemp(temp_cur)
            # 
            # with canvas(device) as drawHumidity:
            #     drawHumidity.text((20, 8), humidity, font=font42, fill=255)
            # time.sleep(delay)
            # 
            # displayTemp(temp_cur)
            # 
            # with canvas(device) as drawWind:
            #     drawWind.text((0, 0), wind, font=font36, fill=255)
            #     drawWind.text((55, 0), u"\u2191" + gust, font=font36, fill=255)
            #     drawWind.text((40, 40), wind_dir, font=font20, fill=255)
            # time.sleep(delay)
            # 
            # displayTemp(temp_cur)

            # with canvas(device) as drawLogo:
            #     drawLogo.bitmap((32, 0), logo, fill=1)
            #     drawLogo.text((0, 0), "Now:", font=font12, fill=255)
            # time.sleep(delay)
            # 
            # displayTemp(temp_cur)
            # 
            # with canvas(device) as drawForecastLogo:
            #     drawForecastLogo.bitmap((32, 0), logoToday, fill=1)
            #     drawForecastLogo.text((0, 0), "Today:", font=font12, fill=255)
            # time.sleep(delay)

            # displayTemp(temp_cur)
            # 
            # with canvas(device) as drawTime:
            #     now = datetime.datetime.now()
            #     drawTime.text((10, 8), "%02d" % now.hour + ":" + "%02d" % now.minute, font=font42, fill=255)
            # time.sleep(delay)
        except:
            with canvas(device) as drawError:
                drawError.text((0, 0), "Error!", font=font20, fill=255)
                drawError.text((0, 40), time.strftime('%H:%M', time.localtime(epoch)), font=font20, fill=255)
            os.mknod(updateFile)
            time.sleep(30)


if __name__ == "__main__":
    main()
