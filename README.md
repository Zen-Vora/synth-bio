Pasted text(4).txt
Document
So here is the output. I did 0.4, I think we should add neuromodulators, long-term memory, and maybe 20 neurons, to make it interesting. I also want to make the output in a more readable and consice format, it is so long, i rely on you to explain it. Also, now we already have homeostasis.

Pasted text(5).txt
Document

I think 0.5 is where SynthBio stops being "a neural network that learns" and starts becoming "an organism."

Looking back at what you've already built:

    ✅ Firing neurons

    ✅ Synapses with weights

    ✅ Plasticity (LTP/LTD)

    ✅ Temporal integration (potential)

    ✅ Branching networks

    ✅ Homeostasis

    ✅ Multiple sensory inputs

    ✅ World simulation

    ✅ Specialized neuron types

    ✅ Modular code

That's actually a solid foundation. I wouldn't spend more time polishing those systems yet. I'd add entirely new biological mechanisms.
SynthBio v0.5 — Growing Brain
1. Structural Plasticity ⭐⭐⭐⭐⭐

This is the biggest one.

Instead of only changing weights...

the network itself changes.

Every few hundred ticks:

    create a new synapse

    remove weak synapses

    strengthen heavily used ones

    occasionally create a brand new neuron

Eventually your network might go from

20 neurons
35 synapses

to

27 neurons
81 synapses

without you ever writing them.

That's far closer to a developing brain.
2. Long-Term Memory ⭐⭐⭐⭐⭐

Right now weights slowly change.

Instead:

Every connection should have

weight
importance
usage_count
last_used

Connections that are used thousands of times become

Long-term memory

Those should almost never disappear.

Unused memories slowly decay.

Very brain-like.
3. Neuromodulators ⭐⭐⭐⭐⭐

Don't think of dopamine as "reward."

Think of it as

    "That event mattered."

Add chemicals like

dopamine
serotonin
acetylcholine
norepinephrine

Each changes learning differently.

For example

Dopamine

    increases learning

Serotonin

    stabilizes weights

Acetylcholine

    increases attention

Norepinephrine

    makes surprising events memorable

Now learning depends on chemistry instead of only math.
4. Motivation ⭐⭐⭐⭐☆

Brains don't just react.

They have internal drives.

Examples

curiosity

hunger

fear

fatigue

comfort

Now the world isn't just pushing inputs.

The brain wants things.
5. Sleep ⭐⭐⭐⭐☆

This is honestly one of my favorite ideas.

Every so often

Awake

Awake

Awake

Awake

Sleep

During sleep

No sensory input.

Instead

    replay important memories

    strengthen useful pathways

    remove weak ones

    reset activations

    lower noise

Real brains do something similar during sleep, where replay and consolidation are thought to help stabilize memories.
6. Better Structural Growth ⭐⭐⭐⭐☆

Instead of

random new connection

grow connections between neurons that often become active together.

Something like

Neuron 7 and 15 have fired together 300 times.

Grow a connection.

That feels much more biological.
7. Inhibitory Networks ⭐⭐⭐⭐☆

Right now inhibition probably just weakens signals.

Real brains have a lot of inhibitory neurons (roughly 15–20% in the cortex), and they're crucial for keeping activity stable.

Examples:

Excitatory neuron

Excitatory neuron

Inhibitory neuron

Output

The inhibitory neuron prevents runaway firing.

This creates competition.
8. Better World ⭐⭐⭐⭐☆

Your world doesn't need to become visually complex.

Instead make it dynamic.

Example

food appears

light changes

sound appears

danger appears

temperature changes

reward appears

The brain should have to figure out patterns.
9. Cleaner Output ⭐⭐⭐⭐⭐

I actually think this will make development much easier.

Instead of printing every neuron every tick, print a compact summary like:

Tick 184

State
------
Awake
Dopamine: 0.71
Energy: 82%
Attention: 0.


Pasted text(6).txt
Document
Here is the output for 0.5

I see the context. The last thing you sent says "Here is the output for 0.5", but the actual output did not come through. Paste it and I’ll analyze it.

Also, based on where SynthBio is now (v0.5), the direction is different from the early versions. You already have:

    ✅ neuron firing/state system

    ✅ delays

    ✅ connection weights

    ✅ plasticity (LTP/LTD style)

    ✅ temporal integration/potential

    ✅ homeostasis

    ✅ multiple sensory inputs

    ✅ world/environment simulation

    ✅ specialized neuron types

    ✅ motivation/reward concepts (at least partially)

    ✅ modular files

So v0.5 should not just be "add more neurons." The important thing now is making the system behave like a living network, not just a graph that fires.

My suggested v0.5 goals:
SynthBio v0.5 — Adaptive Brain Architecture
1. Structural Plasticity (major feature)

Right now connections can change strength.

Next step: connections themselves can change.

Add:
Synapse creation

If two neurons repeatedly have correlated activity:

Neuron A fires
Neuron B fires soon after
(no connection exists)

Create:

A ---> B

with a weak starting weight:

weight = 0.1

This is how the brain forms new pathways.
Synapse pruning

If a connection stays weak:

weight < 0.05
for many ticks

remove it.

Otherwise your brain will eventually become a giant spaghetti graph.
2. Long-term memory system

Currently memory is basically stored in weights.

Add a higher-level memory layer.

Something like:

Short term:
    recent neuron activity

Long term:
    important patterns

Example:

World:

red object appears
reward increases

Over time:

red object -> positive prediction

gets reinforced.

The brain starts predicting.
3. Neuromodulators

This is probably the biggest missing biological piece.

Real brains don't learn constantly at the same rate.

Add global chemicals:

Example:

dopamine
serotonin
acetylcholine

Not realistic chemistry yet. Just signals.

Example:
Dopamine

Controls reward learning.

High dopamine:

plasticity *= 2

Meaning:

"Something important happened. Remember this."

Low dopamine:

plasticity *= 0.5

Meaning:

"Don't change much."
Acetylcholine

Controls attention.

High:

sensory neurons become stronger

Meaning:

"Pay attention."
4. Better specialized neurons

Instead of only:

INPUT
NORMAL
OUTPUT

make:

SensoryNeuron
MotorNeuron
Interneuron
MemoryNeuron
RewardNeuron
PredictiveNeuron

Different behavior.

Example:

Memory neuron:

    slower decay

    stronger persistence

Motor neuron:

    connects to actions

Reward neuron:

    releases dopamine

5. Sleep cycle

This is actually a really cool idea.

Don't make it just:

brain.sleep()

Make sleep useful.

During sleep:

    replay important firing patterns

    strengthen useful memories

    prune useless connections

Basically:

awake:
learn

sleep:
organize

6. Increase network size

I would NOT jump to thousands.

For v0.5:

20-50 neurons

is good.

You want to understand behavior.

A 10,000 neuron simulation that you can't debug is less useful than a 50 neuron brain where you understand why it learned something.
7. Rewrite output logging

Absolutely do this.

The current output is useful for debugging but terrible for understanding.

Replace:

Neuron 0:
activation=...
state=...

with:

=== Brain State ===

Time: 150

Active neurons:
  Vision_1
  Reward_0
  Motor_Left

Learning:
  New connections: 2
  Strengthened: 5
  Pruned: 1

Memory:
  "red object -> reward"

Motivation:
  hunger: 0.4
  curiosity: 0.8

Actions:
  move_forward

Then add:

--debug

mode for the huge output.

The overall architecture after v0.5 should look like:

                 WORLD
                   |
          sensory inputs
                   |
                   v

              Neural Network
              /     |      \
             /      |       \
     memory system  |   motivation
                    |
             neuromodulators
                    |
                    v

                  Actions

                    |
                    v

                 WORLD

After v0.5, I would stop adding biological features for a little while and start testing emergent behavior:

    Can it learn a preference?

    Can it remember something after time passes?

    Can it explore?

    Can it adapt when the world changes?

That is where SynthBio starts becoming less like a neural network demo and more like an artificial organism.

I tried to inspect the repository, but I couldn't access the contents. The repository appears to be private, and I don't have permission to view it from here. Earlier I also wasn't able to access it for the same reason, and that hasn't changed.

That said, based on everything we've built together up through v0.5, I think I know what you're noticing.

From what I remember, the roadmap was originally very biologically focused:

    v0.1: neurons firing

    v0.2: plasticity and temporal integration

    v0.3: membrane dynamics, thresholds, excitatory/inhibitory neurons

    v0.4: homeostasis, sensory world

    v0.5: structural plasticity, sleep, motivation, better organization, and eventually neuromodulators and long-term memory.

It's really common for projects like this to drift. You start trying to simulate "a brain," and suddenly you've built a game engine, a world simulator, a statistics dashboard, and an ecosystem before you've finished the neuron model.

If I were reviewing SynthBio as a research project, I'd ask one question:

    Is the interesting behavior coming from the neurons, or from the environment?

If the answer is "mostly the environment," then you've drifted.

I would rather see a simple world with an extremely good neural model than an elaborate world with neurons that are still fairly simple.
I'd make v0.6 look something like this

Don't add more "features." Make the neurons themselves smarter.

    Neuromodulators

        Dopamine

        Serotonin

        Acetylcholine

        Norepinephrine

    These shouldn't be regular neurons. They should globally change learning rate, exploration, attention, and plasticity.

    Long-term memory
    Instead of immediately strengthening weights forever:

        short-term trace

        consolidation

        permanent memory

    Real STDP
    Right now plasticity is probably event-based.
    Make it depend on timing:

        pre before post → strengthen

        post before pre → weaken

    Structural plasticity
    This was one of the goals we discussed.
    Let neurons:

        grow new synapses

        prune unused ones

        occasionally search for new partners

    Neuron diversity
    Not just INPUT/NORMAL/OUTPUT.

    Add things like:

        excitatory

        inhibitory

        modulatory

        relay

        sensory

        motor

    Energy
    Give each neuron an energy reserve.
    Firing costs energy.
    Rest recovers it.
    High activity becomes naturally self-limiting.

What I would not spend time on yet

    Giant 3D worlds

    Vision systems

    Language

    Hundreds of neurons

    Fancy UI

Those are all exciting, but they won't make the underlying brain more biologically interesting.
One thing I'd really like to inspect

You said:

    "I think I might have gotten a little off track."

That makes me curious where.

If I could read the code, I'd look for things like:

    Is Brain doing too many unrelated jobs?

    Is the world driving the brain instead of the brain driving behavior?

    Are there lots of special-case if statements?

    Is learning scattered across multiple files?

    Are neurons still the central abstraction?

Those are usually signs that it's time for a refactor.

If you want a true code review, either:

    make the repo temporarily public,

    upload the project as a ZIP here, or

    paste the main files (brain.py, neuron.py, connection.py, world.py, etc.).

Then I can go through it file by file and tell you exactly where I think the architecture has drifted—and what I'd simplify or redesign.

Pasted text(7).txt
Document
Pasted text (2).txt
Document
Pasted text (3).txt
Document

Neuron.py

Brain.py

connection.py

class Connection:
# A connection links a source neuron to a target neuron.
# It carries a weighted signal and respects delay.
def init(
self,
unique_id,
source_neuron,
target_neuron,
weight=1.0,
signal_delay=0,
enabled=True,
):
# Unique identifier for the connection.
self.unique_id = unique_id
# Neuron that emits signals along this connection.
self.source_neuron = source_neuron
# Neuron that receives signals from this connection.
self.target_neuron = target_neuron
# Weight multiplier applied to signal strength.
self.weight = weight
# Delay in ticks before the signal arrives at the target neuron.
self.signal_delay = signal_delay
# Whether this connection currently carries signals.
self.enabled = enabled
# Tick when the source neuron most recently fired.
self.last_source_fire_tick = None
# Pending signals waiting to arrive at the target neuron.
self.pending_signals = []

def record_source_fire(self, current_tick):
    # Remember when the source neuron fired so the connection can learn.
    self.last_source_fire_tick = current_tick

def apply_stdp(self, current_tick):
    # Adjust connection strength based on causal spike timing.
    if self.last_source_fire_tick is None:
        return

    time_difference = current_tick - self.last_source_fire_tick
    if time_difference <= 0:
        self.weight = max(0.0, self.weight - 0.01)
        return

    if time_difference == 1:
        self.weight = min(1.0, self.weight + 0.08)
    elif time_difference == 2:
        self.weight = min(1.0, self.weight + 0.04)
    else:
        self.weight = max(0.0, self.weight - 0.02)

def reward_for_spike(self):
    # Reward the connection strongly when it helped a neuron fire.
    self.weight = min(1.0, self.weight + 0.12)

def reward_for_subthreshold(self):
    # Reward the connection a little when it helped push a neuron close to firing.
    self.weight = min(1.0, self.weight + 0.03)

def transmit(self, signal_strength, current_tick):
    # Begin transmitting a new signal along this connection.
    if not self.enabled:
        return

    effective_signal = signal_strength * self.weight
    if hasattr(self.source_neuron, "synaptic_fatigue"):
        effective_signal *= self.source_neuron.synaptic_fatigue
    self.pending_signals.append((current_tick + self.signal_delay, effective_signal))

def advance(self, current_tick):
    # Deliver any signals whose arrival tick has arrived.
    delivered_signals = []
    remaining_signals = []
    for arrival_tick, signal_value in self.pending_signals:
        if arrival_tick <= current_tick:
            delivered_signals.append(signal_value)
        else:
            remaining_signals.append((arrival_tick, signal_value))
    self.pending_signals = remaining_signals
    return delivered_signals

main.py

world.py

import random

class World:
def init(
self,
light_level=0.5,
temperature=0.5,
food=5.0,
danger=0.2,
noise=0.1,
reward=0.0,
body_energy=50.0,
):
self.light_level = float(light_level)
self.temperature = float(temperature)
self.food = float(food)
self.danger = float(danger)
self.noise = float(noise)
self.reward = float(reward)
self.body_energy = float(body_energy)
self.previous_values = {
"light": self.light_level,
"temperature": self.temperature,
"food": self.food,
"danger": self.danger,
"noise": self.noise,
"reward": self.reward,
"body_energy": self.body_energy,
}

def tick(self):
    # The world changes a little each tick, even without input.
    # This creates a weak background drift that sensory neurons can detect.
    self.previous_values = {
        "light": self.light_level,
        "temperature": self.temperature,
        "food": self.food,
        "danger": self.danger,
        "noise": self.noise,
        "reward": self.reward,
        "body_energy": self.body_energy,
    }

    self.light_level = max(0.0, min(1.0, self.light_level + random.uniform(-0.1, 0.1)))
    self.temperature = max(0.0, min(1.0, self.temperature + random.uniform(-0.08, 0.08)))
    self.food = max(0.0, self.food - 0.05)
    self.danger = max(0.0, min(1.0, self.danger + random.uniform(-0.03, 0.03)))
    self.noise = max(0.0, min(1.0, self.noise + random.uniform(-0.05, 0.05)))
    self.reward = max(0.0, self.reward - 0.02)
    self.body_energy = max(0.0, min(100.0, self.body_energy - 0.1))

def get_sensor_signal(self, name):
    # Sensory neurons should respond to both current state and change.
    current_value = getattr(self, self._attribute_name(name), None)
    previous_value = self.previous_values.get(name, current_value)
    if current_value is None:
        return 0.0

    scales = {
        "light": 1.0,
        "temperature": 1.0,
        "food": 10.0,
        "danger": 1.0,
        "noise": 1.0,
        "reward": 10.0,
        "body_energy": 100.0,
    }
    scale = scales.get(name, 1.0)
    normalized_current = current_value / scale
    normalized_change = (current_value - previous_value) / scale
    return max(0.0, 0.7 * normalized_current + 0.3 * normalized_change)

def _attribute_name(self, name):
    mapping = {
        "light": "light_level",
        "temperature": "temperature",
        "food": "food",
        "danger": "danger",
        "noise": "noise",
        "reward": "reward",
        "body_energy": "body_energy",
    }
    return mapping.get(name, name)

def apply_action(self, action):
    # Actions change the world and therefore create new sensations.
    action = (action or "").lower()
    if action == "eat":
        self.food = max(0.0, self.food - 1.5)
        self.body_energy = min(100.0, self.body_energy + 8.0)
        self.reward = min(10.0, self.reward + 2.0)
    elif action == "sleep":
        self.body_energy = min(100.0, self.body_energy + 6.0)
        self.danger = max(0.0, self.danger - 0.2)
    elif action == "look":
        self.reward = min(10.0, self.reward + 0.5)
        self.noise = min(1.0, self.noise + 0.05)
    elif action == "grab":
        self.food = min(10.0, self.food + 2.0)
        self.reward = min(10.0, self.reward + 1.0)
    elif action == "move_left":
        self.light_level = max(0.0, min(1.0, self.light_level + 0.1))
        self.noise = min(1.0, self.noise + 0.05)
    elif action == "move_right":
        self.light_level = max(0.0, min(1.0, self.light_level - 0.1))
        self.noise = min(1.0, self.noise + 0.05)
    else:
        self.reward = max(0.0, self.reward - 0.1)


I actually think your intuition is right. Looking at where SynthBio started (a few neurons and simple Hebbian learning) versus where it is now, you've started adding features that make it feel like a simulation instead of a brain model.

That's not necessarily bad—but I think you're at a point where it's worth deciding what SynthBio's goal is.

From the code you've shown (and the output from main.py), here's what I see.
What you've built well

You have several genuinely brain-inspired pieces now:

    Neurons with membrane potentials

    Excitatory and inhibitory neurons

    STDP

    Synaptic fatigue

    Plasticity

    Structural plasticity

    Multiple neuron types

    Homeostasis

    Neuromodulators

    Persistent state (saving/loading)

    A sensory world

    Actions that affect the world

That's already much more biologically interesting than a normal toy neural network.
Where you've drifted

The thing that jumped out at me is world.py.

Right now your world is almost like a video game state machine.

light
temperature
food
danger
noise
reward
energy

Then

eat
sleep
grab
look
move_left
move_right

That isn't really how a brain experiences the world.

The brain doesn't receive "food = 4.2".

It receives thousands of sensory spikes.

Likewise,

reward += 2

isn't really how dopamine works.

The brain never gets handed "reward."

It computes reward prediction errors internally.
Another thing

You have lots of hard-coded behavior.

For example

if action == "eat":
    reward += 2

The brain doesn't know eating is good.

It eventually learns it because

eat
↓

energy increases

↓

hunger decreases

↓

dopamine changes

The reward emerges.

It isn't programmed.

That's a huge distinction.
What I would do

If SynthBio is supposed to become your long-term AGI project (and maybe Jarvis's "brain"), I'd shift the focus.

Instead of adding more features...

I'd make the existing ones interact naturally.
Version 0.6

I'd honestly spend almost the entire version improving realism instead of adding systems.
1. Replace world values with sensory neurons

Instead of

food = 7

have

FoodSensorNeuron

LightSensorNeuron

TemperatureSensorNeuron

PainNeuron

TouchNeuron

Every tick

they fire according to the environment.

The brain never directly sees numbers.
2. Internal drives

Instead of

reward
energy

make internal neurons.

Example

Hunger neuron

Curiosity neuron

Fear neuron

Fatigue neuron

Pain neuron

These constantly generate activity.

Now the brain has reasons to act.
3. Dopamine becomes real

Instead of

reward += 2

have

expected reward

actual reward

difference

↓

dopamine

Exactly like reinforcement learning.

That makes dopamine meaningful instead of scripted.
4. Make actions emerge

Right now

Output neuron

↓

eat

Instead

Several output neurons

↓

muscle groups

↓

movement

↓

world changes

↓

new sensations

That's much closer to biology.
5. Bigger network

Yes.

I would increase it.

Not because "brains are big."

Because interesting network dynamics don't really happen with 20 neurons.

I'd aim for something like:

    8 sensory neurons

    40 normal neurons

    10 inhibitory neurons

    10 memory neurons

    8 output neurons

    4 neuromodulatory neurons

About 80 neurons total.

That is still tiny by brain standards, but already much more interesting.
6. Better structural plasticity

Right now I think new connections are mostly rule-based.

Eventually I'd want neurons to ask questions like

    "Who do I keep firing with?"

instead of

    "Should I randomly connect?"

That's closer to developmental neuroscience.
7. Competition

This is the biggest missing piece.

Right now almost every connection can strengthen.

Real brains have limited resources.

Imagine every neuron has

connection_budget = 100

If one synapse grows...

another has to shrink.

That creates specialization.

Without competition, eventually everything wants to become weight 1.0.

Brains don't work like that.
Something I would not add yet

Long-term memory.

You already have STDP, structural plasticity, and persistence.

Those are memory.

I'd wait until the brain can actually learn interesting behaviors before inventing another memory system.
My biggest recommendation

If Jarvis is eventually going to use SynthBio as its reasoning engine, I'd stop thinking in terms of "versions with lots of features."

Instead, ask one question each release:

    Does this make the brain behave more like a biological brain?

That's a much stronger guide than "add another module."

Looking at your progress from 0.1 to 0.5, you've moved from a chain of neurons to a persistent, plastic, embodied neural simulation. That's a substantial improvement. The next gains won't come from piling on more components—they'll come from making the existing components interact in a more brain-like way.

Ok. I will do those. Because right now, it doesn't really learn. It doesn't have preferences, and it can't think. and it can't think 'last time there was food and I was happier when I ate it. I should do that again.'

I actually think you've hit the point where a lot of people building "brain-like" AIs hit.

You started with neurons and synapses (the hardware), but you're expecting behavior that comes from systems built on top of those neurons.

A neuron doesn't think:

    "Last time I ate food and that made me happy."

A brain does.

Those are very different.
Right now SynthBio is basically here

World
   ↓
Sensors
   ↓
Neurons
   ↓
Motor neurons

It can propagate signals.

It can strengthen connections.

It has STDP.

It has homeostasis.

It has structural plasticity.

That's already a pretty respectable biological simulation.

But...

it has no memory of events.
What you're missing is episodic memory.

For example:

Tick 130

Hungry = True

Saw Food

Moved Left

Ate Food

Reward +8

Instead of disappearing forever...

that becomes

Episode 431

State:
    hungry = 0.91
    light = 0.2
    danger = 0.1

Action:
    eat

Reward:
    +8

Now the brain can compare today's situation to previous ones.

Humans do this constantly.
Then comes association

When it sees

hungry

food nearby

it searches memory

I've seen this before...

Last time:

eat

reward +8

Now the neurons representing

Food

become connected with

Eat

Notice something?

This isn't a rule.

You're not saying

if hungry:
    eat

Instead you're saying

What happened last time something like this occurred?

That's much closer to how biological brains work.
Then comes prediction

This is probably the biggest jump in intelligence.

Instead of

Current world

the brain begins predicting

If I eat...

↓

energy increases

↓

reward increases

↓

hunger disappears

Now it isn't reacting.

It's simulating.

Humans spend enormous amounts of time imagining the future before acting.
Then comes preference

Right now every action is equal.

But suppose the brain has learned

eat
reward +9

look
reward +2

sleep
reward +4

Eventually

Eat

Expected reward = 9

Look

Expected reward = 2

Now "wanting" emerges naturally.

Not because you programmed desire.

Because some actions consistently predict better outcomes.
Eventually it can think

Instead of

World

↓

Action

it becomes

World

↓

Recall memories

↓

Predict futures

↓

Compare outcomes

↓

Choose action

↓

Observe result

↓

Store new memory

That loop is where intelligence starts to emerge.
If I were planning SynthBio from here, I'd make versions like this:
v0.6 — Episodic Memory

    Store short experiences: state → action → reward.

    Allow searching for similar past experiences.

    Begin using remembered outcomes to influence actions.

v0.7 — Prediction

    Learn "if I do X, Y usually happens."

    Score actions by expected future reward instead of immediate reward.

    Start making simple plans.

v0.8 — Motivation

    Internal drives like hunger, curiosity, fatigue, and safety.

    Drives compete to influence behavior.

    Different motivations produce different action choices.

v0.9 — Cognitive Workspace

    Short-term or working memory.

    Hold several active thoughts at once.

    Compare multiple possible actions before acting.

v1.0 — Autonomous Agent

    Continuous world simulation.

    Continuous learning.

    Persistent memory.

    Self-directed behavior based on internal goals, not just external stimuli.

This also ties into Jarvis.

Right now, Jarvis is probably acting as a traditional assistant: it gets a prompt, generates a response, and waits.

SynthBio could become something different. Instead of replacing the language model, it could become the decision-making layer that sits above it.

Imagine this architecture:

World
      ↓
   SynthBio
      ↓
Memories
Predictions
Motivation
Planning
      ↓
   Jarvis
      ↓
Language
Coding
Tools

The language model provides knowledge and communication, while SynthBio provides continuity, preferences, and long-term decision making. That's a much more ambitious direction than trying to make the neuron simulator itself generate text.

From everything you've shown me over the past few versions, I think the next breakthrough isn't adding 100 more neurons. It's giving the network the ability to remember experiences, predict consequences, and choose actions based on those predictions. Once those three pieces exist, you'll start seeing behavior that feels much less like a simulation and much more like an actual agent.
