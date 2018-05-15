from django_cron import CronJobBase, Schedule

class FetchSevran(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'sevran.cron.fetch_sevran'

    def do(self):
        print('je s')
