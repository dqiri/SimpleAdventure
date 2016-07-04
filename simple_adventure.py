import sys

def choicesMaker(choices, choice):
    assert(len(choices) != 0)
    assert(choice > 0 and choice <= len(choices))
    return choices[choice - 1][0]

def parseScript(script):
    parsed = {}

    scriptfile = open(script, 'r')

    #print "Parsing", scriptfile.name

    line = scriptfile.readline()
    while line:
        if line[-1] == '\n':
            line = line[:-1]
        line = line.split(';')

        if len(line) < 3:
            print "Each line should consist of the following: label, content, next..."
            raise AssertionError
        if line[0] in parsed:
            print line[0], "already points to previous content", parsed[line[0]]
            raise AssertionError
        choicesParsed = []
        for cp in line[2:]:
            choicelabel, choicecontent = cp.split('|')
            choicesParsed.append([choicelabel, choicecontent])
        """               [content, [choiceslabel, choicecontent]]"""
        line[1] = line[1].split('\\n')
        line[1] = '\n'.join(line[1])
        parsed[line[0]] = [line[1], choicesParsed]
        line = scriptfile.readline()
    return parsed

def playGame(parsed, start, choicename="What do you do?"):
    ptr = start

    print "Game has started. To end, type KILL at anytime"
    while True:
        choices = parsed[ptr][1]

        print parsed[ptr][0]
        print '\n'
        if len(choices) == 1:
            print choices[0][1], "    Press Enter to Continue..."
        else:
            print choicename
            for i, p in enumerate(parsed[ptr][1]):
                p = p[1]
                print "{}. {}".format(i + 1, p)

        correct = False
        while not correct:
            try:
                x = raw_input()
                if x == "KILL":
                    break
                if len(choices) == 1:
                    choice = choices[0][0]
                else:
                    choice = choicesMaker(choices, int(x))
                correct = True
            except:
                print "Please retry your choice. Use only the numbers and hit enter"
                print x
        if x == "KILL":
            return
        ptr = choice
        print '======================'

def main():
    usage = "python %s <script_name>" % sys.argv[0]
    if len(sys.argv) != 2:
        print 'Please provide the script to play'
        print usage
        return

    x = sys.argv[1]

    parsed = parseScript(x)
    playGame(parsed, 'start')

if __name__ == "__main__":
    main()
