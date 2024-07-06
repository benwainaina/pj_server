from entry.models import Entry, EntryCategory
from django.db.models import Q
from datetime import datetime

class FilterHelper(object):
    def __init__(self, *args,**kwargs) -> None:
        self.results = []
        self.user_instance = kwargs.get('user')
        self.filter_fields = kwargs.get('filter_fields')
        self.decide_on_filter()
        
    def decide_on_filter(self):
        all_results = self._filter_get_all_entries()
        if len(self.filter_fields.keys()) == 0:
            self.results = self._marshall_data(all_results)
            return
        
        # if there is a category in the filters, apply it
        if self.filter_fields.get('category'):
            results = self._filter_entries_by_category(all_results)
        
        # if there is a selected period in the filters, apply it
        if self.filter_fields.get('period'):
            results = self._filter_entries_by_period(results)
            
        self.results = self._marshall_data(results)
        
    def _filter_get_all_entries(self):
        return Entry.objects.all()
    
    def _filter_entries_by_category(self, all_results):
        category = self.filter_fields.get('category')
        if category == 'all':
            return all_results
        try:
            return all_results.filter(category=EntryCategory.objects.get(
                category_uuid=self.filter_fields.get('category')
            ))
        except:
            return []
    
    def _filter_entries_by_period(self, all_results):
        period = self.filter_fields.get('period')
        if period == 'all':
            return all_results
        return all_results.filter(
            Q(date__gte=period.get('start')) & Q(date__lte=period.get('end')),
        )
    
    def _marshall_data(self, instances):
        return [
            {
                'title': entry.title,
                'content': entry.content,
                'category': str(entry.category.category_uuid),
                'date': entry.date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'uuid': str(entry.entry_uuid)
            } for entry in instances
        ]
    