import random
from flask import Flask, render_template, jsonify, request

class TrafficEnvironment:
    def __init__(self):
        self.queues = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        self.wait_times = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        # Directions are now independent. Start with North green.
        self.light_state = 'N_GREEN'
        self.yellow_timer = 0
        
        # We need to know what state we are transitioning TO after yellow
        self.next_state = None
        
        self.total_waiting_time = 0
        self.time_step = 0

    def get_percepts(self):
        # The agent now needs to see all 4 independent queues
        return self.queues

    def trigger_transition(self, target_state):
        if self.light_state != target_state and 'YELLOW' not in self.light_state:
            # E.g if cur is N_GREEN, go to N_YELLOW, and set next to S_GREEN
            current_dir = self.light_state.split('_')[0]
            self.light_state = f"{current_dir}_YELLOW"
            self.next_state = target_state
            self.yellow_timer = 2

    def step(self):
        # Handle yellow light transitions
        if 'YELLOW' in self.light_state:
            self.yellow_timer -= 1
            if self.yellow_timer <= 0:
                self.light_state = self.next_state
                self.next_state = None

        # Arrivals
        for d in self.queues:
            if random.random() < 0.6:
                self.queues[d] += random.randint(0, 3)

        # Departures: Only 1 direction gets to depart if it's green or yellow
        # (Usually vehicles still sneak through on yellow)
        if self.light_state == 'N_GREEN':
            self.queues['N'] = max(0, self.queues['N'] - 5)
        elif self.light_state == 'S_GREEN':
            self.queues['S'] = max(0, self.queues['S'] - 5)
        elif self.light_state == 'E_GREEN':
            self.queues['E'] = max(0, self.queues['E'] - 5)
        elif self.light_state == 'W_GREEN':
            self.queues['W'] = max(0, self.queues['W'] - 5)
            
        elif self.light_state == 'N_YELLOW':
            self.queues['N'] = max(0, self.queues['N'] - 1)
        elif self.light_state == 'S_YELLOW':
            self.queues['S'] = max(0, self.queues['S'] - 1)
        elif self.light_state == 'E_YELLOW':
            self.queues['E'] = max(0, self.queues['E'] - 1)
        elif self.light_state == 'W_YELLOW':
            self.queues['W'] = max(0, self.queues['W'] - 1)

        # Update Wait Times
        # On Green, wait time is 0. Otherwise, increment by 1 sec per step if there's a queue.
        # (Though the requirement says "when signal is red", yellow usually implies stopping, so we continue counting.
        # If queue is 0, arguably wait time is 0, but we just reset it on Green).
        for d in self.wait_times:
            if self.light_state == f"{d}_GREEN":
                self.wait_times[d] = 0
            else:
                self.wait_times[d] += 1

        # Totals
        for count in self.queues.values():
            self.total_waiting_time += count
            
        self.time_step += 1


class TrafficAgent:
    def __init__(self):
        self.current_green_time = 0
        self.min_green_time = 2

    def decide_action(self, percepts, current_light_state):
        if 'YELLOW' in current_light_state:
            return 'KEEP'
            
        self.current_green_time += 1
        
        if self.current_green_time < self.min_green_time:
            return 'KEEP'

        # Agent Logic: Find the direction with the absolute most waiting cars
        # If the max waiting is in the current green direction, keep it.
        # Otherwise, switch to the direction with the max if it's > current + 3.
        
        current_dir = current_light_state.split('_')[0]
        max_dir = max(percepts, key=percepts.get)
        
        if max_dir != current_dir and percepts[max_dir] > percepts[current_dir] + 3:
            self.current_green_time = 0
            return f"SWITCH_TO_{max_dir}"
            
        return 'KEEP'


app = Flask(__name__)
env = TrafficEnvironment()
agent = TrafficAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manual_light', methods=['POST'])
def manual_light():
    data = request.json
    new_state = data.get('state') # Expected: N_GREEN, S_GREEN, E_GREEN, W_GREEN
    
    global env, agent
    if new_state in ['N_GREEN', 'S_GREEN', 'E_GREEN', 'W_GREEN']:
        # Instantly switch to requested green, bypassing yellow transition
        env.light_state = new_state
        env.next_state = None
        env.yellow_timer = 0
        agent.current_green_time = 0
        
        # Also instantly reset the wait time of the new green direction
        target_dir = new_state.split('_')[0]
        env.wait_times[target_dir] = 0
        
    return jsonify({'status': 'ok', 'light_state': env.light_state})

@app.route('/set_queues', methods=['POST'])
def set_queues():
    data = request.json
    queues = data.get('queues', {})
    global env
    for d in ['N', 'S', 'E', 'W']:
        if d in queues:
            try:
                env.queues[d] = max(0, int(queues[d]))
            except (ValueError, TypeError):
                pass
    return jsonify({'status': 'ok', 'queues': env.queues})

@app.route('/step', methods=['POST'])
def step():
    percepts = env.get_percepts()
    action = agent.decide_action(percepts, env.light_state)
    
    if action != 'KEEP' and action.startswith('SWITCH_TO_'):
        target_dir = action.split('_')[2]
        env.trigger_transition(f"{target_dir}_GREEN")
        
    env.step()
    
    return jsonify({
        'queues': env.queues,
        'wait_times': env.wait_times,
        'light_state': env.light_state,
        'total_waiting_time': env.total_waiting_time,
        'time_step': env.time_step,
        'action_taken': action,
        'current_waiting': sum(env.queues.values())
    })

@app.route('/reset', methods=['POST'])
def reset():
    global env, agent
    env = TrafficEnvironment()
    agent = TrafficAgent()
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
