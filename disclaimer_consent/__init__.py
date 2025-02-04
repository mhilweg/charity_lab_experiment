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

    # --- Level-1 Assignment: Anonymity/Observability (Stratified by Gender) ---
    males = [p for p in participants if p.gender == 'Male']
    females = [p for p in participants if p.gender == 'Female']

    for group in [males, females]:
        random.shuffle(group)  # Shuffle participants to randomize assignment order
        group_size = len(group)
        #half_size = (group_size - 1) // 2

        for i, p in enumerate(group):
            if group_size % 2 == 0 or i < group_size - 1:  # Even group or all except the last in odd group
                p.participant.vars['level_1_treatment'] = 'Anonymity' if i < group_size // 2 else 'Observability'
            else:  # Last participant in an odd-sized group
                p.participant.vars['level_1_treatment'] = 'Anonymity' if random.random() < 0.5 else 'Observability'

    # --- Level-2 Assignment: Moral Message/No Message (Stratified by Gender and Level-1) ---
    subgroups_level_2 = {
        ('Male', 'Anonymity'): [p for p in males if p.participant.vars['level_1_treatment'] == 'Anonymity'],
        ('Male', 'Observability'): [p for p in males if p.participant.vars['level_1_treatment'] == 'Observability'],
        ('Female', 'Anonymity'): [p for p in females if p.participant.vars['level_1_treatment'] == 'Anonymity'],
        ('Female', 'Observability'): [p for p in females if p.participant.vars['level_1_treatment'] == 'Observability'],
    }

    for group in subgroups_level_2.values():
        random.shuffle(group)
        group_size = len(group)
        #half_size = (group_size - 1) // 2

        for i, p in enumerate(group):
            if group_size % 2 == 0 or i < group_size - 1:
                p.participant.vars['level_2_treatment'] = 'Moral message' if i < group_size // 2 else 'No message'
            else:
                p.participant.vars['level_2_treatment'] = 'Moral message' if random.random() < 0.5 else 'No message'

    # --- Level-3 Assignment: Easy/Hard (Stratified by Gender, Level-1, and Level-2) ---
    subgroups_level_3 = {
        ('Male', 'Anonymity', 'Moral message'): [p for p in males if p.participant.vars['level_1_treatment'] == 'Anonymity' and p.participant.vars['level_2_treatment'] == 'Moral message'],
        ('Male', 'Anonymity', 'No message'): [p for p in males if p.participant.vars['level_1_treatment'] == 'Anonymity' and p.participant.vars['level_2_treatment'] == 'No message'],
        ('Male', 'Observability', 'Moral message'): [p for p in males if p.participant.vars['level_1_treatment'] == 'Observability' and p.participant.vars['level_2_treatment'] == 'Moral message'],
        ('Male', 'Observability', 'No message'): [p for p in males if p.participant.vars['level_1_treatment'] == 'Observability' and p.participant.vars['level_2_treatment'] == 'No message'],
        ('Female', 'Anonymity', 'Moral message'): [p for p in females if p.participant.vars['level_1_treatment'] == 'Anonymity' and p.participant.vars['level_2_treatment'] == 'Moral message'],
        ('Female', 'Anonymity', 'No message'): [p for p in females if p.participant.vars['level_1_treatment'] == 'Anonymity' and p.participant.vars['level_2_treatment'] == 'No message'],
        ('Female', 'Observability', 'Moral message'): [p for p in females if p.participant.vars['level_1_treatment'] == 'Observability' and p.participant.vars['level_2_treatment'] == 'Moral message'],
        ('Female', 'Observability', 'No message'): [p for p in females if p.participant.vars['level_1_treatment'] == 'Observability' and p.participant.vars['level_2_treatment'] == 'No message'],
    }

    for group in subgroups_level_3.values():
        random.shuffle(group)
        group_size = len(group)
        #half_size = (group_size - 1) // 2

        for i, p in enumerate(group):
            if group_size % 2 == 0 or i < group_size - 1:
                p.participant.vars['difficulty_level'] = 'easy' if i < group_size // 2 else 'hard'
            else:
                p.participant.vars['difficulty_level'] = 'easy' if random.random() < 0.5 else 'hard'

    # --- Level-4 Assignment: No Freeze/Freeze (Stratified by Gender, Level-1, Level-2, and Level-3) ---
    subgroups_level_4 = {
        (gender, level_1, level_2, difficulty): [p for p in participants if p.gender == gender
                                                 and p.participant.vars['level_1_treatment'] == level_1
                                                 and p.participant.vars['level_2_treatment'] == level_2
                                                 and p.participant.vars['difficulty_level'] == difficulty]
        for gender in ['Male', 'Female']
        for level_1 in ['Anonymity', 'Observability']
        for level_2 in ['Moral message', 'No message']
        for difficulty in ['easy', 'hard']
    }

    for group in subgroups_level_4.values():
        for p in group:
            p.participant.vars['level_3_treatment'] = 'No freeze' if random.random() < 0.85 else 'Freeze'

    # --- Debugging: Print Assignments ---
    print("\nLevel 1 Assignments:")
    print([p.participant.vars['level_1_treatment'] for p in participants])

    print("\nLevel 2 Assignments:")
    print([(p.id_in_group, p.participant.vars['level_2_treatment']) for p in participants])

    print("\nLevel 3 Assignments:")
    print([(p.id_in_group, p.participant.vars['difficulty_level']) for p in participants])

    print("\nLevel 4 Assignments:")
    print([(p.id_in_group, p.participant.vars['level_3_treatment']) for p in participants])


page_sequence = [Disclaimer, Demographics, RandomizationWaitPage]
