import asyncio
from datetime import datetime, timedelta

from src.config import settings
from src.handlers.common.main import user_repository
from src.helpers.path_utils import PathUtils
from src.loader import bot
from src.repository.events import EventRepository
from src.repository.sended_events import SendedEventRepository
from src.services.notifications import EventNotificationService

CHECK_INTERVAL = 60

event_notification_service = EventNotificationService(bot, user_repository)

events_file_path = PathUtils.get_events_path()
events_repo = EventRepository(events_file_path)

sended_events_path = PathUtils.get_sended_events_path()
sended_events_repo = SendedEventRepository(sended_events_path)


async def scheduler():
    notify_delta = timedelta(minutes=settings.scheduler.notify_before_minutes)

    while True:
        now = datetime.now()

        for event in events_repo.get_events():
            notify_at = event.date - notify_delta

            if notify_at > now:
                continue

            if not sended_events_repo.is_sended(event):
                await event_notification_service.send_event(event)
                sended_events_repo.mark_as_sended(event)

        await asyncio.sleep(CHECK_INTERVAL)
