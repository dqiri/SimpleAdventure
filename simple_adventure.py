import sys

def choicesMaker(choices, choice):
    """This is a helper function that returns a label/key
    for the `parsed` dictionary.
        @param choices list of choices that you can make
        @param choice int of the choice you want to choose
        @return str of the label's name
    """
    assert(len(choices) != 0)
    assert(choice > 0 and choice <= len(choices))
    return choices[choice - 1][0]

def parseScript(script):
    """This parses a file of the name script
    Script should be in this format
        <label>;<content>;<label 1|choice description 1>;<label 2|choice description 2>;...
    @param script str that points to filename of the script
    @return dict of the parsed format
    for example: {"start" : ["This is the start", [["end", "Go to the end"], ["middle", "Go to the middle"]]...}
    script content would be
    start;This is the start;end|Go to the end;middle|Go to the middle
    middle;<middle content>;<label|...> I hope you get it by now
    Commented lines start with #
    @assert lines should have label;content;next at the very least
    @assert each line has unique label
    @assert all choices should be exhaustive, in otherwords, they lead to a proper content
    """
    parsed = {}

    scriptfile = open(script, 'r')

    #print "Parsing", scriptfile.name

    line = scriptfile.readline()

    notfullfilled = set()
    while line:
#Check if it's just a blank line,
        if len(line) < 2:
            continue
#Commented line
        if line[0] == '#':
            continue
#Remove unnecessary stuff
        if line[-1] == '\n':
            line = line[:-1]
#Splitting by delimiters
        line = line.split(';')

        if len(line) < 3:
            print("Each line should consist of the following: label, content, next...")
            raise AssertionError
        if line[0] in parsed:
            print(line[0], "already points to previous content", parsed[line[0]])
            raise AssertionError
        choicesParsed = []
        for cp in line[2:]:
            choicelabel, choicecontent = cp.split('|')
            choicesParsed.append([choicelabel, choicecontent])
            if choicelabel in notfullfilled:
                notfullfilled.remove(choicelabel)
            elif choicelabel not in parsed:
                notfullfilled.add(choicelabel)

#Used for interpreting \n
        line[1] = line[1].split('\\n')
        line[1] = '\n'.join(line[1])

        """               [content, [choiceslabel, choicecontent]]"""
        parsed[line[0]] = [line[1], choicesParsed]
        line = scriptfile.readline()
    count = 0
    for i in notfullfilled:
        if i not in parsed:
            count += 1
    if count != 0:
        print("The following requires content", notfullfilled)
        raise AssertionError
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
