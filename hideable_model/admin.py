from django.contrib import admin


class HideableModelAdmin(admin.ModelAdmin):
    """
    ModelAdmin class to work with descendents of AbstractHideableModel. This
    admin interface only allows superusers to work with hidden objects. If this 
    admin class is used for hideable models, the interface will have the 
    following properties:
    
    1) Superusers can see all hidden objects, and deleting an object as a 
       superuser deletes the object from the database.
       
    2) Staff users can see any objects that aren't hidden. Deleting a hideable
       object results in the hidden flag being set.
    """
    pass


class StaffHideableModelAdmin(admin.ModelAdmin):
    """
    ModelAdmin class to work with descendents of AbstractHideableModel. This
    admin interface allows both superusers and staff with the usual Django model
    permissions to work with hidden objects:
    
    1) Superusers and staff can see all hidden objects.
    
    2) Superusers and staff are able to delete hidden objects normally from the
       database, as per the expected Django UI behavior.
    """
    pass