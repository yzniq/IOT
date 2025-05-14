import os
from bottle import Bottle, template, run
from gpiozero import MCP3008
import time

# Настройки
moisture_channel = 0  # канал MCP3008 для датчика влажности
adc = MCP3008(moisture_channel)

app = Bottle()

def read_soil_moisture():
    try:
        value = adc.value  # значение от 0.0 (влажно) до 1.0 (сухо)
        percentage = (1 - value) * 100  # преобразуем в проценты сухости
        return round(percentage, 1)
    except Exception as e:
        print(f"Ошибка чтения датчика влажности: {e}")
        return None

@app.route('/')
def index():
    moisture_percent = read_soil_moisture()
    return template("index.html", moisture=moisture_percent, threshold=threshold * 100)

@app.route("/threshold", method="POST")
def set_threshold():
    new_threshold = request.forms.get("threshold")
    try:
        new_threshold = float(new_threshold) / 100  #преобразуем из процентов
        global threshold
        threshold = new_threshold
    except ValueError:
        pass
    control_irrigation(threshold)
    return template("index.html", moisture=read_soil_moisture(), threshold=threshold * 100)

if __name__ == "__main__":
    run(app, host='0.0.0.0', port=8080)