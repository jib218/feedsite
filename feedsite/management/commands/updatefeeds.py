from django.core.management import BaseCommand
from feedsite.models import Feed, Item
from django.utils import timezone
from datetime import timedelta
from feedsite.util import clean_description

import feedparser as fp
import dateutil.parser as dp


class Command(BaseCommand):
    help = "Command for handling the feeds"

    def remove_old_items(self, f: Feed):
        time_threshold = timezone.now() - timedelta(
            days=f.user.settings.delete_older_than_days)
        f.item_set.filter(published__lte=time_threshold).delete()

    def updatefeed(self, f: Feed):
        parsedFeed = fp.parse(f.url)
        f.bozo = parsedFeed.bozo
        f.lastchecked = timezone.now()
        f.save()

        if f.bozo == True:
            return

        for entry in parsedFeed.entries:
            if not 'title' in entry:
                continue
            if not 'link' in entry:
                continue

            unique_id = entry.title

            if 'id' in entry:
                unique_id = entry.id

            if f.item_set.filter(unique_feed_id=unique_id).exists():
                continue

            item = Item()

            item.unique_feed_id = unique_id
            item.title = entry.title
            item.link = entry.link

            if 'description' in entry:
                item.description = entry.summary
            elif 'summary' in entry:
                item.description = entry.summary

            clean_description(item)

            if 'published' in entry:
                item.published = dp.parse(entry.published)
            elif 'date' in entry:
                item.published = dp.parse(entry.date)
            else:
                item.published = timezone.now()

            item.feed = f

            item.save()

    def handle(self, *args, **options):
        for f in Feed.objects.all():
            self.updatefeed(f)
            self.remove_old_items(f)
