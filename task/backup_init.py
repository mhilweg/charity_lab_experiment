from otree.api import *
import time, json



EASY_SEQUENCES = [
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

HARD_SEQUENCES = [
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

SAMPLE_EASY_SEQUENCES = [
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

SAMPLE_HARD_SEQUENCES = [
    {
        "sequence": [1, 4, 9, 1, 4, 9, 1, 4],
        "responses": [9, 9, 4, 4, 1, 1, 9],
    },
    {
        "sequence": [1, 1, 4, 4, 9, 4, 9, 4],
        "responses": [1, 9, 1, 4, 4, 1, 9],
    },
    {
        "sequence": [9, 1, 1, 1, 4, 9, 9, 1],
        "responses": [4, 9, 4, 4, 1, 4, 9],
    },
    {
        "sequence": [4, 9, 9, 9, 1, 1, 4, 1],
        "responses": [1, 4, 1, 1, 1, 9, 4],
    },
    {
        "sequence": [1, 4, 4, 4, 9, 4, 9, 9],
        "responses": [9, 1, 9, 9, 1, 4, 1],
    },
]

class Constants(BaseConstants):
    name_in_url = 'task_flow'
    players_per_group = None
    num_rounds = len(EASY_SEQUENCES) + len(HARD_SEQUENCES)
    easy_sequences = EASY_SEQUENCES
    hard_sequences = HARD_SEQUENCES
    easy_correct_responses = [1, 4, 9, 1, 4, 9, 1, 4, 9, 1]
    hard_correct_responses = [9, 9, 9, 4, 1, 1, 1, 9, 4, 4]
    sample_easy_sequences = SAMPLE_EASY_SEQUENCES
    sample_hard_sequences = SAMPLE_HARD_SEQUENCES
    total_time_seconds = 30  # 2 minutes per difficulty level

    task_instructions = """
    <p>Welcome to the task! In this real-effort task, you will be given a sequence of eight numbers.</p>
                <p>Your goal is to apply specific rules to compute the response for the seventh step. 
                While you are free to input values into response boxes 1 to 6 as well, you must enter a value for the seventh response box, which is mandatory. This is the only response upon which we will determine whether you solved the task correctly. 
                Please pay attention to the rules, as they determine your task performance.</p>
                <p>The rules are as follows:</p>
                <ol>
                    <li>Only the numbers 1, 4, and 9 feature in the sequences and the responses.</li>
                    <li>If the two numbers that you have to compare are the same, the response is that same number.</li>
                    <li>If the two numbers are different, the response is the third number of the three numbers 1, 4, and 9.</li>
                </ol>
                <p>While there are multiple ways to solve this task, we will demonstrate only one method. You are free to use this method or any other: only the correctness of your final answer determines your bonus payment of Z.XY€ per correct response.
                <p><strong>Method</strong></p>
                <ol>
                    <li>To compute the first response, you have to compare the first two numbers of the sequence. If they are identical, the correct response is the very same number again. If they are different, you have to input the one of the three numbers that is not present, i.e. if you compare '1' and '4', the correct response is '9'.</li>
                    <li>For the second response, you have to compare the first response with the third number of the sequence; response 3 then is based on the comparison of response 2 and the fourth number of the sequence, and so on.</li>
                </ol>
                <p>Below you find a sample sequence with the corresponding responses that underscores this method.</p>
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

           

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    round_correctness = models.LongStringField(initial=json.dumps({}))  # Start as an empty dictionary
    round_correctness_task2 = models.LongStringField(initial=json.dumps({}))  # Tracks correctness for Task2
    num_attempted = models.IntegerField(initial=0)

    response_1 = models.IntegerField(blank=True)
    response_2 = models.IntegerField(blank=True)
    response_3 = models.IntegerField(blank=True)
    response_4 = models.IntegerField(blank=True)
    response_5 = models.IntegerField(blank=True)
    response_6 = models.IntegerField(blank=True)
    response_7 = models.IntegerField(blank=False)  # Mandatory

    task1_responses = models.LongStringField(initial=json.dumps({}))  # Stores Task 1 responses
    task2_responses = models.LongStringField(initial=json.dumps({}))  # Stores Task 2 responses

    answers_dict = models.LongStringField(initial="{}")  # Stores responses as a JSON string
    timestamps_dict = models.LongStringField(initial="{}")  # Stores timestamps as a JSON string

def get_timeout_seconds(player: Player):
    participant = player.participant
    return max(participant.vars['expiry'] - time.time(), 0)

def is_displayed(player: Player):
    return get_timeout_seconds(player) > 0

class SequenceExample(Page):
    timer_text = "Time remaining:"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1  # Only display in the first round

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": False})
        # Initialize difficulty level
        if 'difficulty_level' not in participant.vars:
            import random
            participant.vars['difficulty_level'] = random.choice(['easy', 'hard'])
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

        # Initialize timer
        if 'expiry' not in participant.vars:
            participant.vars['expiry'] = time.time() + Constants.total_time_seconds

        remaining_time = max(participant.vars['expiry'] - time.time(), 0)

        return {
            'example_samples': formatted_samples,  # Pass structured sequences and responses
            'remaining_time': remaining_time,  # Remaining time in seconds
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

        remaining_time = max(participant.vars['expiry'] - time.time(), 0)

        return {
            'sequence': sequence,
            'sequence_index': player.round_number,
            'difficulty_level': participant.vars['difficulty_level'],
            'history': history,
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

        last_task = player.round_number == participant.vars['count_rounds_task1']  # Check if this is the last task
        timer_expired = time.time() >= participant.vars.get('expiry', 0)

        if last_task or timer_expired:
            participant.vars['show_transition'] = True  # Flag to show Transition page
            participant.vars['completed_rounds_in_task1'] = player.round_number
            print(f"Task - Completed Rounds in Task1: {participant.vars['completed_rounds_in_task1']}")
        else:
            participant.vars['show_transition'] = False
      

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

        # Calculate remaining time
        remaining_time = max(participant.vars['expiry'] - time.time(), 0)

        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": True})
        sequence_index = 1

        return {
            'example_samples': formatted_samples,
            'remaining_time': remaining_time,  # Pass the calculated remaining time
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

        return {
            'sequence': sequence,
            'sequence_count': sequence_count + 1,
            'answers': json.loads(player.answers_dict),
            'timestamps': json.loads(player.timestamps_dict),
            'example_samples': formatted_samples,
            'history': history,
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

        if 'round_correctness_task2' not in participant.vars:
            participant.vars['round_correctness_task2'] = json.dumps({})  # Initialize if not already set

        correctness_dict = json.loads(participant.vars.get('round_correctness_task2', '{}'))
        correctness_dict[task2_round_number] = is_correct
        participant.vars['round_correctness_task2'] = json.dumps(correctness_dict)
        print(f"Updated round_correctness_task2: {participant.vars['round_correctness_task2']}")

        # Save back JSON fields
        player.answers_dict = json.dumps(json.loads(player.answers_dict))
        player.timestamps_dict = json.dumps(json.loads(player.timestamps_dict))
        print(f"Task2 - Before Save: answers_dict={player.answers_dict}, timestamps_dict={player.timestamps_dict}")

        timer_expired = time.time() >= participant.vars.get('expiry', 0)

        participant.vars['sequence_count'] = participant.vars.get('sequence_count', 0) + 1


        print(f"Player.round_number:{player.round_number}, Sum of count rounds: {participant.vars['completed_rounds_in_task1'] + participant.vars['count_rounds_task2']} ")
        max_rounds_reached = participant.vars['sequence_count'] >= participant.vars['count_rounds_task2']

        # Handle app transition
        if timer_expired or max_rounds_reached:
            print(f"Transitioning to the next app. Timer expired: {timer_expired}, Max rounds reached: {max_rounds_reached}")
            participant.vars['next_app'] = True
            return

page_sequence = [SequenceExample, Task, Transition, SequenceExample2, Task2]
