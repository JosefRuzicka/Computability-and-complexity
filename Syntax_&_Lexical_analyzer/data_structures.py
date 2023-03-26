# File for handling the data structures

# ------------------------------------------------------------
# State List and Shape List are managed each as a diccionary, key is the state/shape name and value is the number of times it appears in the data set.
from pickle import TRUE


state_list = {}
shape_list = {}
event_list = []

def add_state(state):
  if state in state_list:
    state_list[state] += 1
  else:
    state_list[state] = 1

def add_shape(shape):
  if shape in shape_list:
    shape_list[shape] += 1
  else:
    shape_list[shape] = 1

def add_event(event):
  event_list.append(event)

# ------------------------  AUXILIAR METHODS  --------------------------
def print_states():
  print("------------------------  STATE LIST  --------------------------")
  for key in sorted(state_list):
    print(key, ":", state_list[key])

def print_shapes():
  print("------------------------  SHAPE LIST  --------------------------")
  for key in sorted(shape_list):
    print(key, ":", shape_list[key])

def print_events():
  print("------------------------  EVENT LIST  --------------------------")
  for key in event_list:
    print(key)

def fix():
  # Substract 1 from all the states and shapes that have a value greater than 1
  for key in state_list:
    if state_list[key] > 1:
      state_list[key] -= 1
  for key in shape_list:
    if shape_list[key] > 1:
      shape_list[key] -= 1

def get_stats_for_all_states():
  states_stats = {}
  for key in state_list:
    #print("State: ", key)
    #print("Number of events: ", state_list[key])
    #print("Next event in state: ", calculate_next_event_in_state(key))
    #print("Events in state: ", filter_events_list_by_state(key))
    #print("----------------------------------------------------------")
    # Add this value to the dictionary of states, add only three decimals
    states_stats[key] = round(calculate_next_event_in_state(key), 2)
  
  return states_stats

def calculate_next_event_in_state(state):
  keys = list(state_list.keys())
  # Make a sum of all the values of the states
  sum = 0
  for key in keys:
    sum += state_list[key]
  # Calculate the probability of the state
  probability = state_list[state] / sum
  # Calculate the next event in the state
  next_event = probability * 100
  return next_event

def print_all():
  #print_states()
  #print_shapes()
  print_events()

def filter_events_list_by_state(name, list=event_list):
  filtered_list = []
  for i in (range(int(len(list)/11))):
    if (list[i*11 + 4] == name):
      for j in range(11):
        filtered_list.append(list[i*11 + j]) 
  return filtered_list

def filter_events_list_by_shape(name, list=event_list):
  filtered_list = []
  for i in (range(int(len(list)/11))):
    if (list[i*11 + 6] == name):
      for j in range(11):
        filtered_list.append(list[i*11 + j]) 
  return filtered_list
