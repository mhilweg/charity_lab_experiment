from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'comprehension_test'
    players_per_group = None  
    num_rounds = 1  
    bonus_per_correct_answer = 0.15

    comprehension_questions = [
        {
            'question': "If two numbers being compared are the same, what is the correct response?",
            'choices': ["The same number", "The third number in the set", "The sum of the two numbers"],
            'correct': "The same number"
        },
        {
            'question': "If two numbers being compared are different, what is the correct response?",
            'choices': ["The larger number", "The smaller number", "The third number in the set"],
            'correct': "The third number in the set"
        },
        {
            'question': "What is the goal of the task?",
            'choices': [
                "To enter all correct values into all seven response boxes",
                "To enter the correct value into the seventh response box",
                "To calculate the sum of all eight numbers"
            ],
            'correct': "To enter the correct value into the seventh response box"
        }
    ]
    task_instructions = f"""
    <h1>Welcome to the task! </h1>
    <p>
    In this task, you will work with sequences of eight numbers, which can be either <strong>1, 4, or 9</strong>. 
    Your goal is to apply specific rules to compute the <strong>final response for the seventh step</strong> of each sequence.
    While you are free to input values into response boxes <strong>1 to 6</strong>, you must enter a value for the 
    <strong>seventh response box</strong>, which is <strong>mandatory</strong>. This is the <strong>only response</strong> upon which we will determine 
    whether you solved the task correctly.
    </p>
    <p>
    Below, we teach you one method for solving this task, but it is just <strong>one of many possible ways</strong>. 
    <strong>You are free to use this method or any other</strong>, as only the correctness of your <strong>final answer</strong> determines your 
    bonus payment of <strong>{ bonus_per_correct_answer }€</strong> per correct response. Please pay close attention to the rules, as they 
    will guide you in solving the task.
    </p>
    <!-- Sample Sequence Image -->
    <div style="text-align: center; margin: 20px 0;">
        <img src="/static/images/sample_sequence.png" alt="Task Instructions Illustration" style="max-width: 70%; height: auto; border: 2px solid #ddd; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
    </div>

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
    <br>
    <p><em>You can always access these instructions on the subsequent pages through clicking the 'Task Instructions' button in the top right corner.</p>
    """





class Subsession(BaseSubsession):
    def creating_session(self):
        pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    failed_attempts = models.IntegerField(initial=0)
    q1 = models.StringField()
    q2 = models.StringField()
    q3 = models.StringField()

# Function to track popup usage
def track_popup_usage(participant, page_name, popup_name):
    """Tracks popup button usage and stores it in participant.vars."""
    if 'popup_usage' not in participant.vars:
        participant.vars['popup_usage'] = {}  # Initialize storage
    if page_name not in participant.vars['popup_usage']:
        participant.vars['popup_usage'][page_name] = []  # Initialize page tracking

    # Add the popup name to the page's tracking list
    participant.vars['popup_usage'][page_name].append(popup_name)


# Custom route to handle AJAX requests for popup tracking
from django.http import JsonResponse
import json

def track_popup_usage_view(request):
    """Handles AJAX calls to track popup button clicks."""
    if request.method == 'POST':
        data = json.loads(request.body)
        popup_name = data.get('popup_name')
        page_name = data.get('page_name')
        print(f"Popup Name: {popup_name}, Page Name: {page_name}")

        # Fetch participant and update usage tracking
        participant = request.user.participant
        track_popup_usage(participant, page_name, popup_name)
        print(f"Participant Popup Usage: {participant.vars.get('popup_usage', {})}")
        return JsonResponse({'status': 'success'})
    
        


custom_routes = {
    'track_popup_usage': track_popup_usage_view,
}

class Introduction(Page):
    @staticmethod
    def is_displayed(player):
        return True  # Ensure this is the first page.

    @staticmethod
    def vars_for_template(player):
        return {
            "tax_rate": 30,
            'base_pay': 5,
            "charity_focus": "fighting child labour, poverty, and discrimination of girls and women in developing countries",
        }

class TaskInstructions(Page):
    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        
        return {
            'instructions': Constants.task_instructions,
            'difficulty_level': participant.vars.get("difficulty_level"),
            'bonus_per_correct_answer': Constants.bonus_per_correct_answer,
        }
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        # Disable all pop-ups
        participant.vars["show_popups"] = {"instructions": True, "examples": False}



class ComprehensionQuestions1(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3']

    def vars_for_template(player):
        questions = []
        for i, question in enumerate(Constants.comprehension_questions, start=1):
            question_data = question.copy()
            question_data['name'] = f'q{i}'
            questions.append(question_data)

        participant = player.participant    
        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": False})
        return {"show_popups": show_popups["instructions"] or show_popups["examples"],
                'questions': questions,
                'difficulty_level': participant.vars.get("difficulty_level"),
                'Constants': Constants,}

    def before_next_page(player, timeout_happened):
        correct_answers = [q['correct'] for q in Constants.comprehension_questions]
        player.participant.vars['first_attempt_failed'] = False  # Default
        
        for i, correct in enumerate(correct_answers, start=1):
            answer = getattr(player, f'q{i}')
            if answer != correct:
                player.participant.vars['first_attempt_failed'] = True
                player.participant.vars[f'q{i}_feedback'] = "incorrect"
            else:
                player.participant.vars[f'q{i}_feedback'] = "correct"

        if player.participant.vars['first_attempt_failed']:
            player.failed_attempts = 1



class ComprehensionQuestions2(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3']

    def vars_for_template(player):
        correct_answers = [q['correct'] for q in Constants.comprehension_questions]
        questions = []
        for i, question in enumerate(Constants.comprehension_questions, start=1):
            question_data = question.copy()
            question_data['name'] = f'q{i}'
            question_data['stored_answer'] = getattr(player, f'q{i}', '')

            # Add feedback: was the previous answer correct or incorrect?
            previous_answer = getattr(player, f'q{i}', None)
            question_data['feedback'] = (
                "correct" if previous_answer == correct_answers[i - 1] else "incorrect"
            )
            questions.append(question_data)
        participant = player.participant    
        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": False})
        return {"show_popups": show_popups["instructions"] or show_popups["examples"],
                'difficulty_level': participant.vars.get("difficulty_level"),
                'questions': questions}


    def before_next_page(player, timeout_happened):
        correct_answers = [q['correct'] for q in Constants.comprehension_questions]
        all_correct = True

        for i, correct in enumerate(correct_answers, start=1):
            answer = getattr(player, f'q{i}')
            if answer != correct:
                all_correct = False

        if not all_correct:
            player.participant.vars['redirect_to_clarification'] = True
        else:
            player.participant.vars['redirect_to_clarification'] = False

    def is_displayed(player):
        return player.failed_attempts == 1


class ComprehensionClarification(Page):
    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": False})
        questions = []
        for question in Constants.comprehension_questions:
            question_data = question.copy()
            question_data['highlighted_correct'] = question['correct']
            questions.append(question_data)

        return {
            'questions': questions,
            'show_popups': show_popups,
            }

    @staticmethod
    def is_displayed(player):
        return player.participant.vars.get('redirect_to_clarification', False)

class PracticePage(Page):
    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        show_popups = participant.vars.get("show_popups", {"instructions": True, "examples": False})
        # Sequences and correct responses for the practice page
        practice_sequences = [
            {
                'sequence': [1, 4, 9, 1],
                'correct_responses': [9, 9, 4]
            },
            {
                'sequence': [4, 4, 9, 1],
                'correct_responses': [4, 1, 1]
            }
        ]
        return {
            'practice_sequences': practice_sequences,
            'show_popups': show_popups,
        }


page_sequence = [Introduction, TaskInstructions, ComprehensionQuestions1, ComprehensionQuestions2,
                 ComprehensionClarification, PracticePage]
