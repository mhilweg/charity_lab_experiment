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
    def vars_for_template(player):
        return {
            'disclaimer_message': (
                "This study is conducted by the University of Mannheim. All data collected will "
                "be anonymized and used exclusively for research purposes. Your participation is "
                "entirely voluntary, and you may withdraw at any time without penalty."
            ),
            'consent_message': (
                "By clicking 'Next,' you indicate that you have read and understood the above "
                "information and agree to participate in the study."
            ),
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
                level_3_treatment = 'No freeze' if random.random() < 0.9 else 'Freeze'
                p.participant.vars['level_3_treatment'] = level_3_treatment

    # --- Debugging: Print Assignments ---
    print("\nLevel 1 Assignments:")
    print([p.participant.vars['level_1_treatment'] for p in participants])

    print("\nLevel 2 Assignments:")
    print([(p.id_in_group, p.participant.vars['level_2_treatment']) for p in participants])

    print("\nLevel 3 Assignments:")
    print([(p.id_in_group, p.participant.vars['level_3_treatment']) for p in participants])


page_sequence = [Disclaimer, Demographics, RandomizationWaitPage]
