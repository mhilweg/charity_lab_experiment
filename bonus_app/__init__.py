from otree.api import *
import json
import random
import urllib.request
import urllib.parse
import urllib.error

class Constants(BaseConstants):
    name_in_url = 'bonus_app'
    players_per_group = None
    num_rounds = 1  # Two pages: bonus calculation and deduction
    base_payment = 5  # Base payment
    bonus_per_correct_answer = 0.25  # Bonus for each correct answer
    tax_rate = 0.30  # Flat tax rate (30%)

    # 2x2 deduction-treatment cells, assigned to donors only (see assign_deduction_treatments)
    deduction_treatment_cells = [
        ['Anonymity', 'Moral message'],
        ['Anonymity', 'No message'],
        ['Observability', 'Moral message'],
        ['Observability', 'No message'],
    ]
    not_applicable = 'Not applicable'  # treatment value for non-donors

    # Passwords typed by the experimenter / research assistant to release gated pages
    valid_passwords = ["Victoria!", "Michael!", "Johannes!", "Joanna!", "Jonathan",
                       "Jakob!", "Felix!", "Jan!", "Markus!", "Peter!", "Jim!", "Stefan!",
                       "Gabriel!", "Mariia!", "Sophie!", "Selina!", "Divena!",
                       "Ascher!", "Default!"]
    payment_status_timeout_seconds = 5

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



def is_donor(player: Player) -> bool:
    return player.donated_amount > 0


def uses_payment_survey(university: str) -> bool:
    """
    Sites where payment data is collected electronically via the payment survey app (as opposed to the
    paper-based IBAN sheet at Uni Wien). HU Berlin follows the WU flow; the survey additionally asks
    for the tax identification number there.
    """
    return university in ('wu_wien', 'hu_berlin')


def assign_deduction_treatments(player: Player):
    """
    Assigns the Anonymity/Observability and Moral message/No message treatments.

    Called right after the donation decision. Only donors are assigned, because only donors can
    deduct. Assignment is sequential but balanced: within each gender stratum, the session keeps a
    shuffled block of the four 2x2 cells and hands out one cell per donor; when a block is used up a
    freshly shuffled block is drawn. This guarantees near-perfect balance among donors within a
    session without anyone having to wait for other participants.

    Non-donors receive 'Not applicable' in both fields.
    """
    participant = player.participant

    if not is_donor(player):
        participant.level_1_treatment = Constants.not_applicable
        participant.level_2_treatment = Constants.not_applicable
        return

    current = participant.vars.get('level_1_treatment')
    if current not in (None, 'Pending', Constants.not_applicable):
        # Already assigned (e.g. page re-submitted); do not consume another slot.
        return

    session = player.session
    stratum = participant.vars.get('gender') or 'Unknown'

    blocks = session.vars.get('deduction_treatment_blocks') or {}
    queue = list(blocks.get(stratum) or [])
    if not queue:
        queue = [list(cell) for cell in Constants.deduction_treatment_cells]
        random.shuffle(queue)

    level_1, level_2 = queue.pop(0)
    blocks[stratum] = queue
    session.vars['deduction_treatment_blocks'] = blocks  # re-assign so the change is persisted

    participant.level_1_treatment = level_1
    participant.level_2_treatment = level_2
    print(f"Deduction treatments assigned to {participant.code} (stratum={stratum}): {level_1} / {level_2}")


def payment_submitted(player: Player):
    """
    Asks the WU payment survey app whether this participant has submitted payment information.

    Returns True / False, or None if the survey app could not be reached (caller should fall back
    to the experimenter password).
    """
    base_url = player.session.config.get('payment_survey_url')
    if not base_url:
        return None
    query = urllib.parse.urlencode({
        'session_id': player.session.code,
        'participant_id': player.participant.code,
    })
    url = f"{base_url.rstrip('/')}/api/status?{query}"
    try:
        with urllib.request.urlopen(url, timeout=Constants.payment_status_timeout_seconds) as response:
            data = json.loads(response.read().decode('utf-8'))
            return bool(data.get('submitted'))
    except (urllib.error.URLError, ValueError, OSError) as exc:
        print(f"Payment status check failed for {player.participant.code}: {exc}")
        return None


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

        # Deduction treatments are assigned here, i.e. after the donation decision and only to donors
        assign_deduction_treatments(player)

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
            'uses_payment_survey': uses_payment_survey(player.session.config.get('university', 'uni_wien')),
            'is_donor': is_donor(player),
        }

    @staticmethod
    def js_vars(player):
        return {'valid_passwords': Constants.valid_passwords}

    @staticmethod
    def error_message(player, values):
        # Donors are released by the experimenter (password) when it is their turn at the dedicated
        # computer. Non-donors continue on their own terminal and need no password.
        if not is_donor(player):
            return None
        entered_password = values.get('entered_password')
        if not entered_password or entered_password not in Constants.valid_passwords:
            return "Please remain seated until you are asked to go to the dedicated computer."
        return None

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
            'is_donor': is_donor(player),
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
        university = player.session.config.get('university', 'uni_wien')
        donor = is_donor(player)

        # Non-donors at WU / HU Berlin stay on their own terminal: instead of the experimenter password we
        # verify with the payment-survey app that their payment information has arrived.
        verify_payment = (not donor) and uses_payment_survey(university)
        payment_status = 'not_checked'
        if verify_payment:
            received = payment_submitted(player)
            payment_status = {True: 'received', False: 'missing', None: 'unavailable'}[received]

        return {
            'session_code': player.session.code,
            'participant_code': player.participant.code,
            'university': university,
            'uses_payment_survey': uses_payment_survey(university),
            'is_donor': donor,
            'verify_payment': verify_payment,
            'payment_status': payment_status,  # received / missing / unavailable (survey app unreachable) / not_checked
            'payment_survey_url': player.session.config.get('payment_survey_url', ''),
        }

    @staticmethod
    def js_vars(player):
        return {
            'valid_passwords': Constants.valid_passwords,
            'payment_survey_url': player.session.config.get('payment_survey_url', ''),
            'session_code': player.session.code,
            'participant_code': player.participant.code,
            'university': player.session.config.get('university', 'uni_wien'),
        }

    @staticmethod
    def error_message(player: Player, values):
        entered_password = values.get('entered_password')
        password_ok = bool(entered_password) and entered_password in Constants.valid_passwords
        if password_ok:
            return None

        university = player.session.config.get('university', 'uni_wien')
        if not is_donor(player) and uses_payment_survey(university):
            # Authoritative server-side check; the page's Submit button is only enabled after the same
            # check succeeded on page load, but we never trust the browser alone.
            if payment_submitted(player):
                return None
            return ("We have not received your payment information yet. Please complete the payment "
                    "survey first, then return to this page.")

        return "Invalid password entered! Please check with the experimenter."


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
