#!/usr/bin/env python3
# coding: utf-8
import os
import sys
import datetime

LOG_FILE = 'tt.csv'

def add_entry(log, last_time):
    current_time = datetime.datetime.now()
    minutes = round((current_time - last_time).total_seconds() / 60)
    task = input('Enter task: ')
    if ',' in task:
        task = '"{}"'.format(task)
    log.write('{minutes:d},{task}\n'.format(
        task=task,
        minutes=int(minutes),
    ))
    return current_time


INPUT_FUNCTIONS = {
    'a': add_entry,
}


def parse_input(input, log, last_time, input_functions):
    try:
        return input_functions[input](log, last_time)
    except KeyError:
        print('Unknown action.')


def get_prompt(input_functions):
    prompt = 'Please enter action [{}/x]: '.format('/'.join([k for k, v in input_functions.items()]))
    return prompt


def main(log_file, input_functions):
    last_time = datetime.datetime.now()
    if not os.path.exists(log_file):
        with open(log_file, 'w') as log:
            log.write('minutes,task\n')
    with open(log_file, 'a') as log:
        while True:
            s = input(get_prompt(input_functions))
            if s == 'x':
                break
            last_time = parse_input(s, log, last_time, input_functions)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        LOG_FILE = sys.argv[1]
    main(LOG_FILE, INPUT_FUNCTIONS)