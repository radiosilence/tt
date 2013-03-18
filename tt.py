#!/usr/bin/env python3
# coding: utf-8
import os
import sys
import datetime
import csv

LOG_FILE = 'log.csv'

def display_entries(log, last_time, current_task):
    with open(log, 'r') as f:
        c = csv.reader(f)
        for row in c:
            print(' - '.join(row))

def save_current(log, last_time, current_task):
    current_time = datetime.datetime.now()
    minutes = round((current_time - last_time).total_seconds() / 60)
    with open(log, 'a') as f:
        c = csv.writer(f)
        c.writerow([datetime.date.today(), minutes, current_task])
    return current_time


def new_entry(log, last_time, current_task):
    task = input('Enter new task: ')
    return save_current(log, last_time, current_task), task


INPUT_FUNCTIONS = {
    'n': new_entry,
    'd': display_entries,
}


def parse_input(input, log, last_time, current_task, input_functions):
    try:
        return input_functions[input](log, last_time, current_task)
    except KeyError:
        print('Unknown action.')


def get_prompt(input_functions):
    prompt = 'Please enter action [{}/x]: '.format('/'.join([k for k, v in input_functions.items()]))
    return prompt


def main(log, input_functions):
    last_time = datetime.datetime.now()
    current_task = input('Enter current task: ')
    print('Options: [n]ew task, [d]isplay log, e[x]it\n')
    if not os.path.exists(log):
        with open(log, 'w') as f:
            c = csv.writer(f)
            c.writerow(['date', 'minutes', 'task'])
    while True:
        s = input(get_prompt(input_functions))
        if s == 'x':
            save_current(log, last_time, current_task)
            break
        last_time, current_task = parse_input(
            s,
            log,
            last_time,
            current_task,
            input_functions
        ) or (last_time, current_task)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        LOG_FILE = sys.argv[1]
    main(LOG_FILE, INPUT_FUNCTIONS)
