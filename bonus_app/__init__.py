from otree.api import *
import json

class Constants(BaseConstants):
    name_in_url = 'bonus_app'
    players_per_group = None
    num_rounds = 1  # Two pages: bonus calculation and deduction
    base_payment = 5  # Base payment
    bonus_per_correct_answer = 0.50  # Bonus for each correct answer
    tax_rate = 0.30  # Flat tax rate (30%)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    total_correct = models.IntegerField(initial=0)  # Total correct answers across tasks
    bonus_before_tax = models.CurrencyField(initial=0)  # Bonus before taxation
    net_earnings_after_tax = models.CurrencyField(initial=0)  # Earnings after tax
    donated_amount = models.FloatField(initial=0.0)  # Amount donated with two decimal places
    reimbursement_amount = models.FloatField(initial=0.0)  # Tax reimbursement for donation
    net_earnings_after_donation = models.CurrencyField(initial=0.0)
    deduct_donation = models.BooleanField()  # Whether the participant wants to deduct the donation
    button_pressed = models.StringField(choices=["Proceed without Donating", "Donate"], blank=True)



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
        bonus_per_correct = float(Constants.bonus_per_correct_answer)  # Avoid rounding
        base_pay = float(Constants.base_payment)  # Ensure precision
        bonus_from_correct_answers = total_correct * bonus_per_correct
        bonus_before_tax = base_pay + bonus_from_correct_answers

        # Apply tax
        tax_amount = bonus_before_tax * Constants.tax_rate
        net_earnings_after_tax = bonus_before_tax - tax_amount
        donated_amount = float(player.donated_amount)

        # Format all monetary amounts to two decimal places
        formatted_base_pay = f"{base_pay:.2f}"
        formatted_bonus_per_correct = f"{bonus_per_correct:.2f}"
        formatted_bonus_from_correct_answers = f"{bonus_from_correct_answers:.2f}"
        formatted_bonus_before_tax = f"{bonus_before_tax:.2f}"
        formatted_tax_amount = f"{tax_amount:.2f}"
        formatted_net_earnings = f"{net_earnings_after_tax:.2f}"
        formatted_donated_amount = f"{donated_amount:.2f}"
        

        # Store values in the player model
        player.total_correct = total_correct
        player.bonus_before_tax = bonus_before_tax
        player.net_earnings_after_tax = net_earnings_after_tax
        
        print(f"Donated amount: {player.donated_amount}")

        # Debugging information
        print(f"Base Pay: {base_pay}, Bonus from Correct Answers: {bonus_from_correct_answers}")
        print(f"Total Correct: {total_correct}, Bonus Before Tax: {bonus_before_tax}, Tax: {tax_amount}, Net Earnings: {net_earnings_after_tax}")
        print(f"Bonus_per_correct: {bonus_per_correct}")
        
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
    @staticmethod
    def vars_for_template(player: Player):
        level_1_treatment = player.participant.vars.get('level_1_treatment', 'Anonymity')
        level_2_treatment = player.participant.vars.get('level_2_treatment', 'No message')

        # Base content for all participants
        extra_content = """ <p>This is the last page that you see on this terminal.</p> 
        <p>To conclude the experiment, we kindly ask you to proceed to the adjacent room when it is your turn.</p>
        <p>There, you will make a deduction decision and have to input your IBAN credentials.</p>
        """

        # Conditional content based on Level 1 treatment
        if level_1_treatment == 'Observability':
            extra_content += """ <p>There will be a representative of the charity present in this adjacent room to assist you with inputting your information for accounting purposes.</p>
            """

        # Conditional content based on Level 2 treatment
        if level_2_treatment == 'Moral message':
            extra_content += """ <p>Maybe this is of interest to you: in a recent survey run in Austria, more than 80% of people indicated that they find it morally appropriate to tax-deduct one's charitable donations.</p>
            """

        return {
            'level_1_treatment': level_1_treatment,
            'level_2_treatment': level_2_treatment,
            'extra_content': extra_content,
        }


class PaymentInfoDeductionPage(Page):
    form_model = 'player'
    form_fields = ['deduct_donation']

    @staticmethod
    def vars_for_template(player: Player):
        # Compute reimbursement amount if donation deduction is chosen
        net_earnings_after_donation = round(float(player.net_earnings_after_tax) - float(player.donated_amount), 2)
        donated_amount = round(float(player.donated_amount), 2)
        reimbursement_amount = round(donated_amount * Constants.tax_rate, 2)

        # Format monetary values to two decimal places
        formatted_donated_amount = f"{donated_amount:.2f}"
        formatted_reimbursement_amount = f"{reimbursement_amount:.2f}"
        formatted_net_earnings_after_donation = f"{net_earnings_after_donation:.2f}"

        # Store reimbursement in the player model
        player.net_earnings_after_donation = round(net_earnings_after_donation, 2)
        player.reimbursement_amount = round(reimbursement_amount, 2)

        # Debugging information
        print(f"Donation: {donated_amount}, Reimbursement: {reimbursement_amount}")
        print(f"Net earnings after taxation: {player.net_earnings_after_tax}")
        print(f"Net earnings after donation: {net_earnings_after_donation}")

        print(f"Net earnings after tax (CurrencyField): {player.net_earnings_after_tax}")
        print(f"Net earnings after tax (float): {float(player.net_earnings_after_tax)}")
        print(f"Donation (float): {float(player.donated_amount)}")
        print(f"Net earnings after donation (calculated): {net_earnings_after_donation}")
        print(f"Net earnings after donation (stored): {player.net_earnings_after_donation}")

        return {
            'formatted_donated_amount': formatted_donated_amount,
            'donated_amount': donated_amount,
            'reimbursement_amount': formatted_reimbursement_amount,
            'net_earnings_after_donation': formatted_net_earnings_after_donation,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.deduct_donation:
            player.net_earnings_after_tax += player.reimbursement_amount
            print(f"Donation deducted. Net Earnings Updated: {player.net_earnings_after_tax}")
        else:
            player.net_earnings_after_donation = player.net_earnings_after_tax - player.donated_amount
            print(f"No donation deduction. Net Earnings: {player.net_earnings_after_tax}")

class FarewellPage(Page):
    pass

page_sequence = [BonusPage, AnnouncementPage, PaymentInfoDeductionPage, FarewellPage]
