import datetime

messages = []
count = 0
timestamp = None
time_diff = datetime.datetime.now()


class Message(object):
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


class Note(object):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


while True:
    ui = raw_input('>')
    if ui == '': continue
    if len(messages) > 100:
        messages.pop(0)
    if ui[0] == ';': # note taking
        messages.append(Note(ui))
    else:
        count += 1
        for m in reversed(messages):
            if isinstance(m, Message):
                m.set_elapsed_time()
                break
        messages.append(Message(count, ui))
    for message in messages:
        print message

