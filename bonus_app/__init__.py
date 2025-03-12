from otree.api import *
import json

class Constants(BaseConstants):
    name_in_url = 'bonus_app'
    players_per_group = None
    num_rounds = 1  # Two pages: bonus calculation and deduction
    base_payment = 5  # Base payment
    bonus_per_correct_answer = 0.25  # Bonus for each correct answer
    tax_rate = 0.30  # Flat tax rate (30%)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    total_correct = models.IntegerField(initial=0)  # Total correct answers across tasks
    bonus_before_tax = models.FloatField(initial=0)  # Bonus before taxation
    net_earnings_after_tax = models.FloatField(initial=0)  # Earnings after tax
    donated_amount = models.FloatField(initial=0.0)  # Amount donated with two decimal places
    reimbursement_amount = models.FloatField(initial=0.0)  # Tax reimbursement for donation
    net_earnings_after_donation = models.FloatField(initial=0.0)
    deduct_donation = models.BooleanField()  # Whether the participant wants to deduct the donation
    button_pressed = models.StringField(choices=["Proceed without Donating", "Donate"], blank=True)
    entered_password = models.StringField(blank=True)  # Stores the password entered by the participant

    belief_donation_percentage = models.FloatField(
        label="What percentage of participants do you think donated?",
        min=0,
        max=100
    )
    belief_deduction_percentage = models.FloatField(
        label="What percentage of donors do you think deducted their donation?",
        min=0,
        max=100
    )


    # Page (i) responses
    donation_decision_reason = models.LongStringField(label='What was driving your donation decision?')
    deduction_decision_reason = models.LongStringField(label='What was driving your deduction decision?')

    # Pages (ii) & (iii) task-related responses
    task_1_pattern_attempt = models.StringField(
        label='Did you try to discover the hidden pattern or did you only use the method provided?',
        choices=[
            'I tried to discover the hidden pattern and failed.',
            'I tried to discover the hidden pattern and succeeded.',
            'I did not bother looking for the pattern; I focused on using the method provided.'
        ],
        widget=widgets.RadioSelect
    )
    task_1_strategy = models.LongStringField(blank=True, label='What was your strategy to discover the pattern?')
    task_1_guess_pattern = models.LongStringField(blank=True, label='Please describe your guess of the pattern.')
    task_1_reason_no_attempt = models.LongStringField(blank=True, label='Why did you not bother looking for the pattern?')

    task_2_pattern_attempt = models.StringField(
        label='Did you try to discover the hidden pattern or did you only use the method provided?',
        choices=[
            'I tried to discover the hidden pattern and failed.',
            'I tried to discover the hidden pattern and succeeded.',
            'I did not bother looking for the pattern; I focused on using the method provided.'
        ],
        widget=widgets.RadioSelect
    )
    task_2_strategy = models.LongStringField(blank=True, label='What was your strategy to discover the pattern?')
    task_2_guess_pattern = models.LongStringField(blank=True, label='Please describe your guess of the pattern.')
    task_2_reason_no_attempt = models.LongStringField(blank=True, label='Why did you not bother looking for the pattern?')



class BonusPage(Page):
    form_model = 'player'
    form_fields = ['donated_amount']

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        # Deserialize stored data
        first_level_correctness = json.loads(participant.vars.get('final_round_correctness', '{}'))
        second_level_correctness = json.loads(participant.vars.get('final_round_correctness_task2', '{}'))

        # Calculate total correct answers
        first_level_correct = sum(first_level_correctness.values())
        second_level_correct = sum(second_level_correctness.values())
        total_correct = first_level_correct + second_level_correct

        # Calculate earnings
        bonus_per_correct = Constants.bonus_per_correct_answer  # Avoid rounding
        base_pay = Constants.base_payment  # Ensure precision
        bonus_from_correct_answers = total_correct * bonus_per_correct
        bonus_before_tax = base_pay + bonus_from_correct_answers

        # Apply tax
        tax_amount = bonus_before_tax * Constants.tax_rate
        net_earnings_after_tax = bonus_before_tax *(1 - Constants.tax_rate)
        donated_amount = float(player.donated_amount)
        net_earnings_after_donation = net_earnings_after_tax - player.donated_amount

        # Format all monetary amounts to two decimal places
        formatted_base_pay = f"{base_pay:.2f}"
        formatted_bonus_per_correct = f"{bonus_per_correct:.2f}"
        formatted_bonus_from_correct_answers = f"{bonus_from_correct_answers:.2f}"
        formatted_bonus_before_tax = f"{bonus_before_tax:.2f}"
        formatted_tax_amount = f"{tax_amount:.2f}"
        formatted_net_earnings = f"{net_earnings_after_tax:.2f}"
        formatted_donated_amount = f"{donated_amount:.2f}"
        formatted_net_earnings_after_donation = f"{net_earnings_after_donation:.2f}"
        

        # Store values in the player model
        player.total_correct = total_correct
        player.bonus_before_tax = bonus_before_tax
        player.net_earnings_after_tax = net_earnings_after_tax
        player.net_earnings_after_donation = player.net_earnings_after_tax - player.donated_amount
        
        print(f"Donated amount: {player.donated_amount}")

        # Debugging information
        print(f"Base Pay: {base_pay}, Bonus from Correct Answers: {bonus_from_correct_answers}")
        print(f"Total Correct: {total_correct}, Bonus Before Tax: {bonus_before_tax}, Tax: {tax_amount}, Net Earnings: {net_earnings_after_tax}")
        print(f"Bonus_per_correct: {bonus_per_correct}")
        print(f"Formatted net earnings after tax: {formatted_net_earnings}")
        
        return {
            'first_level_correct': first_level_correct,
            'second_level_correct': second_level_correct,
            'total_correct': total_correct,
            'bonus_from_correct_answers': formatted_bonus_from_correct_answers,
            'bonus_before_tax': formatted_bonus_before_tax,
            'tax_amount': formatted_tax_amount,
            'net_earnings_after_tax': formatted_net_earnings,
            'bonus_per_correct': formatted_bonus_per_correct,
            'donated_amount': formatted_donated_amount,
            'net_earnings_after_donation': formatted_net_earnings_after_donation,
            'base_pay': formatted_base_pay,
        }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.donated_amount > 0:
            player.button_pressed = 'Donate'
        else:
            player.button_pressed = 'Proceed without Donating'

        print(f"Button pressed: {player.button_pressed}")
        print(f"Donation: {player.donated_amount}, Reimbursement: {player.reimbursement_amount}")

class AnnouncementPage(Page):
    form_model = 'player'
    form_fields = ['entered_password']
    
    @staticmethod
    def vars_for_template(player: Player):
        level_1_treatment = player.participant.vars.get('level_1_treatment', 'Anonymity')
        level_2_treatment = player.participant.vars.get('level_2_treatment', 'No message')

        # Base content for all participants
        observability_text = ""
        moral_message = ""

        # Conditional content based on Level 1 treatment
        if level_1_treatment == 'Observability':
            #extra_content += """ <p>There will be a representative of the charity present in this adjacent room to assist you with inputting your information for accounting purposes.</p>
            #"""
            observability_text = """ <p>A proctor will be available at the dedicated computer to assist you with entering your information.</p>
            """

        # Conditional content based on Level 2 treatment
        if level_2_treatment == 'Moral message':
            moral_message = """ <p>Did you know? In a recent survey conducted in Austria <em>(Aman Hild & Hilweg-Waldeck, WP)</em>, over <strong>80% of respondents</strong> indicated that they consider it morally appropriate to tax-deduct charitable donations.</p>
            """


        return {
            'level_1_treatment': level_1_treatment,
            'level_2_treatment': level_2_treatment,
            'observability_text': observability_text,
            'moral_message': moral_message,
            'participant_code': player.participant.code,
            'university': player.session.config.get('university', 'uni_wien'),

        }
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        valid_passwords = ["Victoria!", "Michael!", "Johannes!", "Joanna!", "Jonathan", 
                           "Jakob!", "Felix!", "Jan!","Markus!", "Peter!", "Jim!", "Stefan!",
                             "Gabriel!", "Mariia!", "Sophie!", "Selina!", "Divena!", 
                             "Ascher!", "Default!"]
        entered_password = player.field_maybe_none('entered_password')  # Safely access the field

        print(f"DEBUG: Entered password: {entered_password}")  # Debugging print

        if not entered_password or entered_password not in valid_passwords:
            raise ValueError("Invalid password entered!")  # Prevent navigation
        print(f"DEBUG: Valid password entered: {entered_password}")

class DeductionDecisionPage(Page):
    form_model = 'player'
    form_fields = ['deduct_donation']

    @staticmethod
    def vars_for_template(player: Player):
        # Calculate and format monetary amounts
        net_earnings_after_donation = player.net_earnings_after_tax - player.donated_amount
        reimbursement_amount = player.donated_amount * Constants.tax_rate

        return {
            'formatted_donated_amount': f"{player.donated_amount:.2f}",
            'net_earnings_after_donation': f"{net_earnings_after_donation:.2f}",
            'reimbursement_amount': f"{reimbursement_amount:.2f}",
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Update earnings if donation deduction is chosen
        if player.deduct_donation:
            player.reimbursement_amount = player.donated_amount * Constants.tax_rate
            player.net_earnings_after_tax += player.reimbursement_amount
        else:
            player.net_earnings_after_donation = player.net_earnings_after_tax - player.donated_amount


class IBANPaymentPage(Page):
    form_model = 'player'
    form_fields = ['entered_password']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'session_code': player.session.code,
            'participant_code': player.participant.code,
            'university': player.session.config.get('university', 'uni_wien'),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        valid_passwords = ["Victoria!", "Michael!", "Johannes!", "Joanna!", "Jonathan", 
                           "Jakob!", "Felix!", "Jan!","Markus!", "Peter!", "Jim!", "Stefan!",
                             "Gabriel!", "Mariia!", "Sophie!", "Selina!", "Divena!", 
                             "Ascher!", "Default!"]
        if player.entered_password not in valid_passwords:
            raise ValueError("Invalid password entered! Please check with the experimenter.")


class DonationReasonPage(Page):
    form_model = 'player'
    form_fields = ['donation_decision_reason']

class DeductionReasonPage(Page):
    form_model = 'player'
    form_fields = ['deduction_decision_reason']

class BeliefEstimationPage(Page):
    form_model = 'player'
    form_fields = ['belief_donation_percentage', 'belief_deduction_percentage']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'info_text': "We would like to know your perception of donation and deduction behavior in this study."
        }

    @staticmethod
    def error_message(player, values):
        if not (0 <= values['belief_donation_percentage'] <= 100):
            return "Please enter a percentage between 0 and 100 for donation percentage."
        if not (0 <= values['belief_deduction_percentage'] <= 100):
            return "Please enter a percentage between 0 and 100 for deduction percentage."

class FirstTaskSurveyPage(Page):
    form_model = 'player'
    form_fields = ['task_1_pattern_attempt']

    @staticmethod
    def vars_for_template(player: Player):
        return {'task_name': 'First Task'}

class FirstTaskFollowUpPage(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.task_1_pattern_attempt == 'I tried to discover the hidden pattern and failed.':
            return ['task_1_strategy']
        elif player.task_1_pattern_attempt == 'I tried to discover the hidden pattern and succeeded.':
            return ['task_1_strategy', 'task_1_guess_pattern']
        elif player.task_1_pattern_attempt == 'I did not bother looking for the pattern; I focused on using the method provided.':
            return ['task_1_reason_no_attempt']

class SecondTaskSurveyPage(Page):
    form_model = 'player'
    form_fields = ['task_2_pattern_attempt']

    @staticmethod
    def vars_for_template(player: Player):
        return {'task_name': 'Second Task'}

class SecondTaskFollowUpPage(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.task_2_pattern_attempt == 'I tried to discover the hidden pattern and failed.':
            return ['task_2_strategy']
        elif player.task_2_pattern_attempt == 'I tried to discover the hidden pattern and succeeded.':
            return ['task_2_strategy', 'task_2_guess_pattern']
        elif player.task_2_pattern_attempt == 'I did not bother looking for the pattern; I focused on using the method provided.':
            return ['task_2_reason_no_attempt']

class FarewellPage(Page):
    pass

page_sequence = [
    BonusPage,
    AnnouncementPage,
    DeductionDecisionPage,
    BeliefEstimationPage,
    IBANPaymentPage,
    DonationReasonPage,
    DeductionReasonPage,
    FirstTaskSurveyPage,
    FirstTaskFollowUpPage,
    SecondTaskSurveyPage,
    SecondTaskFollowUpPage,
    FarewellPage
]
