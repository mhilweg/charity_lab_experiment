from otree.api import *
import time, json



EASY_SEQUENCES_OLD = [
    [1, 1, 4, 9, 1, 4, 9, 1],
    [4, 4, 9, 1, 4, 9, 1, 4],
    [9, 9, 1, 4, 9, 1, 4, 9],
    [1, 1, 9, 4, 1, 9, 4, 1],
    [4, 4, 1, 9, 4, 1, 9, 4],
    [9, 9, 4, 1, 9, 4, 1, 9],
    [1, 1, 4, 9, 1, 4, 9, 1],
    [4, 4, 9, 1, 4, 9, 1, 4],
    [9, 9, 1, 4, 9, 1, 4, 9],
    [1, 1, 9, 4, 1, 9, 4, 1],
]

EASY_SEQUENCES_CORRECT = [
    [1, 4, 1, 1, 1, 4, 9, 1],
    [1, 4, 9, 4, 4, 4, 9, 4],
    [9, 9, 9, 9, 1, 4, 1, 9],
    [1, 1, 4, 9, 1, 9, 1, 1],
    [9, 9, 1, 9, 9, 9, 4, 9],
    [1, 4, 4, 4, 4, 4, 9, 1],
    [1, 1, 1, 4, 1, 1, 9, 4],
    [4, 4, 4, 1, 4, 1, 4, 1],
    [4, 1, 1, 1, 1, 4, 9, 1],
    [9, 9, 1, 9, 1, 9, 9, 4],
    [1, 9, 9, 1, 9, 9, 9, 1],
    [4, 1, 4, 4, 9, 1, 4, 4],
    [1, 9, 1, 1, 1, 9, 4, 1],
    [4, 9, 9, 4, 9, 9, 9, 4],
    [9, 4, 1, 4, 4, 4, 1, 4],
    [4, 4, 1, 4, 4, 4, 1, 9],
    [1, 1, 1, 9, 1, 1, 4, 9],
    [4, 4, 9, 9, 9, 9, 1, 9],
    [4, 1, 9, 1, 1, 1, 1, 4],
    [1, 4, 9, 9, 9, 1, 9, 4],
    [1, 1, 9, 4, 1, 4, 1, 1],
    [4, 4, 9, 4, 4, 4, 9, 1],
    [4, 9, 4, 4, 1, 9, 4, 4],
    [1, 1, 9, 9, 9, 9, 4, 9],
    [9, 1, 4, 1, 1, 1, 1, 9],
    [4, 4, 4, 9, 4, 9, 4, 9],
    [9, 1, 9, 1, 9, 9, 9, 1],
    [1, 1, 4, 4, 4, 4, 4, 1],
    [9, 9, 1, 1, 1, 1, 1, 9],
    [9, 4, 9, 4, 9, 9, 9, 4],
    [1, 1, 9, 1, 1, 1, 9, 4],
    [9, 9, 9, 9, 4, 1, 4, 9],
    [9, 9, 4, 4, 4, 4, 4, 9],
    [1, 1, 4, 1, 1, 1, 4, 9],
    [9, 9, 4, 9, 9, 9, 1, 9],
    [4, 4, 4, 4, 1, 9, 9, 1],
]

EASY_SEQUENCES = [
    [1, 4, 1, 1, 1, 4, 9, 1],
    [1, 4, 9, 4, 4, 4, 9, 4],
    [9, 9, 9, 9, 1, 4, 1, 9],
    [1, 1, 4, 9, 1, 9, 1, 1],
    [9, 9, 1, 9, 9, 9, 4, 9],
    [1, 4, 4, 4, 4, 4, 9, 1],
    [1, 1, 1, 4, 1, 1, 9, 4],
    [4, 4, 4, 1, 4, 1, 4, 1],
    [4, 1, 1, 1, 1, 4, 9, 1],
    [9, 9, 1, 9, 1, 9, 9, 4],
    [1, 9, 9, 1, 9, 9, 9, 1],
    [4, 1, 4, 4, 9, 1, 4, 4],
    [1, 9, 1, 1, 1, 9, 4, 1],
    [4, 9, 9, 4, 9, 9, 9, 4],
    [9, 4, 1, 4, 4, 4, 1, 4],
    [4, 4, 1, 4, 4, 4, 1, 9],
    [1, 1, 1, 9, 1, 1, 4, 9],
    [4, 4, 9, 9, 9, 9, 1, 9],
    [4, 1, 9, 1, 1, 1, 1, 4],
    [1, 4, 9, 9, 9, 1, 9, 4],
    [1, 1, 9, 4, 1, 4, 1, 1],
    [4, 4, 9, 4, 4, 4, 9, 1],
    [4, 9, 4, 4, 1, 9, 4, 4],
    [1, 1, 9, 9, 9, 9, 4, 9],
    [9, 1, 4, 1, 1, 1, 1, 9],
    [4, 4, 4, 9, 4, 9, 4, 9],
    [9, 1, 9, 1, 9, 9, 9, 1],
    [1, 1, 4, 4, 4, 4, 4, 1],
    [9, 9, 1, 1, 1, 1, 1, 9],
    [9, 4, 9, 4, 9, 9, 9, 4],
    [1, 1, 9, 1, 1, 1, 9, 4],
]

HARD_SEQUENCES_OLD = [
    [1, 4, 9, 1, 4, 9, 1, 4],
    [1, 1, 4, 4, 9, 4, 9, 4],
    [9, 1, 1, 1, 4, 9, 9, 1],
    [4, 9, 9, 9, 1, 1, 4, 1],
    [1, 4, 4, 4, 9, 4, 9, 9],
    [9, 4, 1, 1, 4, 9, 9, 4],
    [4, 4, 9, 9, 1, 1, 4, 9],
    [9, 4, 4, 1, 4, 9, 9, 1],
    [4, 4, 4, 9, 1, 1, 4, 1],
    [1, 4, 1, 4, 1, 1, 4, 4],
]

HARD_SEQUENCES_CORRECT = [
    [4, 9, 1, 9, 4, 9, 4, 4],
    [1, 4, 9, 1, 4, 9, 1, 4],
    [4, 4, 1, 1, 9, 1, 4, 1],
    [4, 1, 4, 1, 9, 9, 1, 4],
    [1, 1, 1, 4, 9, 4, 9, 9],
    [1, 9, 4, 9, 1, 9, 1, 1],
    [9, 9, 9, 1, 4, 1, 1, 1],
    [4, 9, 9, 1, 4, 1, 9, 9],
    [1, 9, 9, 4, 1, 1, 1, 4],
    [1, 4, 1, 1, 9, 4, 4, 9],
    [9, 1, 9, 1, 9, 4, 1, 1],
    [9, 9, 4, 9, 1, 1, 4, 1],
    [9, 4, 4, 1, 9, 4, 1, 9],
    [4, 4, 4, 9, 1, 9, 1, 1],
    [4, 1, 9, 9, 1, 4, 9, 4],
    [1, 1, 9, 4, 4, 9, 9, 9],
    [4, 1, 4, 4, 9, 1, 1, 9],
    [4, 4, 4, 1, 9, 1, 9, 9],
    [9, 9, 9, 4, 1, 4, 4, 4],
    [9, 4, 4, 1, 9, 1, 4, 4],
    [9, 9, 1, 9, 4, 4, 1, 4],
    [4, 4, 9, 9, 1, 9, 4, 9],
    [1, 1, 4, 9, 9, 4, 4, 4],
    [4, 1, 9, 4, 1, 9, 4, 1],
    [1, 1, 1, 9, 4, 9, 4, 4],
    [4, 9, 9, 1, 4, 9, 1, 4],
    [1, 9, 1, 9, 1, 4, 9, 9],
    [9, 4, 1, 4, 9, 4, 9, 9],
    [9, 1, 4, 1, 9, 1, 9, 9],
    [9, 1, 1, 4, 9, 9, 9, 4],
    [1, 4, 9, 9, 4, 1, 9, 1],
    [4, 4, 1, 4, 1, 9, 1, 1],
    [1, 1, 9, 9, 4, 4, 1, 1],
    [9, 9, 4, 4, 1, 1, 4, 4],
    [9, 1, 9, 9, 9, 1, 4, 1],
    [1, 1, 4, 4, 1, 4, 1, 9],
]

HARD_SEQUENCES = [
    [4, 9, 1, 9, 4, 9, 4, 4],
    [1, 4, 9, 1, 4, 9, 1, 4],
    [4, 4, 1, 1, 9, 1, 4, 1],
    [4, 1, 4, 1, 9, 9, 1, 4],
    [1, 1, 1, 4, 9, 4, 9, 9],
    [1, 9, 4, 9, 1, 9, 1, 1],
    [9, 9, 9, 1, 4, 1, 1, 1],
    [4, 9, 9, 1, 4, 1, 9, 9],
    [1, 9, 9, 4, 1, 1, 1, 4],
    [1, 4, 1, 1, 9, 4, 4, 9],
    [9, 1, 9, 1, 9, 4, 1, 1],
    [9, 9, 4, 9, 1, 1, 4, 1],
    [9, 4, 4, 1, 9, 4, 1, 9],
    [4, 4, 4, 9, 1, 9, 1, 1],
    [4, 1, 9, 9, 1, 4, 9, 4],
    [1, 1, 9, 4, 4, 9, 9, 9],
    [4, 1, 4, 4, 9, 1, 1, 9],
    [4, 4, 4, 1, 9, 1, 9, 9],
    [9, 9, 9, 4, 1, 4, 4, 4],
    [9, 4, 4, 1, 9, 1, 4, 4],
    [9, 9, 1, 9, 4, 4, 1, 4],
    [4, 4, 9, 9, 1, 9, 4, 9],
    [1, 1, 4, 9, 9, 4, 4, 4],
    [4, 1, 9, 4, 1, 9, 4, 1],
    [1, 1, 1, 9, 4, 9, 4, 4],
    [4, 9, 9, 1, 4, 9, 1, 4],
    [1, 9, 1, 9, 1, 4, 9, 9],
    [9, 4, 1, 4, 9, 4, 9, 9],
    [9, 1, 4, 1, 9, 1, 9, 9],
    [9, 1, 1, 4, 9, 9, 9, 4],
    [1, 4, 9, 9, 4, 1, 9, 1],
]

SAMPLE_EASY_SEQUENCES_OLD = [
    {
        "sequence": [1, 1, 4, 9, 1, 4, 9, 1],
        "responses": [1, 9, 9, 4, 4, 1, 1],
    },
    {
        "sequence": [4, 4, 9, 1, 4, 9, 1, 4],
        "responses": [4, 1, 1, 9, 9, 4, 4],
    },
    {
        "sequence": [9, 9, 1, 4, 9, 1, 4, 9],
        "responses": [9, 4, 4, 1, 1, 9, 9],
    },
    {
        "sequence": [1, 1, 9, 4, 1, 9, 4, 1],
        "responses": [1, 4, 4, 9, 9, 1, 1],
    },
    {
        "sequence": [4, 4, 1, 9, 4, 1, 9, 4],
        "responses": [4, 9, 9, 1, 1, 4, 4],
    },
]

SAMPLE_EASY_SEQUENCES = [
    {
        "sequence": [1, 9, 9, 4, 9, 9, 9, 9],
        "responses": [4, 1, 9, 9, 9, 9, 9],
    },
    {
        "sequence": [9, 4, 4, 4, 9, 4, 4, 4],
        "responses": [1, 9, 1, 4, 4, 4, 4],
    },
    {
        "sequence": [1, 1, 1, 9, 1, 1, 1, 4],
        "responses": [1, 1, 4, 9, 4, 9, 1],
    },
    {
        "sequence": [9, 9, 1, 9, 1, 4, 9, 9],
        "responses": [9, 4, 1, 1, 9, 9, 9],
    },
    {
        "sequence": [4, 4, 4, 9, 1, 4, 4, 9],
        "responses": [4, 4, 1, 1, 9, 1, 4],
    },
]

SAMPLE_HARD_SEQUENCES = [
    {
        "sequence": [1, 4, 1, 4, 4, 9, 9, 1],
        "responses": [9, 4, 4, 4, 1, 4, 9],
    },
    {
        "sequence": [4, 1, 1, 4, 9, 9, 1, 4],
        "responses": [9, 9, 1, 4, 1, 1, 9],
    },
    {
        "sequence": [9, 9, 1, 1, 4, 4, 1, 1],
        "responses": [9, 4, 9, 1, 9, 4, 9],
    },
    {
        "sequence": [9, 1, 9, 9, 1, 4, 4, 1],
        "responses": [4, 1, 4, 9, 1, 9, 4],
    },
    {
        "sequence": [1, 1, 4, 4, 9, 9, 4, 4],
        "responses": [1, 9, 1, 4, 1, 9, 1],
    },
]

class Constants(BaseConstants):
    name_in_url = 'task_flow'
    players_per_group = None
    num_rounds = len(EASY_SEQUENCES) + len(HARD_SEQUENCES)
    easy_sequences = EASY_SEQUENCES
    hard_sequences = HARD_SEQUENCES
    #easy_correct_responses_OLD = [1, 4, 9, 1, 4, 9, 1, 4, 9, 1] # only seventh responses in here.
    #easy_correct_responses_correct = [1, 4, 9, 1, 9, 4, 1, 4, 1, 9, 9, 4, 1, 9, 4, 4, 1, 9, 1, 9, 1, 4, 4, 9, 1, 4, 9, 4, 1, 9, 1, 9, 4, 1, 9, 4] # one extra sequence for storing reasons
    easy_correct_responses = [1, 4, 9, 1, 9, 4, 1, 4, 1, 9, 9, 4, 1, 9, 4, 4, 1, 9, 1, 9, 1, 4, 4, 9, 1, 4, 9, 4, 1, 9, 1] # one extra sequence for storing reasons
    #hard_correct_responses_OLD = [9, 9, 9, 4, 1, 1, 1, 9, 4, 4]
    #hard_correct_responses_correct = [1, 9, 4, 9, 1, 4, 9, 1, 4, 9, 4, 9, 1, 4, 9, 1, 9, 4, 9, 1, 9, 4, 1, 9, 1, 1, 4, 1, 4, 4, 9, 4, 1, 9, 4, 1]
    hard_correct_responses = [1, 9, 4, 9, 1, 4, 9, 1, 4, 9, 4, 9, 1, 4, 9, 1, 9, 4, 9, 1, 9, 4, 1, 9, 1, 1, 4, 1, 4, 4, 9]
    sample_easy_sequences = SAMPLE_EASY_SEQUENCES
    sample_hard_sequences = SAMPLE_HARD_SEQUENCES
    total_time_seconds = 360  # 6 minutes per difficulty level
    freeze_time_seconds = 90  # 90 seconds freeze time duration
    bonus_per_correct_answer = 0.12
    number_of_tasks = 30

    task_instructions = f"""
    <h1>Welcome to the task! </h1>
    <p>
    In this task, you will work with sequences of eight numbers, which can be either 1, 4, or 9. 
    To facilitate your understanding, consider the sample picture below. The sequence of eight numbers is displayed with white boxes. 
    Below it, there are seven response boxes, with the first six being blue and the seventh one being green.
    </p>
    <p>
    Your goal is to apply specific rules to compute the <strong>final response for the seventh step</strong> of each sequence. 
    While you are free to input values into response boxes 1 to 6 as well, you must enter a value for the
    <strong>seventh response box</strong>, which is mandatory. This is the <strong>only response</strong> upon which we will determine 
    whether you solved the task correctly.
    </p>
    <p>
    Below, we teach you one method for solving this task, but it is just one of many possible ways. 
    <strong>You are free to use this method or any other</strong>, as only the correctness of your final answer determines your 
    bonus payment of <strong>{ bonus_per_correct_answer }€</strong> per correct response. There are <strong>hidden patterns</strong> to discover in the sequences that
    make it easier to find the correct seventh response.  
    </p>
     <!-- Sample Sequence Image -->
    <div style="text-align: center; margin: 20px 0;">
        <img src="/static/images/sample_sequence.png" alt="Task Instructions Illustration" style="max-width: 70%; height: auto; border: 2px solid #ddd; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
    </div>

    <p>
    You will play two versions of this task. Each version
    has a <strong>maximum of { number_of_tasks } sequences</strong>. Thus, you can earn a total bonus payment of up to 8.40€. Please pay close attention to the rules, as they 
    will guide you in solving the task.
    </p>
    <div style="margin-top: 20px; padding: 15px; border: 1px solid #d0e7ff; border-radius: 8px; background-color: #f5fff0;">
        <h3 style="color: #0056b3;">📋 Rules</h3>
        <ul style="list-style: none; padding: 0;">
            <li>✅ Only the numbers <strong>1</strong>, <strong>4</strong>, and <strong>9</strong> feature in the sequences and the responses.</li>
            <li>✅ If the two numbers that you have to compare are the same, the response is that same number.</li>
            <li>✅ If the two numbers are different, the response is the third number of the three numbers <strong>1</strong>, <strong>4</strong>, and <strong>9</strong>.</li>
        </ul>
    </div>
    <div style="margin-top: 20px; padding: 15px; border: 1px solid #ffe082; border-radius: 8px; background-color: #f5fff0;">
        <h3 style="color: #cc8c00;">🛠 Method #1</h3>
        <ul style="list-style: none; padding: 0;">
            <li>🔍 To compute the first response, compare the first two numbers of the sequence. If they are identical, the correct response is the very same number again. If they are different, input the one of the three numbers that is not present. For example, if you compare '1' and '4', the correct response is '9'.</li>
            <li>🔍 For the second response, compare the first response with the third number of the sequence. The third response is based on the comparison of the second response and the fourth number of the sequence, and so on.</li>
        </ul>
    </div>
    """

class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            participant = player.participant
            if not player.round_correctness:
                player.round_correctness = json.dumps({})
                print(f"Initialized round_correctness for Player {player.id_in_group}: {player.round_correctness}")
            
            if 'in_task2_phase' not in participant.vars:
                participant.vars['in_task2_phase'] = False

            participant.vars['final_round_correctness'] = {}  # Stores results from Task1
            participant.vars['final_round_correctness_task2'] = {}  # Stores results from Task2


           

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    round_correctness = models.LongStringField(initial=json.dumps({}))  # Start as an empty dictionary
    round_correctness_task2 = models.LongStringField(initial=json.dumps({}))  # Tracks correctness for Task2
    num_attempted = models.IntegerField(initial=0)

    response_1 = models.IntegerField(blank=True, max_value = 9)
    response_2 = models.IntegerField(blank=True, max_value = 9)
    response_3 = models.IntegerField(blank=True, max_value = 9)
    response_4 = models.IntegerField(blank=True, max_value = 9)
    response_5 = models.IntegerField(blank=True, max_value = 9)
    response_6 = models.IntegerField(blank=True, max_value = 9)
    response_7 = models.IntegerField(blank=False, max_value = 9)  # Mandatory

    answers_dict = models.LongStringField(initial="{}")  # Stores responses as a JSON string
    timestamps_dict = models.LongStringField(initial="{}")  # Stores timestamps as a JSON string

def get_timeout_seconds(player: Player):
    participant = player.participant
    return max(participant.vars['expiry'] - time.time(), 0)

def is_displayed(player: Player):
    return get_timeout_seconds(player) > 0

class InterimInstructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1  # Only display in the first round

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": False})
        total_time_minutes = Constants.total_time_seconds // 60 # make sure this is an integer value
        number_of_tasks = Constants.number_of_tasks
        return {
            'total_time_minutes': total_time_minutes,
            'instruction_points': [
                "There are some <strong>hidden patterns</strong> in the sequences that can be used to determine the correct seventh response more quickly.",
                "On the next page, you will see a set of sample sequences that follow the same logic as the ones you will have to solve. Use them to <strong>detect these patterns</strong>.",
                f"You have a total time budget of {total_time_minutes} minutes for looking at the sample sequences and solving <strong>{number_of_tasks} actual tasks</strong> for each of the two versions.",
                "When moving forward to playing the tasks, you can always inspect the sample sequences again through a pop-up button. In addition, you can always see <strong>all previously played sequences</strong>.",
                "The time starts to tick down once you click 'Next' on this page and move on to the sequence examples."
            ],
            'show_popups': show_popups,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Start the timer for the total task time
        participant = player.participant
        if 'expiry' not in participant.vars:
            participant.vars['expiry'] = time.time() + Constants.total_time_seconds

class SequenceExample(Page):
    timer_text = "Time remaining:"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1  # Only display in the first round

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        
        level_3_treatment = participant.vars.get('level_3_treatment', 'No freeze')
        freeze_enabled = level_3_treatment == 'Freeze'

        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": False})
        # Initialize difficulty level
        if 'difficulty_level' not in participant.vars:
            import random
            print(f"Assign difficulty level in task app:")
            participant.vars['difficulty_level'] = random.choice(['easy', 'hard'])
            print(f"Assign difficulty level in task app")

        # Fill the difficulty order dictionary
        if 'difficulty_order' not in participant.vars:
            participant.vars['difficulty_order'] = {
                1: participant.vars['difficulty_level'],
                2: 'hard' if participant.vars['difficulty_level'] == 'easy' else 'easy',
            }

        sample_sequences = (
            Constants.sample_easy_sequences if participant.vars['difficulty_level'] == "easy" else Constants.sample_hard_sequences
        )

        # Prepare sequences and responses
        formatted_samples = []
        for sample in sample_sequences:
            responses = [
                {"value": r, "highlight": idx == 6, "is_last": idx == len(sample["responses"]) - 1}
                for idx, r in enumerate(sample["responses"])
            ]
            formatted_samples.append({
                "sequence": ", ".join(map(str, sample["sequence"])),
                "responses": responses,
            })

        # Split samples into two columns
        left_column = formatted_samples[:3]  # First three examples
        right_column = [
            {"sequence": sample["sequence"], "responses": sample["responses"], "index": idx + 4}
            for idx, sample in enumerate(formatted_samples[3:])
        ]  # Add index offset for right column

        # Initialize timer
        if 'expiry' not in participant.vars:
            participant.vars['expiry'] = time.time() + Constants.total_time_seconds

        remaining_time = max(participant.vars['expiry'] - time.time(), 0)
        print(f"Remaining time passed to template: {remaining_time}")

        return {
            #'example_samples': formatted_samples,  # Pass structured sequences and responses
            'left_column': left_column,
            'right_column': right_column,
            'freeze_enabled': 'true' if freeze_enabled else 'false',
            'freeze_message': f"You can proceed to playing the task after {Constants.freeze_time_seconds} seconds. "
            "Use the time to find a pattern in the data that may make it easier for you to solve the subsequent exercises."
             if freeze_enabled else "",
            'remaining_time': remaining_time,
            'freeze_time': Constants.freeze_time_seconds,
            'show_popups': show_popups["instructions"] or show_popups["examples"],

            # Pass Constants explicitly to ensure templates have access
            'Constants': Constants,
        }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        # Examples pop-up is now active, instructions remain
        if participant.vars.get("show_popups"):
            participant.vars["show_popups"]["examples"] = True
        
        # Initialize counters based on the first difficulty level
        if 'count_rounds_task1' not in participant.vars:
            participant.vars['count_rounds_task1'] = (
                len(Constants.easy_sequences) if participant.vars['difficulty_level'] == 'easy' else len(Constants.hard_sequences)
            )
        if 'count_rounds_task2' not in participant.vars:
            participant.vars['count_rounds_task2'] = (
                len(Constants.hard_sequences) if participant.vars['difficulty_level'] == 'easy' else len(Constants.easy_sequences)
            )

        print(f"Initialized counters: count_rounds_task1={participant.vars['count_rounds_task1']}, count_rounds_task2={participant.vars['count_rounds_task2']}")

class Task(Page):
    form_model = 'player'
    form_fields = ['response_1', 'response_2', 'response_3', 'response_4', 'response_5', 'response_6', 'response_7', 'answers_dict', 'timestamps_dict']
        
    timer_text = "Time remaining:"
    get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (
            player.round_number <= Constants.num_rounds # redundant
            and not participant.vars.get('in_task2_phase', False)
        )

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        # Initialize answers and timestamps if not already set
        if not player.answers_dict:
            player.answers_dict = json.dumps({i: "NaN" for i in range(1, 8)})
        if not player.timestamps_dict:
            player.timestamps_dict = json.dumps({i: 0 for i in range(1, 8)})

        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": True})
        sequences = (
            Constants.easy_sequences if participant.vars['difficulty_level'] == "easy" else Constants.hard_sequences
        )

        correct_responses = (
            Constants.easy_correct_responses if participant.vars['difficulty_level'] == "easy" else Constants.hard_correct_responses
        )

        sample_sequences = (
        Constants.sample_easy_sequences if participant.vars['difficulty_level'] == "easy" else Constants.sample_hard_sequences
        )

        # Format example sequences for the pop-up
        formatted_samples = []
        for sample in sample_sequences:
            responses = []
            for idx, r in enumerate(sample["responses"]):
                responses.append({
                    "value": r,
                    "highlight": idx == 6,  # Highlight only the 7th response
                })
            formatted_samples.append({
                "sequence": ", ".join(map(str, sample["sequence"])),
                "responses": responses,
            })

        sequence = sequences[player.round_number - 1]

        history = []
        for i in range(player.round_number - 1):
            round_player = player.in_round(i + 1)
            current_sequence = sequences[i]
            correct_response = correct_responses[i]  # Retrieve pre-stored correct response

            responses = []
            for j in range(1, 8):
                response_value = round_player.field_maybe_none(f"response_{j}")
                responses.append({
                    "value": response_value,
                    "is_correct": j == 7 and response_value == correct_response,  # Only the seventh box is checked
                })

            history.append({
                "sequence": current_sequence,
                "responses": responses,
            })

        # Turn history upside down to display the most recent entry on top
        reversed_history = history[::-1]

        remaining_time = max(participant.vars['expiry'] - time.time(), 0)

        return {
            'sequence': sequence,
            'sequence_index': player.round_number,
            'number_of_tasks': Constants.number_of_tasks,
            'difficulty_level': participant.vars['difficulty_level'],
            'history': reversed_history,
            'remaining_time': remaining_time,  # Remaining time in seconds
            'example_samples': formatted_samples,
            'show_popups': show_popups["instructions"] or show_popups["examples"],
            'answers': json.loads(player.answers_dict),
            'timestamps': json.loads(player.timestamps_dict),
            'Constants': Constants, # Pass Constants explicitly to ensure templates have access
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        print(f"Before Update: {json.loads(player.round_correctness)}")

        correct_responses = (
            Constants.easy_correct_responses if participant.vars['difficulty_level'] == "easy" else Constants.hard_correct_responses
        )
        correct_response = correct_responses[player.round_number - 1]

        # Check if the 7th response is correct
        is_correct = 1 if player.response_7 == correct_response else 0

        # Step 1: Propagate round_correctness from the previous round
        if player.round_number > 1:  # Skip for the first round
            previous_player = player.in_round(player.round_number - 1)
            player.round_correctness = previous_player.round_correctness

        # Fetch the current dictionary and add the current round's result
        correctness_dict = json.loads(player.round_correctness) if player.round_correctness else {}
        print(f"Round {player.round_number} - Retrieved round_correctness: {correctness_dict}")

        correctness_dict[player.round_number] = is_correct  # Add or update the entry for the current round
        print(f"Round {player.round_number} - Updated round_correctness: {correctness_dict}")

        player.round_correctness = json.dumps(correctness_dict)  # Save back to the field
        print(f"Round {player.round_number} - Saved round_correctness: {player.round_correctness}")


        print(f"Updated Round Correctness: {player.round_correctness}")

        player.num_attempted += 1

        if player.round_number == len(Constants.easy_sequences) and participant.vars['difficulty_level'] == "easy":
            participant.vars['difficulty_level'] = "hard"
            participant.vars['expiry'] = time.time() + Constants.total_time_seconds

        # Save answers_dict and timestamps_dict
        answers = json.loads(player.answers_dict) if player.answers_dict else {}
        timestamps = json.loads(player.timestamps_dict) if player.timestamps_dict else {}

        # Debugging: Log received data
        print(f"Received Answers Dict: {answers}")
        print(f"Received Timestamps Dict: {timestamps}")
        print(f"After Update: {json.loads(player.round_correctness)}")

        player.answers_dict = json.dumps(answers)
        player.timestamps_dict = json.dumps(timestamps)

        last_task = player.round_number == (participant.vars['count_rounds_task1'] - 1)  # Check if this is the last task
        timer_expired = time.time() >= participant.vars.get('expiry', 0)

        if last_task or timer_expired:
            participant.vars['show_transition'] = True  # Flag to show Transition page
            participant.vars['completed_rounds_in_task1'] = player.round_number
            participant.vars['final_round_correctness'] = json.dumps(correctness_dict)
            print(f"Final round_correctness (Task 1): {participant.vars['final_round_correctness']}")
            print(f"Task - Completed Rounds in Task1: {participant.vars['completed_rounds_in_task1']}")
        else:
            participant.vars['show_transition'] = False
        
        print(f"Task - Player round_number: {player.round_number}, count_rounds_task1: {participant.vars['count_rounds_task1']}")

      

class Transition(Page):

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (
            participant.vars.get('show_transition', False)
            and not participant.vars.get('in_task2_phase', False))
    
    def vars_for_template(player: Player):
            participant = player.participant
            print(f"Transition: show_transition {participant.vars.get('show_transition')} and in_task2_phase {participant.vars.get('in_task2_phase')}")
            # Retrieve or default `show_popups`
            show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": True})


            # Get the current difficulty level
            current_difficulty = participant.vars.get('difficulty_level', None)
            if not current_difficulty:
                raise ValueError("current_difficulty is not set in participant.vars")

            # Determine the next difficulty
            next_difficulty = "hard" if current_difficulty == "easy" else "easy"

            # Debugging logs (optional)
            print(f"Transition Page: current_difficulty={current_difficulty}, next_difficulty={next_difficulty}")

            return {
                "current_difficulty": current_difficulty,
                "next_difficulty": next_difficulty,
                "show_popups": show_popups,
        }


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        print(f"Before Transition: round_number={player.round_number}, difficulty_level={participant.vars.get('difficulty_level')}")
        print(f"Participant vars: {participant.vars}")
        participant.vars['sequence_count'] = 0

        # Mark the transition as complete
        #participant.vars['show_transition'] = False
        if 'in_task2_phase' not in participant.vars:
            participant.vars['in_task2_phase'] = False
        print(f"End of Tr: Show_transition:{participant.vars['show_transition']}, in_task2_phase:{participant.vars['in_task2_phase']}")

        # Reset the difficulty level for the second phase
        participant.vars['difficulty_level'] = (
            'hard' if participant.vars['difficulty_level'] == 'easy' else 'easy'
        )

        # Get the current difficulty level
        current_difficulty = participant.vars.get('difficulty_level', None)
        if not current_difficulty:
            raise ValueError("current_difficulty is not set in participant.vars")

        # Determine the next difficulty
        next_difficulty = "hard" if current_difficulty == "easy" else "easy"
        participant.vars['expiry'] = time.time() + Constants.total_time_seconds
        print(f"Expiry set for next sequence: {participant.vars['expiry']}")

        return {
            "current_difficulty": current_difficulty,
            "next_difficulty": next_difficulty,
            "expiry": participant.vars['expiry'],  # Add expiry time for debugging or display
        }

class SequenceExample2(Page):
    timer_text = "Time remaining:"

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.vars.get('show_transition', False) and not participant.vars.get('in_task2_phase', False))

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        print(f"Start of SE2: Show_transition:{participant.vars['show_transition']}, in_task2_phase:{participant.vars['in_task2_phase']}")

        level_3_treatment = participant.vars.get('level_3_treatment', 'No freeze')
        freeze_enabled = participant.vars.get('level_3_treatment') == 'Freeze'

        sample_sequences = (
            Constants.sample_hard_sequences
            if participant.vars.get('difficulty_level') == 'hard'
            else Constants.sample_easy_sequences
        )

        formatted_samples = []
        for sample in sample_sequences:
            responses = [
                {"value": r, "highlight": idx == 6, "is_last": idx == len(sample["responses"]) - 1}
                for idx, r in enumerate(sample["responses"])
            ]
            formatted_samples.append({
                "sequence": ", ".join(map(str, sample["sequence"])),
                "responses": responses,
            })

        # Split samples into two columns
        left_column = formatted_samples[:3]  # First three examples
        right_column = [
            {"sequence": sample["sequence"], "responses": sample["responses"], "index": idx + 4}
            for idx, sample in enumerate(formatted_samples[3:])
        ]  # Add index offset for the right column

        # Calculate remaining time
        remaining_time = max(participant.vars['expiry'] - time.time(), 0)

        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": True})
        sequence_index = 1

        return {
            'left_column': left_column,
            'right_column': right_column,
            'freeze_enabled': 'true' if freeze_enabled else 'false',
            'freeze_message': f"You can proceed to playing the task after {Constants.freeze_time_seconds} seconds. Use the time to find a pattern in the data that may make it easier for you to solve the subsequent exercises." if level_3_treatment == 'Freeze' else "",
            'remaining_time': Constants.total_time_seconds,
            'freeze_time': Constants.freeze_time_seconds,
            'show_popups': show_popups,
            'Constants': Constants,
            'sequence_index': sequence_index,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.vars['show_transition'] = False
        participant.vars['in_task2_phase'] = True

        print(f"End of SE2: Show_transition: {participant.vars['show_transition']}, in_task2_phase: {participant.vars['in_task2_phase']}, expiry: {participant.vars['expiry']}")

class Task2(Page):
    form_model = 'player'
    form_fields = ['response_1', 'response_2', 'response_3', 'response_4', 'response_5', 'response_6', 'response_7', 'answers_dict', 'timestamps_dict']

    timer_text = "Time remaining:"
    get_timeout_seconds = get_timeout_seconds
    
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.vars.get('next_app', False):
            return False
        return participant.vars.get('in_task2_phase', False)

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        print(f"Start of T2:Show_transition:{participant.vars['show_transition']}, in_task2_phase:{participant.vars['in_task2_phase']}")

        # Retrieve the number of rounds completed in Task1
        completed_rounds_in_task1 = participant.vars.get('completed_rounds_in_task1', 0)

        sequence_count = participant.vars.get('sequence_count', 0)

        # Validate sequence_count
        if sequence_count < 0 or sequence_count > len(Constants.hard_sequences):
            raise ValueError(f"Invalid sequence_count: {sequence_count}. Check logic.")

        # Debugging Logs
        print(f"Task2 - Completed Rounds in Task1: {completed_rounds_in_task1}")
        print(f"Task2 - Current round_number: {player.round_number}")
        print(f"Task2 - Sequence_count: {sequence_count}")

        # Initialize answers_dict and timestamps_dict
        if not player.answers_dict:
            player.answers_dict = json.dumps({str(i): "NaN" for i in range(1, 8)})
        if not player.timestamps_dict:
            player.timestamps_dict = json.dumps({str(i): 0 for i in range(1, 8)})

 
        sequences = (
            Constants.hard_sequences
            if participant.vars.get('difficulty_level') == 'hard'
            else Constants.easy_sequences
        )
        sequence = sequences[sequence_count]
        print(sequence)

        # Prepare example sequences for the modal
        sample_sequences = (
            Constants.sample_hard_sequences
            if participant.vars.get('difficulty_level') == 'hard'
            else Constants.sample_easy_sequences
        )

        formatted_samples = []
        for sample in sample_sequences:
            responses = [
                {"value": r, "highlight": idx == 6, "is_last": idx == len(sample["responses"]) - 1}
                for idx, r in enumerate(sample["responses"])
            ]
            formatted_samples.append({
                "sequence": ", ".join(map(str, sample["sequence"])),
                "responses": responses,
            })

        # Prepare history
        history = []
        for i in range(completed_rounds_in_task1, player.round_number):
            #round_player = player.in_round(i + 1)
            round_player = player.in_round(i)

            # Correct sequence index for Task2
            sequence_task2_index = i - completed_rounds_in_task1
            sequence_task2 = sequences[sequence_task2_index]
            correct_response_task2 = (
                Constants.hard_correct_responses[sequence_task2_index]
                if participant.vars.get('difficulty_level') == 'hard'
                else Constants.easy_correct_responses[sequence_task2_index]
            )


            responses = [
                {
                    "value": round_player.field_maybe_none(f"response_{j}"),
                    "is_correct": j == 7 and round_player.field_maybe_none(f"response_{j}") == correct_response_task2,
                }
                for j in range(1, 8)
            ]

            history.append({
                "sequence": sequence_task2,
                "responses": responses,
            })

        remaining_time = max(participant.vars['expiry'] - time.time(), 0)
        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": True})
        reversed_history = history[::-1]

        return {
            'sequence': sequence,
            'sequence_count': sequence_count + 1,
            'number_of_tasks': Constants.number_of_tasks,
            'answers': json.loads(player.answers_dict),
            'timestamps': json.loads(player.timestamps_dict),
            'example_samples': formatted_samples,
            'history': reversed_history,
            'difficulty_level': participant.vars['difficulty_level'],
            'remaining_time': remaining_time,
            'show_popups': show_popups,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant

        # Validate and save JSON fields
        if not player.answers_dict:
            player.answers_dict = json.dumps({str(i): "NaN" for i in range(1, 8)})
        if not player.timestamps_dict:
            player.timestamps_dict = json.dumps({str(i): 0 for i in range(1, 8)})

        is_task2_phase = participant.vars.get('in_task2_phase', False)

        correct_responses = (
            Constants.hard_correct_responses
            if participant.vars.get('difficulty_level') == 'hard'
            else Constants.easy_correct_responses
        )

        # Calculate the round number relative to Task2
        completed_rounds_task1 = participant.vars.get('completed_rounds_in_task1', 0)
        task2_round_number = player.round_number - completed_rounds_task1 + 1

        if task2_round_number <= 0 or task2_round_number > len(correct_responses):
                raise ValueError(f"Invalid task2_round_number: {task2_round_number}. Check logic.")

        # Get the correct response for this round
        correct_response = correct_responses[task2_round_number - 1]


        # Check correctness
        is_correct = 1 if player.response_7 == correct_response else 0

        if player.round_number > completed_rounds_task1:  # Only applicable for rounds beyond the first in Task2
            previous_player = player.in_round(player.round_number - 1)
            previous_correctness = json.loads(previous_player.round_correctness_task2 or "{}")
        else:
            previous_correctness = {}

        # Update the dictionary with the current round's result
        previous_correctness[task2_round_number] = is_correct
        player.round_correctness_task2 = json.dumps(previous_correctness)
        

        # Save back JSON fields
        player.answers_dict = json.dumps(json.loads(player.answers_dict))
        player.timestamps_dict = json.dumps(json.loads(player.timestamps_dict))
        print(f"Task2 - Before Save: answers_dict={player.answers_dict}, timestamps_dict={player.timestamps_dict}")

        timer_expired = time.time() >= participant.vars.get('expiry', 0)

        participant.vars['sequence_count'] = participant.vars.get('sequence_count', 0) + 1

        #if task2_round_number == participant.vars['count_rounds_task2']:
         #   participant.vars['final_round_correctness_task2'] = json.loads(participant.vars['round_correctness_task2'])
          #  print(f"Task 2 - final round correctness: {participant.vars['final_round_correctness_task2']}")
        
        print(f"Player.round_number:{player.round_number}, Sum of count rounds: {participant.vars['completed_rounds_in_task1'] + participant.vars['count_rounds_task2']} ")
        max_rounds_reached = participant.vars['sequence_count'] >= (participant.vars['count_rounds_task2'] - 1)

        player.num_attempted += 1

        print(f"Task2 - Player round_number: {player.round_number}, count_rounds_task2: {participant.vars['count_rounds_task2']}")


        # Handle app transition
        if timer_expired or max_rounds_reached:
            participant.vars['final_round_correctness_task2'] = json.dumps(previous_correctness)
            print(f"Final round_correctness_task2 (Task 2): {participant.vars['final_round_correctness_task2']}")
            print(f"Transitioning to the next app. Timer expired: {timer_expired}, Max rounds reached: {max_rounds_reached}")
            participant.vars['next_app'] = True
            return

page_sequence = [InterimInstructions, SequenceExample, Task, Transition, SequenceExample2, Task2]
