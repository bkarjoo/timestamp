import datetime

messages = []
count = 0

while True:
    ui = raw_input('>')
    if ui == '': continue
    if len(messages) > 100:
        messages.pop()
    timestamp = datetime.datetime.now()
    count += 1
    messages.append('{} {}  {}'.format(timestamp, count, ui))
    for message in messages: print message
