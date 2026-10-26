# -*- coding: utf-8 -*-
"""
Builds two Word documents with the participant-facing text of the tax-deduction lab experiment.

  Version 1: instruction pages only
  Version 2: every page a participant can see (plus the external payment survey)

Content is transcribed from the oTree templates / page classes (settings: university = hu_berlin).
"""
import re, sys, datetime, pathlib
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PROJECT = pathlib.Path(r"C:\Users\mih89vw\Documents\Projects\Charity\Lab_experiment\tax_deduction_experiment")
OUT_DIR = PROJECT / "docs"
IMG = PROJECT / "_static" / "images" / "sample_sequence.png"
CHARITY_IMG = PROJECT / "_static" / "images" / "stop_child_labour.jpg"
TODAY = datetime.date.today().isoformat()
COMMIT = sys.argv[1] if len(sys.argv) > 1 else "n/a"

# ----------------------------------------------------------------------------------------------
# Content model
#   ('p', text)            paragraph; **bold**, *italic* inline markup
#   ('h', text)            on-screen heading inside the page
#   ('ul', [items])        bullet list
#   ('radio', [options])   radio buttons
#   ('field', label)       input field
#   ('button', label)      button
#   ('note', text)         experimenter note (grey, italic) - NOT seen by participants
#   ('variant', label, [blocks])   conditional block, shown only under the stated condition
#   ('img', path, width_cm)
#   ('seqtable', [(seq, responses)])  example sequences
#   ('hr',)
# ----------------------------------------------------------------------------------------------

SAMPLE_EASY = [
    ([1, 9, 9, 4, 9, 9, 9, 9], [4, 1, 9, 9, 9, 9, 9]),
    ([9, 4, 4, 4, 9, 4, 4, 4], [1, 9, 1, 4, 4, 4, 4]),
    ([1, 1, 1, 9, 1, 1, 1, 4], [1, 1, 4, 9, 4, 9, 1]),
    ([9, 9, 1, 9, 1, 4, 9, 9], [9, 4, 1, 1, 9, 9, 9]),
    ([4, 4, 4, 9, 1, 4, 4, 9], [4, 4, 1, 1, 9, 1, 4]),
]
SAMPLE_HARD = [
    ([1, 4, 1, 4, 4, 9, 9, 1], [9, 4, 4, 4, 1, 4, 9]),
    ([4, 1, 1, 4, 9, 9, 1, 4], [9, 9, 1, 4, 1, 1, 9]),
    ([9, 9, 1, 1, 4, 4, 1, 1], [9, 4, 9, 1, 9, 4, 9]),
    ([9, 1, 9, 9, 1, 4, 4, 1], [4, 1, 4, 9, 1, 9, 4]),
    ([1, 1, 4, 4, 9, 9, 4, 4], [1, 9, 1, 4, 1, 9, 1]),
]

COMPREHENSION = [
    ("If two numbers being compared are the same, what is the correct response?",
     ["The same number", "The third number in the set", "The sum of the two numbers"], "The same number"),
    ("If two numbers being compared are different, what is the correct response?",
     ["The larger number", "The smaller number", "The third number in the set"], "The third number in the set"),
    ("What is the goal of the task?",
     ["To enter all correct values into all seven response boxes",
      "To enter the correct value into the seventh response box",
      "To calculate the sum of all eight numbers"], "To enter the correct value into the seventh response box"),
]

TASK_INSTRUCTIONS_BLOCKS = [
    ('h', "Welcome to the task!"),
    ('p', "In this task, you will work with sequences of eight numbers, which can be either 1, 4, or 9. "
          "To facilitate your understanding, consider the sample picture below. The sequence of eight numbers is displayed with white boxes. "
          "Below it, there are seven response boxes, with the first six being blue and the seventh one being green."),
    ('p', "Your goal is to apply specific rules to compute the **final response for the seventh step** of each sequence. "
          "While you are free to input values into response boxes 1 to 6 as well, you must enter a value for the "
          "**seventh response box**, which is mandatory. This is the **only response** upon which we will determine "
          "whether you solved the task correctly."),
    ('p', "Below, we teach you one method for solving this task, but it is just one of many possible ways. "
          "**You are free to use this method or any other**, as only the correctness of your final answer determines your "
          "bonus payment of **0.25€** per correct response. There are **hidden patterns** to discover in the sequences that "
          "make it easier to find the correct seventh response."),
    ('img', IMG, 14),
    ('p', "You will play two versions of this task. Each version has a **maximum of 30 sequences**. Thus, you can earn a total "
          "bonus payment of up to 15.00 EUR. Please pay close attention to the rules, as they will guide you in solving the task."),
    ('h', "📋 Rules"),
    ('ul', ["✅ Only the numbers **1**, **4**, and **9** feature in the sequences and the responses.",
            "✅ If the two numbers that you have to compare are the same, the response is that same number.",
            "✅ If the two numbers are different, the response is the third number of the three numbers **1**, **4**, and **9**."]),
    ('h', "🛠 Method #1"),
    ('ul', ["🔍 To compute the first response, compare the first two numbers of the sequence. If they are identical, the correct "
            "response is the very same number again. If they are different, input the one of the three numbers that is not present. "
            "For example, if you compare '1' and '4', the correct response is '9'.",
            "🔍 For the second response, compare the first response with the third number of the sequence. The third response is "
            "based on the comparison of the second response and the fourth number of the sequence, and so on."]),
    ('p', "*You can always access these instructions on the subsequent pages through clicking the 'Task Instructions' button in the top right corner.*"),
]

POPUP_NOTE_1 = "A button 'Task Instructions' in the top-right corner of the screen re-opens the task instructions (page 2.2) in a pop-up window."
POPUP_NOTE_2 = ("Two buttons in the top-right corner of the screen, 'Task Instructions' and 'Example Sequences', re-open the task "
                "instructions (page 2.2) and the example sequences of the current version in pop-up windows.")

def example_blocks(part2=False):
    b = [('p', "Please review the following example sequences and their corresponding responses. The seventh response is highlighted "
               "as it is especially important for solving the task.")]
    if part2:
        b.append(('p', "Note that the underlying patterns may be different from the first set of sequences that you worked on."))
    b += [
        ('p', '*You can at any time access these sample sequences on the subsequent page through clicking the "Example Sequences" button on the top right corner.*'),
        ('p', "**Time Remaining:** [countdown, mm:ss]"),
        ('variant', "Participants whose current version uses the 'easy' sequence set", [('seqtable', SAMPLE_EASY)]),
        ('variant', "Participants whose current version uses the 'hard' sequence set", [('seqtable', SAMPLE_HARD)]),
        ('button', "Start Task"),
        ('note', "Each participant plays both versions; the order (easy first or hard first) is randomised and balanced by gender. "
                 "The two sets differ only in the hidden pattern, the rules are identical. Participants never see the words 'easy' or 'hard'."),
    ]
    return b

PAGES = [
    # ------------------------------------------------------------------ Part 1: consent and instructions
    dict(part="Consent and demographics", title="Legal Disclaimer and Consent", tpl="disclaimer_consent/Disclaimer.html",
         who="All participants", instr=True, blocks=[
        ('p', "This study is conducted by Humboldt University Berlin and Julius-Maximilians University Würzburg. All data collected will "
              "be anonymized and used exclusively for research purposes. Your participation is entirely voluntary, and you may withdraw "
              "at any time without penalty."),
        ('p', "By clicking 'Next,' you indicate that you have read and understood the above information and agree to participate in the study."),
        ('button', "Next"),
    ]),
    dict(part="Consent and demographics", title="Demographics", tpl="disclaimer_consent/Demographics.html",
         who="All participants", instr=False, blocks=[
        ('p', "Please answer the following questions."),
        ('field', "What is your field of studies? (text field, optional)"),
        ('p', "Which degree are you currently enrolled in?"),
        ('radio', ["Bachelors", "Masters", "PhD", "Other"]),
        ('field', "How old are you? (number, 18 to 99)"),
        ('p', "What was your gender at birth?"),
        ('radio', ["Male", "Female"]),
        ('button', "Continue"),
        ('note', "After this page all participants wait on an oTree wait page (standard text: 'Please wait', 'Waiting for other participants.') "
                 "until everyone has arrived; the order of the two task versions is assigned at that moment."),
    ]),
    # ------------------------------------------------------------------ task instructions app
    dict(part="Task instructions", title="Welcome to the Experiment", tpl="task_instructions/Introduction.html",
         who="All participants", instr=True, blocks=[
        ('p', "Thank you for participating in our study! Below, you'll find all the information you need to get started."),
        ('h', "📝 Task Overview"),
        ('p', "You will complete a task in 2 variations. Your performance in this task will determine your bonus payment."),
        ('p', "*More information on the task and how to play it will follow on the subsequent page.*"),
        ('h', "💰 Earnings and Taxes"),
        ('p', "Your total earnings consist of:"),
        ('ul', ["**Base Payment:** 5 EUR (guaranteed for participation)",
                "**Bonus Payment:** Up to 15.00 EUR (based on task performance)"]),
        ('p', "All earnings, including the base and bonus payments, are subject to a flat tax rate of **30%**."),
        ('p', "**Taxes**: We will take 30% of your earnings and add it to a common tax pool."),
        ('p', "*This tax pool will be redistributed equally among all participants once the study finishes. That is, everybody gets the same share of it.*"),
        ('h', "🌍 Donation Opportunity"),
        ('p', "After completing the task, you will have the option to donate a portion of your earnings to a charity focused on "
              "fighting child labour, poverty, and discrimination of girls and women in developing countries."),
        ('button', "Start the Experiment"),
    ]),
    dict(part="Task instructions", title="Task Instructions", tpl="task_instructions/TaskInstructions.html",
         who="All participants", instr=True, blocks=TASK_INSTRUCTIONS_BLOCKS + [('button', "Continue")]),
    dict(part="Task instructions", title="Comprehension Questions", tpl="task_instructions/ComprehensionQuestions1.html",
         who="All participants", instr=False, blocks=
        sum([[('p', q), ('radio', opts)] for q, opts, _ in COMPREHENSION], []) + [('button', "Submit"), ('note', POPUP_NOTE_1)]),
    dict(part="Task instructions", title="Comprehension Questions - Attempt 2", tpl="task_instructions/ComprehensionQuestions2.html",
         who="Only participants who answered at least one comprehension question incorrectly on the first attempt", instr=False, blocks=
        sum([[('p', q), ('radio', opts),
              ('variant', "Shown under a question that was answered incorrectly on the first attempt",
               [('p', "Your previous answer was incorrect.")])] for q, opts, _ in COMPREHENSION], [])
        + [('button', "Submit"),
           ('note', "The participant's previous answers are pre-selected. " + POPUP_NOTE_1)]),
    dict(part="Task instructions", title="Comprehension Clarification", tpl="task_instructions/ComprehensionClarification.html",
         who="Only participants who still had an incorrect answer on the second attempt", instr=True, blocks=
        [('p', "Below are the correct answers to the comprehension questions:")]
        + sum([[('p', q), ('ul', [("**" + o + "**" if o == c else o) for o in opts])] for q, opts, c in COMPREHENSION], [])
        + [('note', "The correct answer (bold above) is shown in green bold on screen."), ('button', "Continue"), ('note', POPUP_NOTE_1)]),
    dict(part="Task instructions", title="Practice the Rules", tpl="task_instructions/PracticePage.html",
         who="All participants", instr=True, blocks=[
        ('p', "Below are two sequences for practice. Enter your responses in the boxes and get instant feedback on your answers."),
        ('p', "*These sequences are of length four for your convenience. The actual task sequences will be of length eight.*"),
        ('p', "Sequence 1: 1, 4, 9, 1 with three empty response boxes (correct responses 9, 9, 4)."),
        ('p', "Sequence 2: 4, 4, 9, 1 with three empty response boxes (correct responses 4, 1, 1)."),
        ('p', "Instant feedback shown under each box:"),
        ('ul', ["Correct entry: \"Box 1 correct!\" (respectively Box 2, Box 3), in green.",
                "Wrong entry, sequence 1: \"Wrong. Remember that you are comparing '1' and '4'.\" / "
                "\"Wrong. Remember that you are comparing the first response and '9'.\" / "
                "\"Wrong. Remember that you are comparing the second response and '1'.\"",
                "Wrong entry, sequence 2: \"Wrong. Remember that you are comparing '4' and '4'.\" / "
                "\"Wrong. Remember that you are comparing the first response and '9'.\" / "
                "\"Wrong. Remember that you are comparing the second response and '1'.\""]),
        ('button', "Finish Practice"),
        ('note', "The 'Finish Practice' button only becomes active once all six boxes contain the correct response. " + POPUP_NOTE_1),
    ]),
    # ------------------------------------------------------------------ task app
    dict(part="The task", title="Before we start with the task.", tpl="task/InterimInstructions.html",
         who="All participants", instr=True, blocks=[
        ('ul', ["🕵️ **Pattern Detection:** There are some **hidden patterns** in the sequences that can be used to determine the correct seventh response more quickly.",
                "📊 **Sample Sequences:** On the next page, you will see a set of sample sequences that follow the same logic as the ones you will have to solve. Use them to **detect these patterns**.",
                "⏱️ **Time Budget:** You have a total time budget of 6 minutes for looking at the sample sequences and solving **30 actual tasks** for each of the two versions.",
                "🔍 **Reference Materials:** When moving forward to playing the tasks, you can always inspect the sample sequences again through a pop-up button. In addition, you can always see **all previously played sequences**.",
                "⏳ **Time Tracking:** The time starts to tick down once you click 'Next' on this page and move on to the sequence examples."]),
        ('button', "Next"),
        ('note', POPUP_NOTE_1),
    ]),
    dict(part="The task", title="Sequence Examples", tpl="task/SequenceExample.html",
         who="All participants (first task version)", instr=True, blocks=example_blocks(False)),
    dict(part="The task", title="Task: version 1", tpl="task/Task.html",
         who="All participants, one page per sequence (up to 30) within the 6-minute budget", instr=False, blocks=[
        ('p', "**Time remaining:** [countdown]"),
        ('p', "Sequence [n]/30:"),
        ('p', "[The eight numbers of the current sequence in white boxes, below them seven empty response boxes; boxes 1 to 6 are blue and optional, "
              "box 7 is green and mandatory. Only the digits 1, 4 and 9 are accepted.]"),
        ('button', "Submit"),
        ('h', "History"),
        ('p', "[All previously played sequences of this version with the participant's responses, most recent on top. The seventh response "
              "is coloured green if it was correct and red if it was wrong; the other responses are shown in blue.]"),
        ('note', POPUP_NOTE_2 + " When the 6 minutes are over, oTree automatically submits the page and the participant moves on."),
    ]),
    dict(part="The task", title="Transition to the Next Level", tpl="task/Transition.html",
         who="All participants, after the last sequence of version 1 or when the time is up", instr=True, blocks=[
        ('p', "You have successfully completed all tasks of the first version."),
        ('p', "Next, you will move on to the second version."),
        ('p', "This time there is a **different hidden trick**. While the sequence will follow the same rules, it may feel slightly different, "
              "so pay close attention to adapt to the new pattern."),
        ('p', "On the next page, the timer will start again. Please take a moment to prepare yourself. When you are ready, click the button below to continue."),
        ('button', "Proceed to the second version"),
        ('note', POPUP_NOTE_1),
    ]),
    dict(part="The task", title="Sequence Examples Part 2", tpl="task/SequenceExample2.html",
         who="All participants (second task version)", instr=True, blocks=example_blocks(True)),
    dict(part="The task", title="Task: version 2", tpl="task/Task2.html",
         who="All participants, one page per sequence (up to 30) within the second 6-minute budget", instr=False, blocks=[
        ('p', "**Time remaining:** [countdown]"),
        ('p', "Sequence [n]/30:"),
        ('p', "[Identical layout to version 1: the current sequence, seven response boxes and the Submit button, with the history of the second version on the right.]"),
        ('button', "Submit"),
        ('h', "History"),
        ('note', POPUP_NOTE_2),
    ]),
    # ------------------------------------------------------------------ bonus app
    dict(part="Earnings, donation and deduction", title="Bonus Calculation / Make a Donation / About the Charity", tpl="bonus_app/BonusPage.html",
         who="All participants", instr=True, blocks=[
        ('h', "Bonus Calculation"),
        ('p', "You answered **[number of correct answers]** task(s) correctly."),
        ('p', "Your total earnings before tax: **€[base payment plus bonus]**."),
        ('p', "Tax applied: **€[30% of earnings]** (30% flat rate)."),
        ('p', "Your net earnings after tax: **€[earnings after tax]**."),
        ('p', "Keep in mind that you will receive **an equal share** of the total tax pool **on top**. The exact value will be calculated once all participants completed the experiment."),
        ('h', "Make a Donation"),
        ('p', "Would you like to donate a portion of your net earnings to charity? Enter the amount below."),
        ('field', "Donation Amount: (number, 0 up to the net earnings after tax; default 0.00)"),
        ('p', "[Error shown for an invalid amount: \"Please enter a valid donation amount within your earnings.\"]"),
        ('button', "Donate indicated amount"),
        ('note', "A second, unlabelled 'proceed without donating' link exists in the form but carries no visible text. Participants who leave "
                 "the amount at 0 and click 'Donate indicated amount' are recorded as non-donors."),
        ('h', "About the Charity"),
        ('p', "[Photo of the charity's work, file 'stop_child_labour.jpg']"),
        ('ul', ["📘 Ensure access to education and protect children from exploitive work conditions.",
                "🍴 Provide food security and support sustainable farming practices.",
                "💡 Empower girls and women to access education and grow into entrepreneurship."]),
        ('p', "**Note:** This is a real, registered charity, and all donations collected during this experiment will be transferred directly to the organization after the study concludes."),
    ]),
    dict(part="Earnings, donation and deduction", title="📢 Important Announcement", tpl="bonus_app/AnnouncementPage.html",
         who="All participants; the text depends on whether the participant donated and, for donors, on the treatment", instr=True, blocks=[
        ('variant', "Donors (donation amount > 0)", [
            ('p', "To conclude the experiment, please proceed to the dedicated computer **when it is your turn**. At the dedicated computer, "
                  "you will make a final decision about whether to claim a deduction for your donation. Further, you will input your IBAN credentials there."),
            ('p', "**Stay at your place until you are asked to go to the dedicated computer.**"),
            ('hr',),
            ('p', "As a participant, you have the option to **deduct your donation** from the tax pool. Here's how it works:"),
            ('ul', ["💰 **Reimbursement Rate:** You can recover 30% of your donation as a reimbursement.",
                    "🏦 **Tax Pool Contribution:** The reimbursement is funded by contributions to the tax pool from all participants.",
                    "🤝 **Voluntary Choice:** Deciding to claim the deduction is entirely your choice and does not affect your donation amount."]),
        ]),
        ('variant', "Non-donors (donation amount = 0)", [
            ('p', "On the following pages, you will answer a few more questions and provide your payment information. Please continue on this terminal."),
            ('hr',),
            ('p', "Participants who donated have the option to **deduct their donation** from the tax pool. Here's how it works:"),
            ('ul', ["💰 **Reimbursement Rate:** Donors can recover 30% of their donation as a reimbursement.",
                    "🏦 **Tax Pool Contribution:** The reimbursement is funded by contributions to the tax pool from all participants.",
                    "🤝 **Voluntary Choice:** Deciding to claim the deduction is entirely the donor's choice and does not affect the donation amount."]),
        ]),
        ('variant', "Additional box, donors in the 'Observability' treatment only", [
            ('h', "🔍 Some more information"),
            ('p', "A proctor will be available at the dedicated computer to assist you with entering your information."),
        ]),
        ('variant', "Additional box, donors in the 'Moral message' treatment only", [
            ('h', "💡 What others think about deducting"),
            ('p', "Did you know? In a recent survey conducted in Austria *(Aman Hild & Hilweg-Waldeck, WP)*, over **80% of respondents** "
                  "indicated that they consider it morally appropriate to tax-deduct charitable donations."),
        ]),
        ('variant', "Donors (release field at the bottom of the page)", [
            ('field', "Unlabelled text field for the experimenter's release password"),
            ('p', "[While the field does not contain a valid password: \"Please remain seated until you are asked to go to the adjacent room.\"]"),
        ]),
        ('button', "Next"),
        ('note', "Donors are assigned to one of four treatment cells (Anonymity/Observability × Moral message/No message) right after the donation "
                 "decision, balanced within gender. Non-donors get no treatment. For donors the Next button stays inactive until the experimenter "
                 "types the release password; the experimenter then accompanies the donor to the dedicated computer, where the next pages are shown. "
                 "Non-donors continue on their own terminal without a password."),
    ]),
    dict(part="Earnings, donation and deduction", title="Tax-deducting donation", tpl="bonus_app/DeductionDecisionPage.html",
         who="All participants (donors at the dedicated computer, non-donors at their own terminal)", instr=True, blocks=[
        ('variant', "Donors", [
            ('p', "You earned (after donation): **€[earnings after tax minus donation]**."),
            ('p', "You donated: **€[donation amount]**."),
            ('p', "If you choose to deduct your donation, you will be reimbursed: **€[30% of the donation]**."),
            ('p', "Would you like to deduct your donation for tax reimbursement?"),
        ]),
        ('variant', "Non-donors", [
            ('p', "You earned (after tax): **€[earnings after tax]**."),
            ('p', "You donated: **€0.00**."),
            ('p', "Since you did not donate, there is no donation that could be deducted."),
            ('p', "Would you like to deduct your donation for tax reimbursement? *(Not possible without a donation. Please select \"No\" to continue.)*"),
        ]),
        ('radio', ["Yes", "No"]),
        ('p', "[If no option is selected on submit: \"Please make a decision.\"]"),
        ('button', "Continue"),
        ('note', "For non-donors the 'Yes' option is greyed out and cannot be selected."),
    ]),
    dict(part="Earnings, donation and deduction", title="Your Estimations", tpl="bonus_app/BeliefEstimationPage.html",
         who="All participants", instr=False, blocks=[
        ('p', "We would like to know your perception of donation and deduction behavior in this study. Please provide your best estimate for the following two questions:"),
        ('field', "What percentage of participants in this study do you think donated? (0-100%)"),
        ('field', "What percentage of donors in this study do you think deducted their donation? (0-100%)"),
        ('button', "Submit"),
        ('p', "[Validation messages: \"Please enter a percentage between 0 and 100 for donation percentage.\" / "
              "\"Please enter a percentage between 0 and 100 for deduction percentage.\"]"),
    ]),
    dict(part="Earnings, donation and deduction", title="Payment Instructions", tpl="bonus_app/IBANPaymentPage.html",
         who="All participants; donors see the first variant at the dedicated computer, non-donors the second at their own terminal", instr=True, blocks=[
        ('h', "Payment Identifiers"),
        ('p', "Session ID: [session code] 📄"),
        ('p', "Participant code: [participant code] 📄"),
        ('p', "Experiment code: 2025_001 📄"),
        ('note', "The 📄 icon copies the value to the clipboard and shows the browser message \"Copied to clipboard!\"."),
        ('variant', "Donors (at the dedicated computer)", [
            ('p', "Click the button below to proceed to the payment tool."),
            ('button', "Proceed to Payment Survey"),
            ('note', "Opens the payment survey (Appendix A) in a new browser tab."),
            ('field', "Unlabelled text field for the experimenter's release password"),
            ('p', "[While the field does not contain a valid password: \"Please proceed to the payment survey.\"]"),
            ('button', "Submit"),
            ('note', "The Submit button stays inactive until the experimenter types the release password after checking that the payment survey was submitted."),
        ]),
        ('variant', "Non-donors, payment information not yet received", [
            ('p', "Click the button below to proceed to the payment survey. After submitting your information you will be brought back to this page."),
            ('button', "Proceed to Payment Survey"),
            ('p', "Already submitted your information? Check again."),
            ('field', "Unlabelled text field, hint below it: \"For the experimenter only.\""),
            ('p', "[While the field does not contain a valid password: \"Please proceed to the payment survey.\"]"),
            ('button', "Submit (inactive)"),
        ]),
        ('variant', "Non-donors, payment information received", [
            ('p', "**✅ We have received your payment information.** Click Submit to continue."),
            ('button', "Submit"),
        ]),
        ('variant', "Non-donors, survey app could not be reached", [
            ('p', "**We could not verify your payment information automatically.** If you have not done so yet, please fill in the payment survey "
                  "via the button below. Afterwards, raise your hand and wait for the experimenter."),
            ('button', "Proceed to Payment Survey"),
            ('field', "Unlabelled text field, hint below it: \"For the experimenter only.\""),
            ('button', "Submit (inactive until the experimenter enters the release password)"),
        ]),
        ('p', "[Server-side error messages on submit: \"We have not received your payment information yet. Please complete the payment survey first, "
              "then return to this page.\" / \"Invalid password entered! Please check with the experimenter.\"]"),
        ('note', "For non-donors the survey opens in the same tab and returns to this page afterwards; the experiment then checks with the survey app "
                 "whether the data has arrived."),
    ]),
    dict(part="Exit questions", title="Reflection on Your Donation Decision", tpl="bonus_app/DonationReasonPage.html",
         who="All participants", instr=False, blocks=[
        ('p', "We are interested in what was driving your donation decision. Please describe briefly the thoughts that came to your mind while making this decision, in the order they arose."),
        ('p', "*Typical answers are 3 to 5 sentences long.*"),
        ('field', "Free-text box (multi-line, required)"),
        ('button', "Submit"),
    ]),
    dict(part="Exit questions", title="Reflection on Your Deduction Decision", tpl="bonus_app/DeductionReasonPage.html",
         who="Donors only (non-donors skip this page)", instr=False, blocks=[
        ('p', "We are interested in what was driving your deduction decision. Please describe briefly the thoughts that came to your mind while making this decision, in the order they arose."),
        ('p', "*Typical answers are 3 to 5 sentences long.*"),
        ('field', "Free-text box (multi-line, required)"),
        ('button', "Submit"),
    ]),
    dict(part="Exit questions", title="Experiment Concluded", tpl="bonus_app/FarewellPage.html",
         who="All participants", instr=False, blocks=[
        ('p', "Thank you for participating in our experiment! We greatly appreciate your time and effort."),
        ('p', "The experiment is now concluded. Your payment will be processed once the overall experiment is finished, which will occur within this or the next week. You are free to leave now."),
        ('p', "If you have any questions or concerns, please feel free to reach out to us at paul.hild@hu-berlin.de."),
        ('p', "**Thank you once again, and we hope you have a wonderful day!**"),
    ]),
]

APPENDIX = dict(part="Appendix A: external payment survey", title="Payment Survey", tpl="wu_payment_survey/public/index.html (separate web app)",
    who="All participants, opened from the Payment Instructions page", instr=False, blocks=[
    ('p', "**Session ID:** [session code]"),
    ('p', "**Participant ID:** [participant code]"),
    ('h', "Enter Your Payment Information"),
    ('field', "Full Name: (placeholder \"Enter your full name\", required)"),
    ('field', "Email Address (@): (placeholder \"Enter your email address\", required)"),
    ('field', "City: (placeholder \"Enter your city\", required)"),
    ('field', "ZIP Code: (placeholder \"Enter your ZIP code\", required)"),
    ('field', "IBAN: (placeholder \"Enter your IBAN\", required)"),
    ('p', "[Error on an invalid IBAN: \"Invalid IBAN. Please enter a valid IBAN.\"]"),
    ('button', "Validate"),
    ('button', "Submit"),
    ('p', "[After submission, non-donors: \"Submission successful! Click the button below to return to the experiment.\" followed by a button "
          "\"Return to the experiment\". Donors: \"Submission successful! Please wait until you are told to go back to your seat.\" "
          "On a failure: \"An error occurred. Please try again.\"]"),
    ('note', "Name, e-mail address, city, ZIP code and IBAN are stored in a separate database of the payment survey, linked to the experiment data only through the "
             "session and participant codes."),
])

# ----------------------------------------------------------------------------------------------
# docx helpers
# ----------------------------------------------------------------------------------------------
GREY = RGBColor(0x60, 0x60, 0x60)
BLUE = RGBColor(0x1F, 0x4E, 0x79)

def add_runs(par, text, base_italic=False, size=None):
    """Inline markup: **bold**, *italic*."""
    tokens = re.split(r"(\*\*.+?\*\*|\*.+?\*)", text)
    for t in tokens:
        if not t:
            continue
        bold = t.startswith("**")
        ital = (not bold) and t.startswith("*") and t.endswith("*") and len(t) > 2
        if bold:
            t = t[2:-2]
        elif ital:
            t = t[1:-1]
        r = par.add_run(t)
        r.bold = bold
        r.italic = ital or base_italic
        if size:
            r.font.size = Pt(size)
    return par

def shade(par, hex_fill):
    pPr = par._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hex_fill)
    pPr.append(shd)

def left_border(par, hex_color):
    pPr = par._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single'); left.set(qn('w:sz'), '18'); left.set(qn('w:space'), '6'); left.set(qn('w:color'), hex_color)
    pbdr.append(left); pPr.append(pbdr)

def note(doc, text, indent=0):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(indent)
    r = p.add_run("Note (not shown to participants): ")
    r.italic = True; r.bold = True; r.font.size = Pt(9); r.font.color.rgb = GREY
    for run in add_runs(p, text, base_italic=True, size=9).runs[1:]:
        run.font.color.rgb = GREY
    return p

def seq_table(doc, samples, indent):
    for i, (seq, resp) in enumerate(samples, 1):
        p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(indent)
        r = p.add_run(f"Sequence {i}:"); r.bold = True
        t = doc.add_table(rows=2, cols=8); t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.LEFT
        for j, v in enumerate(seq):
            c = t.cell(0, j); c.text = str(v); c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        t.cell(1, 0).text = ""
        for j, v in enumerate(resp):
            c = t.cell(1, j + 1); c.text = str(v); c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = c.paragraphs[0].runs[0]
            if j == 6:
                run.bold = True; run.font.color.rgb = RGBColor(0x1E, 0x7E, 0x34)
            else:
                run.font.color.rgb = BLUE
        for row in t.rows:
            for c in row.cells:
                c.width = Cm(1.1)
        doc.add_paragraph()
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(indent)
    add_runs(p, "*Top row: the sequence. Bottom row: the responses, offset by one box as on screen; the seventh response is highlighted in green.*", size=9)

def render_blocks(doc, blocks, indent=0.0):
    for b in blocks:
        kind = b[0]
        if kind == 'p':
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(indent); add_runs(p, b[1])
        elif kind == 'h':
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(indent)
            p.paragraph_format.space_before = Pt(8)
            r = p.add_run(b[1]); r.bold = True; r.font.size = Pt(12); r.font.color.rgb = BLUE
        elif kind == 'ul':
            for item in b[1]:
                p = doc.add_paragraph(style='List Bullet'); p.paragraph_format.left_indent = Cm(indent + 0.63); add_runs(p, item)
        elif kind == 'radio':
            for item in b[1]:
                p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(indent + 0.5); add_runs(p, "○  " + item)
        elif kind == 'field':
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(indent)
            r = p.add_run("▭ Input field: "); r.font.color.rgb = GREY
            add_runs(p, b[1])
        elif kind == 'button':
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(indent)
            r = p.add_run(f"[ {b[1]} ]"); r.bold = True; r.font.color.rgb = BLUE
            r2 = p.add_run("  (button)"); r2.font.size = Pt(9); r2.font.color.rgb = GREY
        elif kind == 'note':
            note(doc, b[1], indent)
        elif kind == 'hr':
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(indent)
            r = p.add_run("―――――――――――――――――――――"); r.font.color.rgb = GREY
        elif kind == 'img':
            doc.add_picture(str(b[1]), width=Cm(b[2]))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif kind == 'seqtable':
            seq_table(doc, b[1], indent)
        elif kind == 'variant':
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(indent)
            p.paragraph_format.space_before = Pt(6)
            r = p.add_run("▶ Shown only to: " + b[1]); r.bold = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x8A, 0x4B, 0x00)
            shade(p, "FFF4E0")
            render_blocks(doc, b[2], indent + 0.75)
        else:
            raise ValueError(kind)

def page_header(doc, number, page):
    doc.add_heading(f"{number}  {page['title']}", level=2)
    p = doc.add_paragraph()
    r = p.add_run(f"Shown to: {page['who']}.   Template: {page['tpl']}")
    r.font.size = Pt(9); r.font.color.rgb = GREY; r.italic = True
    shade(p, "F2F2F2")

def footer_pagenum(section, label):
    p = section.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(label + "   |   page "); r.font.size = Pt(8); r.font.color.rgb = GREY
    for tag, txt in (('begin', None), (None, 'PAGE'), ('end', None)):
        run = p.add_run(); run.font.size = Pt(8); run.font.color.rgb = GREY
        if tag:
            el = OxmlElement('w:fldChar'); el.set(qn('w:fldCharType'), tag); run._r.append(el)
        else:
            el = OxmlElement('w:instrText'); el.set(qn('xml:space'), 'preserve'); el.text = txt; run._r.append(el)

def build(version, out_path):
    instructions_only = (version == 1)
    pages = [p for p in PAGES if (p['instr'] or not instructions_only)]

    doc = Document()
    st = doc.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2)

    subtitle = "Version 1: instruction pages only" if instructions_only else "Version 2: all pages"
    doc.add_heading("Participant-facing text of the tax-deduction experiment", level=0)
    p = doc.add_paragraph(); r = p.add_run(subtitle); r.bold = True; r.font.size = Pt(14)
    doc.add_paragraph(f"Humboldt University Berlin and Julius-Maximilians University Würzburg. Generated on {TODAY} from the oTree "
                      f"project 'tax_deduction_experiment' (commit {COMMIT}), session configuration 'main_experiment' with the site setting "
                      f"university = hu_berlin.")

    doc.add_heading("How to read this document", level=1)
    render_blocks(doc, [
        ('p', "Every page a participant can see is listed in the order in which it appears, grouped by the four parts of the experiment. "
              "The text was transcribed from the page templates and the page code, not from screenshots, so that all conditional "
              "variants could be included. Formatting (bold, italic, lists, emoji) follows the screen."),
        ('ul', ["**[Square brackets]** mark values that are filled in at run time (amounts, codes, counters) or describe an on-screen element that is not text, such as the number boxes.",
                "**▶ Shown only to:** introduces a block that appears only under the stated condition (donor status, treatment, task version, validation state). Everything outside such blocks is shown to everyone who reaches the page.",
                "**[ Label ] (button)** is a button; **○** is a radio-button option; **▭ Input field** is a text or number field.",
                "**Note (not shown to participants)** is an explanation for the reader of this document and never appears on screen."]),
        ('p', "Not covered here: the verbal and printed instructions the experimenter gives at the start of a session, the standard oTree wait page, "
              "and browser-level messages. " + ("Pages without instruction content (questionnaires, the task screens themselves, the exit questions "
              "and the farewell page) are omitted in this version; version 2 of this document contains them." if instructions_only else
              "Appendix A documents the separate payment-survey web page in which participants enter their payment details.")),
    ])

    doc.add_heading("Flow of a session", level=1)
    render_blocks(doc, [
        ('p', "1. Consent and demographics  →  2. Task instructions, comprehension check and practice  →  3. The task: two versions of up to 30 "
              "sequences with 6 minutes each  →  4. Earnings, donation decision, announcement, deduction decision, beliefs, payment details  →  5. Exit questions and farewell."),
        ('p', "After the donation decision, donors are called one by one to a dedicated computer where they take the deduction decision and enter their "
              "payment details (accompanied by the experimenter; in the 'Observability' treatment a proctor is announced). Non-donors go through the same "
              "pages on their own terminal."),
    ])

    doc.add_heading("Pages in this document", level=1)
    numbered = []
    part_no = 0; page_no = 0; last_part = None
    for pg in pages:
        if pg['part'] != last_part:
            part_no += 1; page_no = 0; last_part = pg['part']
        page_no += 1
        numbered.append((f"{part_no}.{page_no}", pg))
    if not instructions_only:
        numbered.append(("A.1", APPENDIX))
    for num, pg in numbered:
        p = doc.add_paragraph(style='List Bullet'); add_runs(p, f"{num}  {pg['title']}")

    last_part = None
    for num, pg in numbered:
        if pg['part'] != last_part:
            doc.add_page_break()
            last_part = pg['part']
            doc.add_heading(("Part " + num.split('.')[0] + ": " if not num.startswith("A") else "") + pg['part'], level=1)
        page_header(doc, num, pg)
        render_blocks(doc, pg['blocks'])

    footer_pagenum(doc.sections[0], f"Tax-deduction experiment, participant-facing text, {subtitle.lower()}")
    doc.save(out_path)
    return numbered

if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    n1 = build(1, OUT_DIR / "Participant_instructions_v1_instruction_pages.docx")
    n2 = build(2, OUT_DIR / "Participant_instructions_v2_all_pages.docx")
    print("v1 pages:", len(n1)); print("v2 pages:", len(n2))
    for num, pg in n2:
        print(f"  {num:5} {'[v1]' if pg.get('instr') else '    '} {pg['title']}")
