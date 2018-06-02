from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

# Create your views here.
from .models import Item, Feed, Settings

class UnreadView(LoginRequiredMixin, generic.ListView):
    template_name = 'feedsite/unread.html'
    model = Item
    max_items = 15

    def get_queryset(self):
        """
        Returns items that are not read.
        """
        firstId = self.request.GET.get("first", None)

        if firstId is not None:
            firstItem = get_object_or_404(Item, 
                feed__user=self.request.user, pk=firstId, isRead=False)
            items = list(Item.objects.filter(feed__user=self.request.user, 
                isRead=False).order_by("-published"))
            try:
                firstIndex = items.index(firstItem)
                return items[firstIndex : firstIndex+self.max_items]
            except: 
                return items[:self.max_items]
        else:
            return Item.objects.filter(feed__user=self.request.user, 
                isRead=False).order_by("-published")[:self.max_items]

    def get_context_data(self, **kwargs):
        context = super(UnreadView, self).get_context_data(**kwargs)
        context["max_items"] = self.max_items
        return context

@login_required
def markread(request, item_id):
    item = get_object_or_404(Item, feed__user=request.user, pk=item_id)
    try:
        item.isRead = True
        item.save()
    finally:
        return HttpResponseRedirect(reverse("feedsite:unread"))

@login_required
def markreadlist(request, first, next):
    firstItem = get_object_or_404(Item, 
                feed__user=request.user, pk=first, isRead=False)
    nextItem = get_object_or_404(Item, 
                feed__user=request.user, pk=next, isRead=False)
    items = list(Item.objects.filter(feed__user=request.user, 
                isRead=False).order_by("-published"))
    try:
        for i in items[items.index(firstItem) : items.index(nextItem)]:
            i.isRead = True
            i.save()
    finally:
        url = "{base_url}?first={querystring}".format(
            base_url=reverse("feedsite:unread"),
            querystring=next
        )
        return HttpResponseRedirect(url)

@login_required
def markreadrest(request, first):
    firstItem = get_object_or_404(Item, 
                feed__user=request.user, pk=first, isRead=False)
    items = list(Item.objects.filter(feed__user=request.user, 
                isRead=False).order_by("-published"))
    try:
        for i in items[items.index(firstItem) : ]:
            i.isRead = True
            i.save()
    finally:
        return HttpResponseRedirect(reverse("feedsite:unread"))

@login_required
def markunread(request, item_id):
    item = get_object_or_404(Item, feed__user=request.user, pk=item_id)
    try:
        item.isRead = False
        item.save()
    finally:
        return HttpResponseRedirect(reverse("feedsite:unread"))

class HistoryView(LoginRequiredMixin, generic.ListView):
    template_name = 'feedsite/history.html'
    model = Item
    paginate_by=30

    def get_queryset(self):
        """
        Returns items that are read.
        """
        return Item.objects.filter(feed__user=self.request.user, 
                isRead=True).order_by("-published")

class FeedsView(LoginRequiredMixin, generic.ListView):
    template_name = 'feedsite/feeds.html'
    model = Feed

    def get_queryset(self):
        """
        Returns Feeds that belong to the user
        """
        return Feed.objects.filter(user=self.request.user)

class FeedCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Feed
    fields = ['title', 'url']
    template_name ='feedsite/feed_create.html'
    success_url = reverse_lazy('feedsite:feeds') 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FeedUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Feed
    fields = ['title', 'url']
    template_name ='feedsite/feed_update.html'
    success_url = reverse_lazy('feedsite:feeds') 

    def get_object(self, queryset=None):
        return Feed.objects.get(user=self.request.user, pk=self.kwargs['pk'])

class FeedDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Feed
    success_url = reverse_lazy('feedsite:feeds') 
    template_name ='feedsite/feed_delete.html'

    def get_object(self, queryset=None):
        return Feed.objects.get(user=self.request.user, pk=self.kwargs['pk'])

class SettingsView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Settings
    template_name = 'feedsite/settings.html'
    success_url = reverse_lazy("feedsite:settings")
    fields = ["delete_older_than_days", "timezone"]

    def get_object(self, queryset=None):
        try: 
            return Settings.objects.get(user=self.request.user)
        except:
            s = Settings()
            s.user = self.request.user
            s.save()
            return s
