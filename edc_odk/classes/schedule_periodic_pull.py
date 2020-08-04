from django_q.tasks import schedule


class SchedulePeriodicPull:

    def schedule_odk_data_pull(self):
        """
        Schedule to pull data from the odk aggregate server every minute,
        from 7a.m to 16:59, Monday through Friday.
        """
        schedule(
            'edc_odk.tasks.pull_all_data_from_odk',
            schedule_type='C',
            cron='* 7-16 * * 1-5')
