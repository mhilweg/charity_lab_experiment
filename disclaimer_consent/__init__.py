from otree.api import *
import random


class C(BaseConstants):
    NAME_IN_URL = 'disclaimer_consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent_given = models.BooleanField(
        label="I consent to participate in this study.",
        choices=[(True, 'Yes'), (False, 'No')],
        widget=widgets.RadioSelect
    )

    gender = models.StringField(
        label="What is your gender at birth?",
        choices=["Male", "Female"],
        widget=widgets.RadioSelect
    )

    field_of_studies = models.StringField(
        label="What is your field of studies?",
        blank=True
    )


class Disclaimer(Page):
    form_model = 'player'
    form_fields = ['consent_given']

    def before_next_page(player, timeout_happened):
        # If participant does not consent, mark them for study exit.
        if not player.consent_given:
            player.participant.vars['study_exit'] = True


class StudyExit(Page):
    def is_displayed(player):
        # Display this page only if participant did not consent.
        return player.participant.vars.get('study_exit', False)

    def vars_for_template(player):
        return {
            'exit_message': "Thank you for your interest in the study. Since you did not consent to participate, the experiment will now end."
        }


class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender', 'field_of_studies']

class RandomizationWaitPage(WaitPage):
    after_all_players_arrive = 'assign_treatments'

def assign_treatments(subsession):
    session = subsession.session
    participants = subsession.get_players()

    # --- Manual or Default Level 1 Assignment ---
    if 'level_1_treatment' in session.config:
        level_1_treatment = session.config['level_1_treatment']
    else:
        level_1_treatment = 'Anonymity'  # Default fallback

    for p in participants:
        p.participant.vars['level_1_treatment'] = level_1_treatment

    # --- Level 2 Assignment (Stratified by Gender and Level 1) ---
    males = [p for p in participants if p.gender == 'Male']
    females = [p for p in participants if p.gender == 'Female']

    for group in [males, females]:
        random.shuffle(group)  # Shuffle within each gender group
        half = len(group) // 2
        for i, p in enumerate(group):
            p.participant.vars['level_2_treatment'] = 'Moral message' if i < half else 'No message'

    # --- Level 3 Assignment (Probability-Based, Stratified by Gender and Level 2) ---
    for group in [males, females]:
        for treatment in ['Moral message', 'No message']:
            subgroup = [p for p in group if p.participant.vars['level_2_treatment'] == treatment]
            for p in subgroup:
                level_3_treatment = 'No freeze' if random.random() < 0.1 else 'Freeze'
                p.participant.vars['level_3_treatment'] = level_3_treatment

    # --- Debugging: Print Assignments ---
    print("\nLevel 1 Assignments:")
    print([p.participant.vars['level_1_treatment'] for p in participants])

    print("\nLevel 2 Assignments:")
    print([(p.id_in_group, p.participant.vars['level_2_treatment']) for p in participants])

    print("\nLevel 3 Assignments:")
    print([(p.id_in_group, p.participant.vars['level_3_treatment']) for p in participants])

page_sequence = [Disclaimer, StudyExit, Demographics, RandomizationWaitPage]