from os import environ
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}

# Allow Heroku to serve your app
ALLOWED_HOSTS = ['charity-lab-9f7c7b493bc8.herokuapp.com']

DEBUG = False


SESSION_CONFIGS = [
    {
        'name': 'main_experiment',
        'display_name': 'Main Experiment with Consent and Task Instructions',
        'num_demo_participants': 2,  # Set this to the desired number of participants
        'app_sequence': ['disclaimer_consent', 'task_instructions', 'task', 'bonus_app'],
        'level_1_treatment': 'Observability',
    },
]

INSTALLED_APPS = [
    'otree',
    'disclaimer_consent',
    'task_instructions',
    'task',
    'bonus_app',
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=5.00, doc=""
)

PARTICIPANT_FIELDS = ['expiry', 'difficulty_order', 'final_round_correctness', 'final_round_correctness_task2']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2020228032173'

