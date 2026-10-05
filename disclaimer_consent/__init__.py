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

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Make gender available to later apps (stratum for the deduction-treatment assignment in bonus_app)
        player.participant.gender = player.gender


class RandomizationWaitPage(WaitPage):
    after_all_players_arrive = 'assign_treatments'


def assign_treatments(subsession):
    """
    Assigns everything that must be fixed BEFORE the task starts.

    - Difficulty order (easy-first vs. hard-first): stratified by gender, balanced within session.
    - Freeze: feature disabled, everybody gets 'No freeze' (field kept for data compatibility).

    The deduction treatments (Anonymity/Observability and Moral message/No message) are NOT assigned
    here anymore. They are assigned to donors only, right after the donation decision, in
    bonus_app.assign_deduction_treatments(). Until then they hold the placeholder 'Pending'.
    """
    participants = subsession.get_players()

    for p in participants:
        p.participant.level_1_treatment = 'Pending'
        p.participant.level_2_treatment = 'Pending'
        p.participant.level_3_treatment = 'No freeze'

    # --- Difficulty order: easy/hard first (stratified by gender) ---
    males = [p for p in participants if p.gender == 'Male']
    females = [p for p in participants if p.gender == 'Female']

    for group in [males, females]:
        random.shuffle(group)
        group_size = len(group)

        for i, p in enumerate(group):
            if group_size % 2 == 0 or i < group_size - 1:  # Even group or all except the last in odd group
                p.participant.difficulty_level = 'easy' if i < group_size // 2 else 'hard'
            else:  # Last participant in an odd-sized group
                p.participant.difficulty_level = 'easy' if random.random() < 0.5 else 'hard'

    # --- Debugging: Print Assignments ---
    print("Difficulty order assignments:")
    print([(p.id_in_group, p.participant.difficulty_level) for p in participants])

page_sequence = [Disclaimer, Demographics, RandomizationWaitPage]
