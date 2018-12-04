import datetime
import pickle


class Message(object):
    def __init__(self, count, text):
        self.timestamp = datetime.datetime.now()
        self.count = count
        self.elapsed_time = None
        self.text = text

    def set_elapsed_time(self):
        self.elapsed_time = datetime.datetime.now() - self.timestamp

    def __str__(self):
        return '{} {} {} did: {}'.format(
            self.timestamp.strftime('%H:%M:%S'),
            self.count,
            '0:00:00' if self.elapsed_time is None else str(self.elapsed_time).split('.')[0],
            self.text)


class Note(object):
    def __init__(self, text):
        self.timestamp = datetime.datetime.now()
        self.text = text

    def __str__(self):
        return '{} {} {}'.format(self.timestamp.date(), self.timestamp.strftime('%H:%M:%S'), self.text)


messages = []
count = 0
timestamp = None
time_diff = datetime.datetime.now()
todos = []
realizations = []


try:
    f = open('messages.pkl', 'rb')
    messages = pickle.load(f)
    f.close()
    print 'loaded messages'
    f = open('todos.pkl', 'rb')
    todos = pickle.load(f)
    f.close()
    print 'loaded todos'
    f = open('realizations.pkl', 'rb')
    realizations = pickle.load(f)
    f.close()
    print 'loaded realizations'
except Exception as e:
    print 'failed to load'


def pickle_lists():
    f = open('messages.pkl', 'wb')
    pickle.dump(messages, f)
    f.close()

    f = open('todos.pkl', 'wb')
    pickle.dump(todos, f)
    f.close()

    f = open('realizations.pkl', 'wb')
    pickle.dump(realizations, f)
    f.close()


def print_todos():
    i = 0
    while i < len(todos):
        print '{}. {}'.format(i, todos[i])
        i += 1


def print_realizations():
    i = 0
    while i < len(realizations):
        print '{}. {}'.format(i, realizations[i])
        i += 1


def delete_realizations(i):
    try:
        realizations.pop(i)
    except Exception as e:
        print e.message


def delete_todo(i):
    try:
        todos.pop(i)
    except Exception as e:
        print e.message


while True:
    ui = raw_input('>')

    if ui == '': continue
    if len(messages) > 100:
        messages.pop(0)
    if ui[0] == ';': # note taking
        messages.append(Note(ui))
    elif ui[0] == '/': # realization
        if len(ui) >= 2 and ui[:2] == '/p':
            print_realizations()
            continue
        if len(ui) > 3:
            if ui[:2] == '/d':  # remove realization
                try:
                    i = int(ui.split(' ')[1])
                    text = realizations[i]
                    delete_realizations(i)
                    print_realizations()
                    print 'deleted', text
                except Exception as e:
                    print 'syntax error', e.message

                continue
            else:
                realizations.append(Note(ui))
                messages.append(ui)
    elif ui[0] == ':':
        # :d 23 would delete item number 23
        if len(ui) >= 2 and ui[:2] == ':p':
            print_todos()
            continue
        if len(ui) >=2 and ui[:2] == ':q':
            pickle_lists()
            break
        if len(ui) >=2 and ui[:2] == ':u':
            del messages[-1]

        if len(ui) > 3:
            if ui[:2] == ':d':
                try:
                    i = int(ui.split(' ')[1])
                    text = todos[i]
                    delete_todo(i)
                    print_todos()
                    print 'deleted', text
                except Exception as e:
                    print 'syntax error', e.message

                continue

            else:
                todos.append(ui)
        messages.append(ui)
    else:
        count += 1
        for m in reversed(messages):
            if isinstance(m, Message):
                m.set_elapsed_time()
                break
        messages.append(Message(count, ui))
    for message in messages:
        print message

