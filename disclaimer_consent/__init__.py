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

    age = models.IntegerField(
        label="How old are you?",
        min=18,  # Minimum age (optional)
        max=99,  # Maximum age (optional)
    )

    degree = models.StringField(
        label="Which degree are you currently enrolled in?",
        choices=["Bachelors", "Masters", "PhD", "Other"],
        widget=widgets.RadioSelect
    )


class Disclaimer(Page):
    def vars_for_template(player):
        return {
            'disclaimer_message': (
                "This study is conducted by the University of Mannheim and Masaryk University. All data collected will "
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
    form_fields = ['gender', 'field_of_studies', 'age', 'degree']


class RandomizationWaitPage(WaitPage):
    after_all_players_arrive = 'assign_treatments'


def assign_treatments(subsession):
    session = subsession.session
    participants = subsession.get_players()

    # --- Stratified Level-1 Assignment (Anonymity/Observability) ---
    males = [p for p in participants if p.gender == 'Male']
    females = [p for p in participants if p.gender == 'Female']

    # Randomize treatment within gender groups
    for group in [males, females]:
        random.shuffle(group)  # Shuffle participants
        half = len(group) // 2
        for i, p in enumerate(group):
            if i < half:
                p.participant.vars['level_1_treatment'] = 'Anonymity'
            else:
                p.participant.vars['level_1_treatment'] = 'Observability'

    # --- Stratified Level-2 Assignment (Moral Message/No Message, Based on Gender and Level-1) ---
    subgroups = {
        ('Male', 'Anonymity'): [p for p in males if p.participant.vars['level_1_treatment'] == 'Anonymity'],
        ('Male', 'Observability'): [p for p in males if p.participant.vars['level_1_treatment'] == 'Observability'],
        ('Female', 'Anonymity'): [p for p in females if p.participant.vars['level_1_treatment'] == 'Anonymity'],
        ('Female', 'Observability'): [p for p in females if p.participant.vars['level_1_treatment'] == 'Observability'],
    }

    for key, group in subgroups.items():
        random.shuffle(group)
        half = len(group) // 2
        for i, p in enumerate(group):
            p.participant.vars['level_2_treatment'] = 'Moral message' if i < half else 'No message'

    # --- Stratified Level-3 Assignment (Freeze/No Freeze, Based on Gender and Level-2) ---
    # Create subgroups for level-3 randomization
    level_3_subgroups = {
        ('Male', 'Moral message'): [p for p in males if p.participant.vars['level_2_treatment'] == 'Moral message'],
        ('Male', 'No message'): [p for p in males if p.participant.vars['level_2_treatment'] == 'No message'],
        ('Female', 'Moral message'): [p for p in females if p.participant.vars['level_2_treatment'] == 'Moral message'],
        ('Female', 'No message'): [p for p in females if p.participant.vars['level_2_treatment'] == 'No message'],
    }

    for key, group in level_3_subgroups.items():
        for p in group:
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
