import sys
import getopt


def string_insert(ori, index, text):
    str_list = list(ori)
    str_list.insert(index, text)
    return ''.join(str_list)


def help(code=0):
    print('subtitle_generator.py -s1 -e0 -btimer --text "SAMPLE TEXT"')
    exit(code)


startTick = 1
endTick = 0
text = ''
step = 2

entry = 't0'
scoreboard = 'm.'
doAddRegion = False

try:
    opts, args = getopt.getopt(sys.argv[1:], 's:e:b:hr', ['text=', 'step='])
except getopt.GetoptError:
    help(-1)

for opt, arg in opts:
    if opt == '-s':
        startTick = int(arg)
    elif opt == '-e':
        entry = arg
    elif opt == '-b':
        scoreboard = arg
    elif opt == '--text':
        text = arg
    elif opt == '--step':
        step = int(arg)
    elif opt == '-r':
        doAddRegion = True
    elif opt == '-h':
        help()

if text == '':
    print('Option "--text" is necessary.')
    sys.exit(-2)

base = 'execute if score %s %s matches {tick} run title @a subtitle "{text}"\n' % (
    entry, scoreboard)

build_text = ''

with open('output.mcfunction', 'w', encoding='utf-8') as output:
    if doAddRegion:
        output.write('#region %d..%d %s\n' %
                     (startTick, startTick + len(text) * step, text))
    for char in text:
        build_text += char
        output.write(base.format(tick=startTick,
                                 text=string_insert(build_text, len(build_text) - 1, '\u00a77')))
        startTick += step
    output.write(base.format(tick=startTick, text=text))
    if doAddRegion:
        output.write('#endregion\n')
