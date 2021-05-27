from __future__ import division 
# --- Repositry Imports ---

#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library.
import time # mporting Time for access to countdown and pause breaks.
import serial
import os # Allows direct terminal commands
import json
import os.path # Used to check if a file exists
import pandas as pd # Pandas is a mathmatics libary - in this case used for it's extensive CSV library
import Adafruit_PCA9685 # Imports a library to control motor functions - servo controller.

from termcolor import colored

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=.2)

# --- File Name ---
bottle_file_check = (os.path.isfile('bottle_data.csv')) # Used to check if a file exists (returns True or False)
config_file_check = os.path.isfile('config.json') # Used to check if a file exists (returns True or False)
print(bool(bottle_file_check)) # DEBUG printing check result (bottle data) ([bool]ean as the previous lines return a True or False argument)
print(bool(config_file_check)) # DEBUG printing check result (config data)

# ----- Testing Area -----
    
# - Credits/ Opening Debug Screen/ Flash Screen -
def credits(c_status):
    os.system('clear') # Clears the screen - (for debugging and code display)
    if c_status==1: # are credits activated? "1" = TRUE
        print(colored("Smell Synth.", "cyan", attrs=['bold']))
        time.sleep(1)
        print("Designed & Programmed by Elliott Hall\n")
        print("Portfolio - www.elliotthall.co.uk")
        print("Email - hello@elliotthall.co.uk \n")
        coloured("#################################### \n", 'cyan')
        time.sleep(1)
    else:
        print("Smell Synth. \n")

def print_red(red_message):
    print(colored(red_message, 'red'))

def print_yellow(yellow_message):
    print(colored(yellow_message, 'yellow'))

def print_red_bold(red_message):
    print(colored(red_message, 'red', attrs=['bold']))

def debug_warning(message):
    debug_message = ('\n - *** ' + message + ' ***\n')
    print_red_bold(debug_message)
    # print_red(debug_message)

def debug_amber_warning(message):
    debug_message = ('\n - *** ' + message + ' ***\n')
    print_yellow(debug_message)
    # print_red(debug_message)

def debug_logging(message, color):
    #def color_logging(message, color):
    #    print(colored(message, color))
    logging_message = ('\n - *** ' + message + ' ***\n')
    #print_red_bold(debug_message)
    # print_red(debug_message)
    print(colored(logging_message, color))

def debug_complete(message):
    #def color_logging(message, color):
    #    print(colored(message, color))
    complete_message = (' - ' + message + '\n')
    #print_red_bold(debug_message)
    # print_red(debug_message)
    print(colored(complete_message, 'green'))

def coloured(message, color):
    print(colored(message, color))

def coloured_bold(message, color):
    print(colored(message, color, attrs=['bold']))

def file_create_config():
    temp_number_bottles = 10
    temp_max_bottles = 16
    temp_use_defaults = True
    temp_warning_level = 15

    debug_amber_warning("Would you like to setup the config file?")

    print(colored('------------------------------------\n Defaults:\n------------------------------------\n', 'cyan'), 'Number of Bottles:', temp_number_bottles,'\n Maximum Bottles:', temp_max_bottles,'\n (IGNORE) Defaults Overide :', temp_use_defaults,'\n Refill Level Warning :', temp_warning_level, colored('\n------------------------------------', 'cyan'))
    print(' type "Y" to setup, or "N" to use defaults.\n')
    config_y_n = input(' [Y/N] : ')

    if config_y_n == 'Y' or config_y_n == 'y':
        while config_y_n != 'done':# or config_y_n != 'DONE':
            if config_y_n == 'DONE':
                break
            #print(config_y_n)
            print(colored('\n\n------------------------------------\n Select Option:\n------------------------------------\n', 'cyan'), '1. Number of Bottles\n 2. Maximum Bottles\n 3. (IGNORE) Defaults Overide\n 4. Refill Warning Level\n', colored('------------------------------------', 'cyan'))
            config_y_n = input(' [1/2/3/4/DONE] : ')
            if config_y_n == '1':
                error_check_a = 1
                while error_check_a != 0:
                    print('\n Enter new value for "Number of bottles":')
                    print(' Enter an intiger between 0 and', temp_max_bottles, '(Maximum Bottles)')
                    temp_number_bottles = input(' : ')
                    if int(temp_number_bottles) > 0 and int(temp_number_bottles) <= int(temp_max_bottles):
                        print(colored('\n Number of bottles is now:', 'green'), colored(temp_number_bottles, 'green'))
                        error_check_a = 0
                    else:
                        debug_warning(' Your input was not between the range, Try again.')
                        time.sleep(1)
                        pass
            if config_y_n == '2':
                error_check_a = 1
                while error_check_a != 0:
                    print('\n Enter new value for "MAXIMUM Number of bottles":')
                    print(' Enter an intiger above 0.')
                    temp_max_bottles = input(' : ')
                    if int(temp_max_bottles) > 0:
                        print(colored('\n MAXIMUM number of bottles is now:', 'green'), colored(temp_max_bottles, 'green'))
                        error_check_a = 0
                    else:
                        debug_warning(' Your input was not above 0, Try again.')
                        time.sleep(1)
                        pass
            if config_y_n == '3':
                error_check_a = 1
                while error_check_a != 0:
                    print('\n Enter new value for "Use Default":')
                    print(' Enter "True" or "False" (case sensetive)')
                    temp_use_defaults = input(' : ')
                    if temp_use_defaults == 'True' or temp_use_defaults == 'False':
                        print('\n Use Defaults? is now set to:', str(temp_use_defaults))
                        error_check_a = 0
                    else:
                        debug_warning(' Your input was not valid, Try again.')
                        time.sleep(1)
                        pass
            if config_y_n == '4':
                error_check_a = 1
                while error_check_a != 0:
                    print('\n Enter new value for "Liquid Refill Warning Level":')
                    print(' Enter an intiger above 0.')
                    temp_warning_level = input(' : ')
                    if int(temp_warning_level) > 0:
                        print(colored('\n MAXIMUM number of bottles is now:', 'green'), colored(temp_warning_level, 'green'))
                        error_check_a = 0
                    else:
                        debug_warning(' Your input was not above 0, Try again.')
                        time.sleep(1)
                        pass
            else:
                #debug_warning(" You've not made a valid input, Try again.")
                print('\n')
                pass
    else:
        pass

    config_values = (int(temp_number_bottles), int(temp_max_bottles), bool(temp_use_defaults), int(temp_warning_level))

    config_data = pd.Series(config_values, index=['number_bottles', 'max_bottles', 'use_default', 'refill_warning_level'])
    coloured("- New Config Values Have Been Updated", 'green')
    coloured('------------------------------------\n New Values:\n------------------------------------', 'cyan')
    print(config_data)
    coloured('------------------------------------\n', 'cyan')

    config_data.to_json('config.json')

# - Motor Fuctions / Driver / Controls

# // Motor Variables 
pwm = Adafruit_PCA9685.PCA9685() # Initialise the PCA9685 using the default address (0x40).

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 525  # Max pulse length out of 4096

pwm.set_pwm_freq(60) # Set frequency to 60hz, good for servos.

def set_servo_pulse(channel, pulse): # - Thanks to Tony DiCola for this def function (set_servo_pulse) - License: Public Domain
    # Helper function to make setting a servo pulse width simpler.
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def motor_trigger(scent_servo_ID):
    global servo_min
    global servo_max
    pwm.set_pwm(scent_servo_ID, 0, servo_min)
    time.sleep(0.25)
    pwm.set_pwm(scent_servo_ID, 0, servo_max)

# - Liquid Level Motitoring -
def levels_check(c_status, bottle_file_check):
    #os.system('clear') # Clears the screen - (for debugging and code display)

    coloured('------------------------------------', 'cyan')
    coloured('Beginning Liquid Level Check Process', 'cyan')
    coloured('------------------------------------\n', 'cyan')

    if config_file_check == False: # or bottle_file_check == True:
        debug_warning("No config data found!")
        time.sleep(1)
        file_create_config()
        pass
    #levels_check(c_status, bottle_file_check)
    else:
        time.sleep(1)
        print(' - Loading Config Data from "config.json"\n')
        with open('config.json') as f:
            config_data = json.load(f)
        time.sleep(1)
        coloured('------------------------------------\n Config Data\n------------------------------------', 'cyan')
        print(' Number of Bottles', config_data['number_bottles'])
        print(' Maximum Bottles', config_data['max_bottles'])
        print(' Use Default?', config_data['use_default'])
        print(' Refill Warning Level', config_data['refill_warning_level'])
        coloured('-------------------------------------\n', 'cyan')
        debug_complete('Config File check complete')
        time.sleep(1)

    if bottle_file_check == False: # or bottle_file_check == True:
        debug_warning("No levels data found!")
        time.sleep(1)
        file_create_levels()
        pass
        #levels_check(c_status, bottle_file_check)
    else:
        if c_status==1: # is this check activated? "1" = TRUE
            time.sleep(1)
            print(' - Loading Bottle Data from "bottle_data.csv"\n')
            time.sleep(1)
            bottle_data = pd.read_csv('bottle_data.csv', index_col=0)
            coloured('------------------------------------\n Bottle Data\n------------------------------------', 'cyan')
            print(bottle_data)
            coloured('------------------------------------\n', 'cyan')
            debug_complete('Bottle Data File check complete')
            time.sleep(1)
        else:
            coloured('-------------------------------------', 'red')
            coloured('Liquid Level Check Process - DISABLED', 'red')
            coloured('-------------------------------------\n', 'red')
            time.sleep(1)

def file_create_levels():
    with open('config.json') as f:
        config_data = json.load(f)
    config_number_bottles = config_data['number_bottles']

    servo_id = 0
    bottle_id = 1
    default_level = 43

    coloured(' - Creating New Levels Data ', 'green')
    print(colored("\n USER INPUT REQUIRED:\n, attrs=['bold']") + "Enter the name of the Smell for the\n corresponding bottle_id's.\n")

    print('    Bottle ID: ', bottle_id)
    coll_1 = input('    Smell: ')
    coll_2 = servo_id
    coll_3 = default_level

    first_row = {'scent_name': [coll_1],
            'servo_id': [coll_2],
            'l_levels': [coll_3]
            }

    bottle_data = pd.DataFrame(data=first_row, columns = ['scent_name', 'servo_id', 'l_levels'])
    bottle_data.index = bottle_data.index + 1
    bottle_data.index.name = 'bottle_id'

    #print(bottle_data)

    for x in range(config_number_bottles - 1):

        servo_id = servo_id + 1
        bottle_id = bottle_id + 1

        print('\n   Bottle ID:', bottle_id)
        coll_1 = input('    Smell: ')
        coll_2 = servo_id
        coll_3 = default_level

        new_row = {'scent_name': coll_1,
                'servo_id': coll_2,
                'l_levels': coll_3
                }

        bottle_data = bottle_data.append(new_row, ignore_index=True)
        bottle_data.index = bottle_data.index + 1
        bottle_data.index.name = 'bottle_id'

        #print(bottle_data)

    bottle_data.to_csv('bottle_data.csv')

    # DEBUG this reloads the CSV file after writing to for DEBUG referencing (if statement for automatic cross comparison could be applied here?)
    bottle_data_new = pd.read_csv('bottle_data.csv', index_col=0)
    # print(bottle_data_new)

    #true_check = bottle_data.equals(bottle_data_new)
    #print(true_check)

    if bottle_data.equals(bottle_data_new) == True:
        debug_complete('New Data written successfully!')
    else:
        debug_warning('Error Writing New Bottle Data')

    print('\n', bottle_data, '\n')


def bottle_level_update(bottle_id): # This section runs a program that takes an input of a bottle_ID, reads its current value from a CSV file, removes 1 from it's value (representing a spray), then rewrites the CSV with the updated value.

    bottle_data = pd.read_csv('bottle_data.csv', index_col=0) # This loads the data from the CSV as a table assigning it the name 'bottle_data'

    #print (bottle_data) # DEBUG displays the CSV file as a table to enable cross comparison
    #print('\n')

    levels_check_bottle_id = bottle_data.at[bottle_id,'l_levels'] # This line creates a variable from looking up the value corrolating to the bottle ID under the 'l_levels' in the CSV table
    levels_check_bottle_scent = bottle_data.at[bottle_id,'scent_name'] #This line finds the Bottle_ID's scent name - (i.e wood, sweet, etc.)
    scent_servo_ID = bottle_data.at[bottle_id,'servo_id'] #This line finds the Servo_ID for the scent - (i.e wood, sweet, etc.)

    # This line prints the description and values of the bottle about to be updated
    print(colored('------------------------------------\n Level Check\n------------------------------------\n', 'cyan'), 'Bottle ID:', bottle_id, '\n Scent:', levels_check_bottle_scent, '\n Level:', levels_check_bottle_id, '\n Servo ID:', scent_servo_ID)
    
    # This removes 1 from the previous value
    levels_check_bottle_id = levels_check_bottle_id - 1

    # This line prints the new value of the bottle (how much liquid is left)
    print(colored('------------------------------------', 'cyan'))
    print(colored(' New Level:', 'green'), levels_check_bottle_id, colored('\n------------------------------------\n', 'cyan'))

    # This replaces the Value at the orginal location with the updated level
    bottle_data.at[bottle_id,'l_levels']=levels_check_bottle_id

    # This resaves the CSV file overwriting the orginal values
    bottle_data.to_csv('bottle_data.csv')

    # DEBUG this reloads the CSV file after writing to for DEBUG referencing (if statement for automatic cross comparison could be applied here?)
    bottle_data_new = pd.read_csv('bottle_data.csv', index_col=0)
    # print(bottle_data_new)

    #true_check = bottle_data.equals(bottle_data_new)
    #print(true_check)

    if bottle_data.equals(bottle_data_new) == True:
        debug_complete('New Data written successfully!')
    else:
        print(colored(' - *** Error Writing Updated Value - Bottle_ID =', 'red'), colored(bottle_id, 'red'), colored(' ***', 'red'))

def spray_trigger(bottle_id):
    with open('config.json') as f:
        config_data = json.load(f)
    warning_level = config_data['refill_warning_level']
    bottle_data = pd.read_csv('bottle_data.csv', index_col=0)
    scent_name = bottle_data.at[bottle_id,'scent_name']
    scent_servo_ID = bottle_data.at[bottle_id,'servo_id']
    l_level = bottle_data.at[bottle_id,'l_levels']
    if l_level <= warning_level+1:
        if l_level > 0:
            l_level = l_level-1
            debug_amber_warning('Low Level Warning')
            # LOW LEVEL WARNING - ATTENTION
            # Trigger Amber Light
            print(' -',scent_name,'is running low.', l_level, 'remaining.\n')
            print(' - Spray Bottle', bottle_id, '(', scent_name, ') has been triggered\n')
            #temp_confirmation = str('Spray Bottle', bottle_id, '(', scent_name, ') has been triggered')
            #debug_complete(temp_confirmation)
            bottle_level_update(bottle_id)
            motor_trigger(scent_servo_ID)
            debug_complete('End of "def spray_trigger"')
        elif l_level <= 0:
            empty_warning = ('The Bottle "' + scent_name + '" is EMPTY')
            debug_warning(empty_warning)
            #debug_warning('This Bottle is now EMPTY')
            #print('Bottle:', scent_name)
            # Trigger Error Light RED - ATTENTION
        else:
            debug_warning('Error (spray_trigger - else)')
    else:
        print('\n - Spray Bottle', bottle_id, '(', scent_name, ') has been triggered\n')
        bottle_level_update(bottle_id)
        motor_trigger(scent_servo_ID)
        debug_complete('End of "def spray_trigger"')

# --- Program Start ---

credits(1) # Enables Credits on the debug screen 
debug_complete('Credits Complete')
levels_check(1, bottle_file_check) # Checks the liquid levels based off estimated date (0 = off / 1 = on)
debug_complete('Levels Check Complete')
line = ser.readline().decode('utf-8').rstrip()
debug_complete('begin_boot sent')
while line != 'Boot Confirmed':
    ser.write(b"begin_boot\n")
    line = ser.readline().decode('utf-8').rstrip()

ser.flushOutput()
debug_complete(line)

#time.sleep(1)

while line != 'warning_check_complete':
    ser.write(b"warning_config\n")
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    #time.sleep(2)

debug_complete(line)

# ser.write(b"warning_config\n")
# debug_complete('warning_config')

if __name__ == '__main__':
    ser.flush()
    while True:
        #ser.write(b"Hello from Raspberry Pi!\n")
        line = ser.readline().decode('utf-8').rstrip()
        #print(line)
        #time.sleep(0.5)
        if line == 'left':
            spray_trigger(1)
            print('1')

        elif line == 'right':
            spray_trigger(2)
            print('2')

        elif line == 'up':
            spray_trigger(3)
            print('3')

        elif line == 'down':
            spray_trigger(4)
            print('4')

        elif line == 'select':
            spray_trigger(5)
            print('5')

        #elif line == 'select':
        #    spray_trigger(5)
        #    print('5')

        else:
            #print('_')
            z = 'z'
            
            

while True:
    #debug_logging("levels check", 'green')
    bottle_choice = input('Pick a smell: ')
    spray_data = pd.read_csv('bottle_data.csv', index_col=1)
    debug_testing = spray_data.at[bottle_choice,'bottle_id']
    spray_trigger(debug_testing)
    #bottle_level_update(3)
    #print('Levels Update Complete')


# Create a manual - design task
# Create a randomised 'enviroment combination' selection [using elimination to ensure all are viewed before repeating]
# Take inspiration from black mirror. - some really intresting distopian concepts can arise from this combination of thinking!

# CODE TASKS

# - Create a menu navigation system
# - A Data Ingest System
# - A format to read back the enviroments [punch cards coceptualy]
# - A folder searching system to read and list options
# - Create an LED [traffic light], status identification system
# - Projecting Image and Video output (how?, what format?, Storage anf retieval / database options)
# - Refil option. - reload empty cartrige - maybe even skip any that are empty.
# - Scan feature, to scan the full length of each program to give a final time out come - spray usage - how many loops till empty
# - Physical/software interface to button Input and screen Output.

# - platformio remote agent start