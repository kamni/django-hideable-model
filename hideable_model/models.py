import sys

from django.db import models




################################################################################
# Test Models -- Hack to deal with testrunner issues that ignore test models   #
# when using sqlite databases                                                  #
################################################################################

if 'test' in sys.argv:
    from hideable_model.db.models import HideableModelManager

    class HiddenModel(models.Model):
        name = models.CharField(max_length=10)
        deleted = models.BooleanField()
        objects = HideableModelManager() 
    
    
    class CustomHiddenManager(HideableModelManager):
        hidden_field_name = "disabled"
    
      
    class CustomHiddenModel(models.Model):
        name = models.CharField(max_length=10)
        disabled = models.BooleanField()
        objects = CustomHiddenManager()