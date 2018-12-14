import datetime
import pickle
import subprocess as sp


class Item(object):
    def __init__(self, count, text):
        self.timestamp = datetime.datetime.now()
        self.count = count
        self.elapsed_time = None
        self.text = text

    def set_elapsed_time(self):
        self.elapsed_time = datetime.datetime.now() - self.timestamp

    def __str__(self):
        return '{} {} {} {}'.format(
            self.timestamp.strftime('%H:%M:%S'),
            self.count,
            '0:00:00' if self.elapsed_time is None else str(self.elapsed_time).split('.')[0],
            self.text)


class Items(object):
    def __init__(self, max_size=100, pickle_path=None):
        self.items = []
        self.max_size = max_size
        self.pickle_path = pickle_path
        self.count = 0  # items added today only

    def print_to_console(self):
        index = 0
        for i in self.items:
            print index, i
            index += 1

    def simple_print(self):
        index = 0
        for i in self.items:
            print index, i.text
            index += 1

    def remove(self, i):
        try:
            if not isinstance(i, (int, long)):
                i = int(i)
            return self.items.pop(i)
        except:
            print 'Failed to remove at index {}'.format(i)

    def process_line(self, line):
        self.count += 1
        i = Item(self.count, line)
        self.add(i)

    def add(self, i):
        if len(self.items) > 0:
            self.items[-1].set_elapsed_time()
        self.items.append(i)
        if self.max_size is not None:
            if len(self.items) > self.max_size:
                self.items.pop(0)

    def undo(self):
        # TODO implement so it can undo everything
        del self.items[-1]


    def pickle_list(self):
        if self.pickle_path is not None:
            f = open(self.pickle_path, 'wb')
            pickle.dump(self.items, f)
            f.close()

    def unpickle_list(self):
        if self.pickle_path is not None:
            f = open(self.pickle_path, 'rb')
            self.items = pickle.load(f)
            f.close()


focus = Items(100,'focus.pkl')
notes = Items(100,'notes.pkl')
todos = Items(None,'todos.pkl')
realizations = Items(None,'realizations.pkl')

try:
    focus.unpickle_list()
except IOError:
    pass
try:
    notes.unpickle_list()
except IOError:
    pass
try:
    todos.unpickle_list()
except IOError:
    pass
try:
    realizations.unpickle_list()
except IOError:
    pass


def handleUI(ui):
    # items are preceded by nothing ; : or /
    # commands are single letters p or d
    # d is followed by index number
    if ui[0] == ';':
        # focus
        if len(ui) == 2 and ui == ';p':
            focus.print_to_console()
            return
        elif len(ui) == 2 and ui == ';u':
            focus.undo()
        elif len(ui) > 3 and ui[:2] == ';d':
            toks = ui.split(' ')
            focus.remove(toks[1])
        else:
            focus.process_line(ui)
        focus.print_to_console()
    elif ui[0] == ':':
        # todos
        if len(ui) == 2 and ui == ':p':
            todos.simple_print()
            return
        elif len(ui) > 3 and ui[:2] == ':d':
            toks = ui.split(' ')
            todos.remove(toks[1])
        else:
            todos.process_line(ui)
        todos.simple_print()
    elif ui[0] == '/':
        # realizations
        if len(ui) == 2 and ui == '/p':
            realizations.simple_print()
            return
        elif len(ui) > 3 and ui[:2] == '/d':
            toks = ui.split(' ')
            realizations.remove(toks[1])
        else:
            realizations.process_line(ui)
        realizations.simple_print()
    else:
        # notes
        if len(ui) == 1 and ui == 'p':
            notes.simple_print()
            return
        elif len(ui) > 2 and ui[0] == 'd':
            toks = ui.split(' ')
            notes.remove(toks[1])
        else:
            notes.process_line(ui)


while True:
    ui = raw_input('>')

    if ui == '':
        continue

    if len(ui) == 1 and ui == 'q':
        focus.pickle_list()
        todos.pickle_list()
        realizations.pickle_list()
        notes.pickle_list()
        break

    if ui == 'cls':
        tmp = sp.call('cls', shell=True)
        continue

    handleUI(ui)




