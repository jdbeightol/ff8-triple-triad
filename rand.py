#!/usr/bin/env python3

class RandomNumberGenerator():
    def __init__(self, data):
        self.data = data
        self.cursor = 0

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index-1]

    def getRandom(self):
        return next()

    def seek(self, position):
        self.cursor = position

    def next(self):
        r = self.data[self.cursor]
        self.cursor += 1
        return r

def load(filename):
    with open(filename, 'rb') as dat_file:
        return RandomNumberGenerator(dat_file.read())
