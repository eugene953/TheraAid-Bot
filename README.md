Then install Rasa via pip:

// pip install rasa

Verify installation:

// rasa --version

Step 2: Create a New Rasa Project
In your terminal, run:

// rasa init --no-prompt
This creates a new folder with the default project structure:

your_project/
│
├── data/                 # Contains training data
│   └── nlu.yml           # NLU training examples
│   └── rules.yml         # Rules for conversation flow
│   └── stories.yml       # Example conversations
│
├── models/               # Trained models go here
├── actions/              # Custom action code
│   └── actions.py
│
├── domain.yml            # Intents, entities, slots, responses
├── config.yml            # Pipeline and policy configuration
├── credentials.yml       # Connectors like REST, Telegram
├── endpoints.yml         # Action server, tracker store etc.
└── tests/                # Conversation tests





version: "3.1"*

nlu:
- intent: greet
  examples: |
    - hello
    - hi
    - hello there
    - good morning
    - good evening
    - moin
    - hey there
    - let's go
    - hey dude
    - goodmorning
    - goodevening
    - good afternoon
    - How you dey #pidgin
    - Ya dey  #Local dialect

- intent: goodbye
  examples: |
    - cu
    - good by
    - cee you later
    - good night
    - bye
    - goodbye
    - have a nice day
    - see you around
    - bye bye
    - see you later

- intent: affirm
  examples: |
    - yes
    - y
    - indeed
    - of course
    - that sounds good
    - correct

- intent: deny
  examples: |
    - no
    - n
    - never
    - I don't think so
    - don't like that
    - no way
    - not really

- intent: mood_great
  examples: |
    - perfect
    - great
    - amazing
    - feeling like a king
    - wonderful
    - I am feeling very good
    - I am great
    - I am amazing
    - I am going to save the world
    - super stoked
    - extremely good
    - so so perfect
    - so good
    - so perfect

- intent: mood_unhappy
  examples: |
    - my day was horrible
    - I am sad
    - I don't feel very well
    - I am disappointed
    - super sad
    - I'm so sad
    - sad
    - very sad
    - unhappy
    - not good
    - not very good
    - extremly sad
    - so saad
    - so sad

- intent: bot_challenge
  examples: |
    - are you a bot?
    - are you a human?
    - am I talking to a bot?
    - am I talking to a human?

/////// domain.yml  ///////////////////////

version: "3.1"

intents:
  - greet
  - goodbye
  - affirm
  - deny
  - mood_great
  - mood_unhappy
  - bot_challenge

entities:
  - language

slots:
  language:
    type: text
    influence_conversation: true
    mappings:
      - type: from_text

responses:
  utter_greet:
    - condition:
        - type: slot
          name: language
          value: dialect
      text: "Me veka ne zokwe ne via, Na nia ya venne"

    - condition:
        - type: slot
          name: language
          value: pidgin
      text: "Hi! I dey here to hear you. How you dey feel today?"

    - condition:
        - type: slot
          name: language
          value: english
      text: "Hi! I'm here to listen. How are you feeling today?"

    - text: "Hey! How are you?"  # Fallback/default

  utter_cheer_up:
    - text: "Here is something to cheer you up:"
      image: "https://i.imgur.com/nGF1K8f.jpg"

  utter_did_that_help:
    - text: "Did that help you?"

  utter_happy:
    - text: "Great, carry on!"

  utter_goodbye:
    - text: "Bye"

  utter_iamabot:
    - text: "I am a bot, powered by Rasa."

actions:
  - action_detect_language

session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true


////rules //////////////////

version: "3.1"

rules:
  - rule: Greet and set language
    steps:
      - intent: greet
      - action: action_detect_language
      - action: utter_greet

  - rule: Say goodbye anytime the user says goodbye
    steps:
      - intent: goodbye
      - action: utter_goodbye

  - rule: Say 'I am a bot' anytime the user challenges
    steps:
      - intent: bot_challenge
      - action: utter_iamabot

  - rule: Respond in local dialect if slot is ya dey
    steps:
      - intent: greet
      - slot_was_set:
          - language: Ya dey
      - action: utter_greet

  - rule: Respond in pidgin if slot is how you dey
    steps:
      - intent: greet
      - slot_was_set:
          - language: How you dey
      - action: utter_greet

  ///////stories//////

  
- story: sad path 1
  steps:
  - intent: greet
  - action: utter_greet
  - intent: mood_unhappy
  - action: utter_cheer_up
  - action: utter_did_that_help
  - intent: affirm
  - action: utter_happy

- story: sad path 2
  steps:
  - intent: greet
  - action: utter_greet
  - intent: mood_unhappy
  - action: utter_cheer_up
  - action: utter_did_that_help
  - intent: deny
  - action: utter_goodbye
