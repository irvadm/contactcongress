from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

import sys
sys.path.append('..')

from members.updater import MemberUpdater


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "djangojobstore")


@register_job(scheduler, "interval", seconds=14400, replace_existing=True)
def member_tasks():
    """ Job function added to task scheduler. """
    updater = MemberUpdater()
    updater.update_members(chamber='house')
    updater.update_members(chamber='senate')
    # updater.update_member_images()

register_events(scheduler)

scheduler.start()
print("Scheduler started!")