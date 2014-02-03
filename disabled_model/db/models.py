from django.db import models


class HideableModelManager(models.Manager):
    """ 
    A model manager to allow hiding or 'deleting' objects for a given model 
    without actually removing them from the database. Overrides the regular 
    query methods ('get', 'filter', 'all') to automatically ignore any 
    hidden/deleted objects. The 'include_hidden' can be passed to any of the
    three methods to include these hidden objects as part of the query.
    
    To use this Manager, create a Model class with a BooleanField to indicate 
    whether a given object should be hidden/disabled. If the field is not 
    called 'deleted', create a subclass of this manager that sets 
    'hidden_name_field' to match the name of the desired field.
    
    NOTES: 
    
    1) Use the get_or_create method with caution. While the get_or_create does 
       recognize hidden models to avoid creating database conflicts, this can 
       also cause confusion for users if a view does a get_or_create matching a 
       hidden object but the user is unable to see the object just created in 
       the UI because it ends up being hidden.
    
    """
    hidden_field_name = "deleted"
    
    def _kwargs_for_query(self, kwargs):
        # filter out objects with the flag indicating that they should be 
        # hidden, unless specified otherwise
        if kwargs.get('include_hidden', False):
            kwargs.pop('include_hidden')
        else:
            kwargs[self.hidden_field_name] = False
        return kwargs
    
    def all(self, include_hidden=False):
        """ 
        Custom all method that excludes hidden objects by default. If the
        'include_hidden' kwarg is passed and is True, hidden objects will also
        be included in the query.
        """
        if include_hidden:
            return super(HideableModelManager, self).all()
        return self.filter()
    
    def filter(self, **kwargs):
        """ 
        Custom filter method that excludes hidden objects by default. If the 
        'include_hidden' kwarg is passed and is True, hidden objects will also 
        be included in the query.
        """
        kwargs = self._kwargs_for_query(kwargs)
        return super(HideableModelManager, self).filter(**kwargs)
    
    def get(self, **kwargs):
        """ 
        Custom get method that excludes hidden objects by default. If
        the 'include_hidden' kwarg is passed and is True, hidden objects will
        also be included when running the 'get' method.
        """
        kwargs = self._kwargs_for_query(kwargs)
        return super(HideableModelManager, self).get(**kwargs)
    
    def get_or_create(self, defaults=None, **kwargs):
        # Overridden from parent class to avoid skipping 'deleted' objects
        if not (self.hidden_field_name in kwargs or 
                (defaults and self.hidden_field_name not in defaults)):
            defaults = defaults or {}
            defaults[self.hidden_field_name] = False
        
        lookup, params = self._extract_model_params(defaults, **kwargs)
        self._for_write = True
        try:
            return self.get(include_hidden=True, **lookup), False
        except self.model.DoesNotExist:
            return self._create_object_from_params(lookup, params)
