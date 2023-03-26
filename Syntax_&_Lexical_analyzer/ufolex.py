# ------------------------------------------------------------
# ufolex.py
#
# tokenizer for a expressions related to UFO sightings described
# on an xml file.
# ------------------------------------------------------------
import ply.lex as lex
import data_structures
import ply.yacc as yacc

class eventFoundFlagClass:
     eventFoundFlag = False
# List of token names.   This is always required
flag = eventFoundFlagClass()
tokens = (
    'STATES_LIST_OL',
    'STATES_LIST_CL',

    'STATE_OL',
    'STATE_CL',

    'SHAPES_LIST_OL',
    'SHAPES_LIST_CL', 

    'SHAPE_OL',
    'SHAPE_CL',

    'EVENT_OL',
    'EVENT_CL',

    'LINK_OL',
    'LINK_CL',
    'LINK_TEXT',

    'EVENT_DATE_OL',
    'EVENT_DATE_CL',
    'DATE_TEXT',

    'TIME_OL',
    'TIME_CL',

    'CITY_OL',
    'CITY_CL',

    'COUNTRY_OL',
    'COUNTRY_CL',

    'DURATION_OL',
    'DURATION_CL',

    'SUMMARY_OL',
    'SUMMARY_CL',

    'POSTED_OL',
    'POSTED_CL',

    'IMAGES_OL',
    'IMAGES_CL',
    'IMAGES_TEXT',    

    'GENERIC_TEXT', 
)

# Regular expression rules for simple tokens
t_GENERIC_TEXT   = r'[^<>]*[^<>]'

t_LINK_OL = r'<link>'
t_LINK_CL = r'<\/link>'
t_LINK_TEXT = r'https://nuforc\.org/webreports/reports/[0-9]+/[a-zA-Z0-9]+\.html'

t_EVENT_DATE_OL   = r'<date>'
t_EVENT_DATE_CL   = r'<\/date>'
t_DATE_TEXT = r'(1[0-2]?|[2-9])\/([1-2][0-9]?|3[0-1]?|[4-9])\/([0-9][0-9])'


t_TIME_OL        = r'<time>'
t_TIME_CL        = r'<\/time>'
#t_TIME_TEXT      = r'([0-1][0-9]|[2][0-3]:[0-5][0-9])|Unknown'

# In the city rule we want to get the string inmediately after the city tag
t_CITY_OL     = r'<city>'
t_CITY_CL        = r'<\/city>'

# In the country rule we want to get the string inmediately after the city tag
t_COUNTRY_OL     = r'<country>' 
t_COUNTRY_CL     = r'<\/country>'

t_STATE_OL       = r'<state>'
t_STATE_CL       = r'<\/state>'

t_STATES_LIST_OL = r'<states_list>'
t_STATES_LIST_CL = r'<\/states_list>'

t_SHAPES_LIST_OL = r'<shape_list>'
t_SHAPES_LIST_CL = r'<\/shape_list>'

t_SHAPE_OL       = r'<shape>'
t_SHAPE_CL       = r'<\/shape>'

t_EVENT_OL       = r'<event>'
t_EVENT_CL       = r'<\/event>'

t_DURATION_OL    = r'<duration>'
t_DURATION_CL    = r'<\/duration>'

t_SUMMARY_OL     = r'<su[a-z]+>'
t_SUMMARY_CL     = r'<\/su[a-z]+>'

t_POSTED_OL      = r'<p[a-z]+>'
t_POSTED_CL      = r'<\/p[a-z]+>'

t_IMAGES_OL      = r'<i[a-z]+>'
t_IMAGES_CL      = r'<\/i[a-z]+>'
t_IMAGES_TEXT    = r'(Yes|yes|No|no)'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Define a rule so we can track line numbers
def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
 
# Error handling rule
def t_error(t):
     t.lexer.skip(1)
 
# Build the lexer
lexer = lex.lex()

#Analizador sintáctico 
# dictionary of names
names = { }

eventFoundFlag = False

def p_ufo_xml(t):
     'ufo_xml     : states_list shape_list event_list'

def p_states_list(t):
     '''states_list : STATES_LIST_OL state STATES_LIST_CL'''

def p_state(t): 
     '''state       : STATE_OL GENERIC_TEXT STATE_CL
                    | state state'''
     if t[2] != None:
          data_structures.add_state(t[2])
          if flag.eventFoundFlag:
               data_structures.add_event(t[2])

def p_shape_list(t):
     '''shape_list  : SHAPES_LIST_OL shape SHAPES_LIST_CL'''
     
def p_shape(t):
     '''shape    : SHAPE_OL GENERIC_TEXT SHAPE_CL
                 | shape shape'''
     if t[2] != None:
          data_structures.add_shape(t[2])
          if flag.eventFoundFlag:
               data_structures.add_event(t[2])

def p_event_list(t):
     '''event_list  : event_list event_individual 
		          | event_individual'''

def p_event_individual(t):
     '''event_individual : EVENT_OL link event_date time city state country shape duration summary posted images EVENT_CL
                         | event_individual'''

def p_link(t):
     '''link   : LINK_OL LINK_TEXT LINK_CL'''
     
     if t[2] != None:
          data_structures.add_event(t[2])
          flag.eventFoundFlag = True     
#P
def p_event_date(t):
     '''event_date  : EVENT_DATE_OL DATE_TEXT EVENT_DATE_CL'''
     
     if t[2] != None:
          data_structures.add_event(t[2])

def p_time(t):
     '''time   : TIME_OL GENERIC_TEXT TIME_CL '''

     if t[2] != None:
          data_structures.add_event(t[2])     

#P
def p_city(t):
     '''city   : CITY_OL GENERIC_TEXT CITY_CL
               | CITY_OL CITY_CL'''

     if t[2] == '</city>':
          data_structures.add_event('None')
     elif t[2] != None:
          data_structures.add_event(t[2])
          

def p_country(t):
     '''country   : COUNTRY_OL GENERIC_TEXT COUNTRY_CL'''

     if t[2] != None:
          data_structures.add_event(t[2])
#P
def p_duration(t):
     '''duration   : DURATION_OL GENERIC_TEXT DURATION_CL'''

     if t[2] != None:
          data_structures.add_event(t[2])

def p_summary(t):
     '''summary   : SUMMARY_OL GENERIC_TEXT SUMMARY_CL'''

     if t[2] != None:
          data_structures.add_event(t[2])
#P
def p_posted(t):
     '''posted   : POSTED_OL DATE_TEXT POSTED_CL'''
     
     if t[2] != None:
          data_structures.add_event(t[2])

def p_images(t):
     '''images   : IMAGES_OL IMAGES_TEXT IMAGES_CL'''
     if t[2] != None:
          data_structures.add_event(t[2])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

# Read file
def read_file(file_name):
     with open(file_name, 'r') as f:
          data = f.read()
     return data

# Test it out
#data = read_file("UFO_Report_2022_medium_sample.xml")
data = read_file("UFO_Report_2022_sample.xml")

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
     tok = lexer.token()
     if not tok: 
         break      # No more input

parser = yacc.yacc()
parser.parse(data)
data_structures.fix()
#data_structures.print_all()

