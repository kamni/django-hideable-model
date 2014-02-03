from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.test import TestCase

from hideable_model.models import HiddenModel, CustomHiddenModel
from hideable_model.db.models import *


class HideableModelManagerTests(TestCase):
    def test_all(self):
        pass
    
    def test_all__include_hidden(self):
        pass
    
    def test_filter(self):
        # default, no existing models
        self.assertEquals([], list(HiddenModel.objects.filter(name="test-9334")))
        
        # default, not deleted
        hm1 = HiddenModel.objects.create(name="test-9334", deleted=False)
        hm2 = HiddenModel.objects.create(name="test-9334", deleted=False)
        self.assertEquals([hm1, hm2], list(HiddenModel.objects.filter(name="test-9334")))
        
        # default, deleted
        HiddenModel.objects.create(name="test-9334", deleted=True)
        self.assertEquals([hm1, hm2], list(HiddenModel.objects.filter(name="test-9334")))
        
        # custom, no existing models
        self.assertEquals([], list(CustomHiddenModel.objects.filter(name="test-2861")))
        
        # custom, not deleted
        chm1 = CustomHiddenModel.objects.create(name="test-2861", disabled=False)
        chm2 = CustomHiddenModel.objects.create(name="test-2861", disabled=False)
        self.assertEquals([chm1, chm2], list(CustomHiddenModel.objects.filter(name="test-2861")))
        
        # custom, deleted
        CustomHiddenModel.objects.create(name="test-2861", disabled=True)
        self.assertEquals([chm1, chm2], list(CustomHiddenModel.objects.filter(name="test-2861")))
    
    def test_filter__include_hidden(self):
        # default, no existing models
        self.assertEquals([], list(HiddenModel.objects.filter(include_hidden=True,
                                                              name="test-8588")))
        
        # default, deleted and not deleted objects
        hm1 = HiddenModel.objects.create(name="test-8588", deleted=False)
        hm2 = HiddenModel.objects.create(name="test-8588", deleted=False)
        hm3 = HiddenModel.objects.create(name="test-8588", deleted=True)
        self.assertEquals([hm1, hm2, hm3], list(HiddenModel.objects.filter(include_hidden=True,
                                                                           name="test-8588")))
        
        # custom, no existing models
        self.assertEquals([], list(CustomHiddenModel.objects.filter(include_hidden=True,
                                                                    name="test-0068")))
        
        # custom, deleted and not deleted objects
        chm1 = CustomHiddenModel.objects.create(name="test-0068", disabled=False)
        chm2 = CustomHiddenModel.objects.create(name="test-0068", disabled=False)
        chm3 = CustomHiddenModel.objects.create(name="test-0068", disabled=True)
        self.assertEquals([chm1, chm2, chm3], list(CustomHiddenModel.objects.filter(include_hidden=True,
                                                                                    name="test-0068")))
    
    def test_get(self):
        # default, no existing models
        self.assertRaises(HiddenModel.DoesNotExist, HiddenModel.objects.get, name="test-9322")
        
        # default, deleted
        HiddenModel.objects.create(name="test-9322", deleted=True)
        self.assertRaises(HiddenModel.DoesNotExist, HiddenModel.objects.get, name="test-9322")
        
        # default, not deleted
        hm1 = HiddenModel.objects.create(name="test-9322", deleted=False)
        self.assertEquals(hm1, HiddenModel.objects.get(name="test-9322"))
        
        # custom, no existing models
        self.assertRaises(CustomHiddenModel.DoesNotExist, CustomHiddenModel.objects.get, name="test-2457")
        
        # custom, deleted
        CustomHiddenModel.objects.create(name="test-9322", disabled=True)
        self.assertRaises(CustomHiddenModel.DoesNotExist, CustomHiddenModel.objects.get, name="test-2457")
        
        # custom, not deleted
        chm1 = CustomHiddenModel.objects.create(name="test-2457", disabled=False)
        self.assertEquals(chm1, CustomHiddenModel.objects.get(name="test-2457"))
    
    def test_get__include_hidden(self):
        # default, no existing models
        self.assertRaises(HiddenModel.DoesNotExist, HiddenModel.objects.get, 
                          include_hidden=True, name="test-5487")
        
        # default, deleted
        hm1 = HiddenModel.objects.create(name="test-5487", deleted=True)
        self.assertEquals(hm1, HiddenModel.objects.get(include_hidden=True,
                                                       name="test-5487"))
        
        # default, not deleted
        HiddenModel.objects.create(name="test-5487", deleted=False)
        self.assertRaises(MultipleObjectsReturned, HiddenModel.objects.get, 
                          include_hidden=True, name="test-5487")
        
        # custom, no existing models
        self.assertRaises(CustomHiddenModel.DoesNotExist, CustomHiddenModel.objects.get, 
                          include_hidden=True, name="test-3014")
        
        # custom, deleted
        chm1 = CustomHiddenModel.objects.create(name="test-3014", disabled=True)
        self.assertEquals(chm1, CustomHiddenModel.objects.get(include_hidden=True,
                                                              name="test-3014"))
        
        # custom, not deleted
        CustomHiddenModel.objects.create(name="test-3014", disabled=False)
        self.assertRaises(MultipleObjectsReturned, CustomHiddenModel.objects.get, 
                          include_hidden=True, name="test-3014")
    
    def test_get_or_create(self):
        # default
        
        # custom
        pass