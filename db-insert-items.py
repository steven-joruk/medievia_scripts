#!/usr/bin/env python3

import re

# TODO: height, weight, age, *vuln

class Affect:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        print('Created Affect({}, {})'.format(name, value))

class Modifier:
    def __init__(self, name, typ, value):
        self.name = name
        self.typ = typ
        self.value = value
        print('Created Modifier({}, {}, {})'.format(name, typ, value))

class Item:
    pattern = re.compile(r'(.*) - Lev\((\d+)\) Loc\((\w+)\) (.*)')
    affects = []
    flags = []
    modifiers = []
    name = ''
    level = 0
    location = ''

    AFFECT_NAMES = [
        'armor', 'bluntvuln', 'con', 'dex', 'dr', 'holyvuln', 'hps', 'hr',
        'infcle', 'infmage', 'infmel', 'int', 'litvuln', 'mana', 'srod',
        'ss', 'sta', 'str', 'wis', 'AC-ap'
    ]

    # Don't capture no-auction, nostore, nodrop
    FLAG_NAMES = [
        'AC', 'AE', 'AG', 'AM', 'AT', 'AW', 'BSER', 'DAG', 'fragile', 'noegg', 'nounegg'
    ]

    def __init__(self, line):
        self.parse(line)

    def extract_affect(self, name, line):
        m = re.match(name + r'\((\d)\)', line)
        if m:
            self.affects.append(Affect(name, m.group(1)))

    def extract_affects(self, line):
        for name in self.AFFECT_NAMES:
            self.extract_affect(name, line)

    def extract_dice(self, line):
        if not self.location == 'wield':
            raise 'Trying to extract dice for an incompatible item location'

    def extract_flags(self, line):
        for name in self.FLAG_NAMES:
            if line.find(name):
                self.flags.append(name)

    def extract_modifiers(self, line):
        # SKL/SPL: Name (type value%)[ ...]
        pass

    def extract_spells(self, line):
        # 5xBolt of Lightning
        pass

    def extract_toxins(self, line):
        if not self.type == 'toxin':
            raise 'Trying to extract toxin from an incompatible type'

        # Toxin: INF_MAGE(-10, 3 ticks) INF_CLERIC(-10, 3 ticks) Imbues(12 ticks)

    def parse(self, line):
        m = self.pattern.match(line)
        if not m:
            return False

        self.name = m.group(1)
        self.level = m.group(2)
        self.location = m.group(3)
        other = m.group(4)

        if self.location == 'wield':
            self.extract_dice(other)

        self.extract_affects(other)
        self.extract_flags(other)
        self.extract_modifiers(other)
        self.extract_spells(other)

        if self.type == 'toxin':
            self.extract_toxin(other)

        return True

with open('items.log') as f:
    for line in f:
        item = Item(line)
