from haystack import indexes
from helpdesk.models import Ticket


class TicketIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='description', null=True)
    followup_str = indexes.CharField(model_attr='followup_str')
    title = indexes.CharField(model_attr='title')
    assigned_to = indexes.CharField(model_attr='assigned_to', null=True)
    submitted_by = indexes.CharField(null=True)
    priority_str = indexes.CharField(model_attr='priority_str')
    status_str = indexes.CharField(model_attr='status_str')
    queue = indexes.CharField(model_attr='queue')
    #tags = indexes.MultiValueField(null=True)
    tags = indexes.MultiValueField(null=True)
    tags_str = indexes.CharField(model_attr='tags_str', null=True)

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_model(self):
        return Ticket

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
