from django.db import models, IntegrityError


class HideableModelManager(models.Manager):
    """ 
    A model manager to allow hiding or 'deleting' objects for a given Model 
    without actually removing them from the database. Overrides the regular 
    query methods ('get', 'filter', 'all') to automatically ignore any 
    hidden/deleted objects. The 'include_hidden' can be passed to any of the
    three methods to include these hidden objects as part of the query.
    
    To use this Manager, simply create a Model that extends 
    AbstractHideableModel below. If you want to write your own Model that has
    a custom hidden field boolean, create a subclass of this manager that sets 
    'hidden_name_field' to match the name of the desired field, and use the new
    manager subclass for the 'objects' of your custom Model.
    
    NOTES: 
    
    1) Use the get_or_create method with caution. If you try to get_or_create
       an object that already exists and has been hidden, it will throw a
       HiddenObjectError. This is to prevent accidentally giving users access 
       to objects that they would not otherwise be able to edit themselves due 
       to being "deleted". 
       
       This behavior can be overridden by explicitly including the hidden field 
       as part of the lookup params (e.g. deleted=True) or the defaults.
       
    2) If the 'include_hidden' param is specified and it conflicts with the 
       actual hidden field's lookup value (e.g., include_hidden=False and 
       deleted=True), 'include_hidden' will override the hidden field lookup
       value.
    
    """
    hidden_field_name = "deleted"
    
    def _kwargs_for_query(self, kwargs):
        # filter out objects with the flag indicating that they should be 
        # hidden, unless specified otherwise
        add_hidden_param = not self.hidden_field_name in kwargs
        if 'include_hidden' in kwargs:
            add_hidden_param = not kwargs.pop('include_hidden')
        
        if add_hidden_param:
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
        # Overridden from parent class to avoid skipping 'deleted' objects.
        #
        # If the hidden field is included either as part of the kwargs or the
        # defaults, it will be used to determine whether to include hidden
        # objects in the 'get' search. If hidden objects are not included, but 
        # the lookup parameters would return a result if hidden objects had
        # been included, it raises a HiddenObjectError instead to prevent 
        # giving users/apps accidental access to objects for which they might 
        #not have permission.
        
        '''
        case 1: straightforward
        case 2: include_hidden brings a result, but not regular, and include_hidden was intentional
        case 3: include_hidden brings a result, but not regular, and include_hidden was not included
        '''
        include_hidden = (self.hidden_field_name in kwargs or
                          (defaults and self.hidden_field_name in defaults))
        
        try:
            obj = self.get(include_hidden=include_hidden, **kwargs)
            if not include_hidden and self.filter(include_hidden=True, **lookup):
                raise HiddenObjectError('Object exists but is hidden. Lookup: %s'
                                        % lookup)
            return obj, False
        except self.model.DoesNotExist:
            return self.create(**kwargs)


class AbstractHideableModel(models.Model):
    """
    Abstract Django model that provides support for using the 'deleted' field
    to hide objects instead of deleting them.
    """
    deleted = models.BooleanField(default=False)
    objects = HideableModelManager()
    
    class Meta:
        abstract = True


class HiddenObjectError(IntegrityError):
    pass