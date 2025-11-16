import serial
import time

words = {
    'negative': {
        'academic': [
            'difficult',
            'hard',
            'problem',
            'tough',
            'struggle',
            'pressure',
            'difficulty',
            'distractions',
            'struggled',
            'slack'
        ],
        'actions': [
            'risk',
            'fired',
            'dont',
            'broke',
            'outed',
            'miss',
            'removed',
            'hurt',
            'kicked',
            'deleted'
        ],
        'items': [
            'mice',
            'bomb',
            'tilted',
            'fungus',
            'rats',
            'rodent'
        ],
        'other': [
            'bad',
            'less',
            'issues',
            'harder',
            'down',
            'lost',
            'stress',
            'worst',
            'terrible',
            'missing'
        ],
        'people': [
            'nobody',
            'aiders',
            'panhandlers',
            'commies',
            'inconsiderate',
            'offenders',
            'obody'
        ],
        'places': [
            'overcrowding',
            'crowded',
            'dump',
            'cramped',
            'prison',
            'cell'
        ],
        'resources': [
            'tuition',
            'housing'
        ],
        'social': [
            'alone',
            'dry',
            'bored',
            'pissed',
            'upsetting',
            'downvoted',
            'embarrassing',
            'drunken',
            'aggressive',
            'rude'
        ]
    },
    'neutral': {
        'academic': [
            'semester',
            'class',
            'program',
            'college',
            'classes',
            'course',
            'research',
            'questions',
            'project',
            'rch'
        ],
        'actions': [
            'have',
            'going',
            'want',
            'say',
            'change',
            'took',
            'make',
            'work',
            'made',
            'used'
        ],
        'items': [
            'hat',
            'tickets',
            'money',
            'food',
            'software',
            'bike',
            'bed',
            'data',
            'mail',
            'packages'
        ],
        'other': [
            'more',
            'from',
            'out',
            'how',
            'also',
            'should',
            'what',
            'now',
            'first',
            'way'
        ],
        'people': [
            'students',
            'people',
            'team',
            'student',
            'band',
            'roy',
            'professor',
            'someone',
            'coach',
            'him'
        ],
        'places': [
            'nion',
            'school',
            'rpi',
            'room',
            'campus',
            'larkson',
            'home',
            'house',
            'place',
            'office'
        ],
        'resources': [
            'system',
            'email',
            'services',
            'parking',
            'credit',
            'info',
            'advice',
            'government',
            'anner',
            'wikipedia'
        ],
        'social': [
            'game',
            'hockey',
            'games',
            'hey',
            'group',
            'lunch',
            'lol',
            'rivalry',
            'football',
            'sports'
        ]
    },
    'positive': {
        'academic': [
            'goal',
            'high',
            'learning',
            'understanding',
            'lead',
            'understand',
            'learn',
            'easy',
            'championship',
            'accepted'
        ],
        'actions': [
            'recommend',
            'help',
            'working',
            'fix',
            'fixed',
            'win',
            'improve',
            'fixing',
            'support',
            'scored'
        ],
        'items': [
            'mores',
            'chilli',
            'burgers'
        ],
        'other': [
            'good',
            'right',
            'free',
            'experience',
            'better',
            'great',
            'easier',
            'able',
            'interested',
            'love'
        ],
        'people': [
            'friends',
            'tutors',
            'friend',
            'master',
            'utors',
            'bff',
            'star',
            'tars',
            'stars',
            'mentor'
        ],
        'places': [],
        'resources': [
            'aid',
            'tutoring',
            'power',
            'scholarship',
            'successcenter',
            'opportunities',
            'counseling',
            'recommendations',
            'tips',
            'resource'
        ],
        'social': [
            'pep',
            'hanks',
            'community',
            'fun',
            'hangout',
            'confidential',
            'spirit',
            'willing',
            'together',
            'bonfire'
        ]
    }
}

commands = {
    '.': '1',
    '-': '2',
    '.-': '3',
    '-.': '4',
    '..': '5',
    '--': '6',
    '.--': '7',
    '..-': '8',
    '...': '9',
    '---': '10',
    '....': 'back onece',
    '.....': 'back to root',
    '......': 'end program'
}

commands_mapping = {
    1: '.',
    2: '-',
    3: '.-',
    4: '-.',
    5: '..',
    6: '--',
    7: '.--',
    8: '..-',
    9: '...',
    10: '---'
}

def get_input():
    ser = serial.Serial("COM5", 9600, timeout = 1)
    time.sleep(2)
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").strip()
                print(line)
                
    except KeyboardInterrupt:
        print("Exiting Program")
    finally:
        ser.close()
    return line

class menu:
    def __init__(self, file_system):
        self.file_system = file_system
        self.current_position = file_system
        self.path = []

    def display_path(self):
        if not self.path:
            print('root')
        else:
            path_str = ' > '.join(self.path)
            print(f'root > {path_str}')

    def on_leaf(self):
        return isinstance(self.current_position, list)

    def options(self):
        if self.on_leaf():
            return self.current_position
        else:
            return sorted(list(self.current_position.keys()))

    def move_forward(self, choice):
        if self.on_leaf():
            print('error: on leaf')
            return False
        
        if choice in self.current_position:
            self.current_position = self.current_position[choice]
            self.path.append(choice)
            return True
        else:
            print('error: invalid choice')
            return False

    def move_back(self):
        if not self.path:
            print('error: you are at the root')
            return
        self.path.pop()
        self.current_position = self.file_system
        for key in self.path:
            self.current_position = self.current_position[key]

test = menu(words)
navigating = True
final_message_words = []

while navigating:
    print()
    test.display_path()
    current_options = test.options()
    if test.on_leaf():
        if not current_options:
            print('error: nothing in that category')
        for i, word in enumerate(current_options, 1):
            print(f'{commands_mapping[i]} {word}')
        choice = get_input().replace(" ", "")
        if choice == '....':
            test.move_back()
            continue
        if choice == '.....':
            test.current_position = test.file_system
            test.path = []
            continue
        if choice == '......':
            navigating = False
            break
        try:
            num_str = commands[choice]
            choice_index = int(num_str) - 1  
            if 0 <= choice_index < len(current_options):
                selected_word = current_options[choice_index]
                final_message_words.append(selected_word)
                print(f'added {selected_word}')
                test.current_position = test.file_system
                test.path = []
            else:
                print('error: nothing in that position')
        except (ValueError, KeyError):
            print('error: invalid command')
    else:
        for i, option_name in enumerate(current_options, 1):
            print(f'{commands_mapping[i]} {option_name}')
        choice = get_input().replace(" ","")
        if choice == '....':
            test.move_back()
            continue
        if choice == '.....':
            test.current_position = test.file_system
            test.path = []
            continue
        if choice == '......':
            navigating = False
            break
        try:
            num_str = commands[choice]
            choice_index = int(num_str) - 1
            
            if 0 <= choice_index < len(current_options):
                selected_key = current_options[choice_index] 
                test.move_forward(selected_key)
            else:
                print('error: nothing in that position')
        except (ValueError, KeyError):
            print('error')
print()
print('ended')
if final_message_words:
    print(f'output: {' '.join(final_message_words)}')