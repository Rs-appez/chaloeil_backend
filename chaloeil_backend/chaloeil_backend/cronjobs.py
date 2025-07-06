CRONJOBS = [
    ('0 18 * * *', 'question.cron.create_questions_of_the_day',
     '>> /tmp/django_cron_test.log 2>&1'),

]
