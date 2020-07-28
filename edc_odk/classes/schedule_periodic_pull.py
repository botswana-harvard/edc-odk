from django_q.tasks import schedule


class SchedulePeriodicPull:

    def schedule_odk_data_pull(self):
        """
        Schedule to pull data from the odk aggregate server every 5 minutes.
        """
        schedule(
            'edc_odk.tasks.pull_all_data_from_odk',
            schedule_type='C',
            cron='*/5 * * * 1-7')
