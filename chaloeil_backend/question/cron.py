def test_task():
    """
    This is a test task that can be scheduled using cron.
    It currently does nothing but can be expanded in the future.
    """
    with open('/tmp/django_cron_test.log', 'a') as f:
        f.write('Test task executed successfully.\n')
