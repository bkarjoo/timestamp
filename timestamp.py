import datetime

messages = []
count = 0
timestamp = None
time_diff = datetime.datetime.now()

while True:
    ui = raw_input('>')
    if ui == '': continue
    if ui[0] == ';': # note taking
        for message in messages: print message
        print ui
        continue
    if len(messages) > 100:
        messages.pop()
    previous = timestamp
    timestamp = datetime.datetime.now()
    count += 1
    if previous is not None:
        time_diff = timestamp - previous
    messages.append('{} {} {} {}'.format(timestamp.strftime('%H:%M:%S'), count, str(time_diff).split('.')[0], ui))
    for message in messages: print message
