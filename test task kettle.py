import configparser
import logging
import sys
import time
from threading import Thread

import keyboard

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='main.log',
    filemode='w')

config = configparser.ConfigParser()
config.read("setup.ini")
# создаём объекта парсера для получения данных из файла конфигурации

STOP_KEY = config['Kettle']['stop_key']
STOP_MESSAGE = f'press {STOP_KEY} to stop the program'


def check_exit() -> None:
    """Added second stream in programm
       for keyboard interrupt opportunity.
    """
    print(STOP_MESSAGE)
    while True:
        if keyboard.is_pressed(STOP_KEY):
            print('', 'kettle program stopped', sep='\n')
            sys.exit()


class Kettle:
    """Kettle behavior imitation."""

    def water_amount(self) -> str:
        """Asking amount of water to pour."""

        min_ammount = float(config['Kettle']['min_ammount'])
        max_ammount = float(config['Kettle']['max_ammount'])

        while True:
            try:
                amonut = float(
                    input('How much water to pour?'
                          f'From {min_ammount} to {max_ammount}: ')
                )
            except ValueError:
                logging.exception('wrong input, expected a float number')
                print('wrong input, expected a float number')
                continue
            if amonut < min_ammount or amonut > max_ammount:
                logging.info('incorrect water amount')
                print(f'you can pour from {min_ammount} to {max_ammount} liters')
                continue
            logging.info(f'poured {amonut} liters')
            print(f'Poured {amonut} liters')
            break

    def turn_on_question(self) -> str:
        """Decision to turn on a kettle."""
        while True:
            question = input('Wanna start boiling? yes/no: ')
            if question == 'yes':
                logging.info('kettle turned on')
                print('Kettle turned on')
                return True
            elif question == 'no':
                logging.info('a kettle wasnt turned on, program stopped')
                print('Ok, see you soon :)')
                return False
            else:
                logging.info('wrong input')
                print('Wrong input, expected yes or no')
                continue

    def boiling(self) -> str:
        """Boiling water process."""
        temperature = 0
        boiling_time = int(config['Kettle']['boiling_time'])  # default = 10
        boiling_temperature = int(config['Kettle']['boiling_temperature'])  # default = 100
        one_sec = 1

        while temperature <= boiling_temperature:
            logging.info(f'temperature: {int(temperature)} °C')
            print(f'temperature: {int(temperature)} °C')
            time.sleep(one_sec)
            temperature += boiling_temperature/boiling_time
        print(f'temperature: {int(boiling_temperature)} °C')
        logging.info('water boiled, kettle turn off')
        print('Done! water boiled', 'Kettle turn off', sep='\n')


def main() -> None:
    """Main function for program."""
    kettle = Kettle()
    kettle.water_amount()
    if kettle.turn_on_question():
        kettle.boiling()


thread1 = Thread(target=check_exit, daemon=False)
thread1.start()
thread2 = Thread(target=main, daemon=True)
thread2.start()
