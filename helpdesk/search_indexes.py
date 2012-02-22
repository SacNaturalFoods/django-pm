import datetime
from haystack import indexes
from helpdesk.models import Ticket


class TicketIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    queue = indexes.CharField(model_attr='queue', faceted=True)
    submitter_email = indexes.CharField(model_attr='submitter_email', faceted=True)

    def get_model(self):
        return Ticket

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
        return self.get_model().objects.all()
