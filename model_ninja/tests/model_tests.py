from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.test import TestCase

from hideable_model.models import HiddenModel, CustomHiddenModel
from hideable_model.db.models import *


class HideableModelManagerTests(TestCase):
    def test__kwargs_for_query(self):   
        # default, no include_hidden flag, no hidden field specified
        self.assertEquals({"test": 3, "deleted": False}, 
                          HiddenModel.objects._kwargs_for_query({"test": 3}))
        
        # default, no include_hidden flag, hidden field specified
        for deleted in (True, False):
            self.assertEquals({"test": 3, "deleted": deleted},
                              HiddenModel.objects._kwargs_for_query({"test": 3,
                                                                     "deleted": deleted}))
        
        # default, include_hidden flag, no hidden field specified
        self.assertEquals({"test": 3, "deleted": False},
                          HiddenModel.objects._kwargs_for_query({"test": 3,
                                                                 "include_hidden": False}))
        self.assertEquals({"test": 3},
                          HiddenModel.objects._kwargs_for_query({"test": 3,
                                                                 "include_hidden": True}))
        
        # default, include_hidden flag and hidden field specified
        for hidden in (True, False):
            for deleted in (True, False):
                self.assertEquals({"test": 3, "deleted": hidden and deleted},
                                  HiddenModel.objects._kwargs_for_query({"test": 3,
                                                                         "include_hidden": hidden,
                                                                         "deleted": deleted}))
        
        # custom, no include_hidden flag, no hidden field specified
        self.assertEquals({"test": 3, "disabled": False}, 
                          CustomHiddenModel.objects._kwargs_for_query({"test": 3}))
        
        # custom, no include_hidden flag, hidden field specified
        for disabled in (True, False):
            self.assertEquals({"test": 3, "disabled": disabled},
                              CustomHiddenModel.objects._kwargs_for_query({"test": 3,
                                                                           "disabled": disabled}))
        
        # custom, include_hidden flag, no hidden field specified
        self.assertEquals({"test": 3, "disabled": False},
                          CustomHiddenModel.objects._kwargs_for_query({"test": 3,
                                                                       "include_hidden": False}))
        self.assertEquals({"test": 3},
                          CustomHiddenModel.objects._kwargs_for_query({"test": 3,
                                                                       "include_hidden": True}))
        
        # custom, include_hidden flag and hidden field specified
        for hidden in (True, False):
            for disabled in (True, False):
                self.assertEquals({"test": 3, "disabled": hidden and disabled},
                                  CustomHiddenModel.objects._kwargs_for_query({"test": 3,
                                                                               "include_hidden": hidden,
                                                                               "disabled": disabled}))
    
    def test_all(self):
        HiddenModel.objects.all(include_hidden=True).delete()
        CustomHiddenModel.objects.all(include_hidden=True).delete()
        
        # default, no existing models
        self.assertEquals([], list(HiddenModel.objects.all()))
        
        # default, not deleted
        hm1 = HiddenModel.objects.create(name="test-7499", deleted=False)
        hm2 = HiddenModel.objects.create(name="test-9585", deleted=False)
        self.assertEquals([hm1, hm2], list(HiddenModel.objects.all()))
        
        # default, deleted
        HiddenModel.objects.create(name="test-5799", deleted=True)
        self.assertEquals([hm1, hm2], list(HiddenModel.objects.all()))
        
        # custom, no existing models
        self.assertEquals([], list(CustomHiddenModel.objects.all()))
        
        # custom, not deleted
        chm1 = CustomHiddenModel.objects.create(name="test-7499", disabled=False)
        chm2 = CustomHiddenModel.objects.create(name="test-9585", disabled=False)
        self.assertEquals([chm1, chm2], list(CustomHiddenModel.objects.all()))
        
        # custom, deleted
        CustomHiddenModel.objects.create(name="test-5799", disabled=True)
        self.assertEquals([chm1, chm2], list(CustomHiddenModel.objects.all()))
    
    def test_all__include_hidden(self):
        HiddenModel.objects.all(include_hidden=True).delete()
        CustomHiddenModel.objects.all(include_hidden=True).delete()
        
        # default, no existing models
        self.assertEquals([], list(HiddenModel.objects.all(include_hidden=True)))
        
        # default, not deleted
        hm1 = HiddenModel.objects.create(name="test-3241", deleted=False)
        hm2 = HiddenModel.objects.create(name="test-8009", deleted=False)
        self.assertEquals([hm1, hm2], list(HiddenModel.objects.all(include_hidden=True)))
        
        # default, deleted
        hm3 = HiddenModel.objects.create(name="test-4117", deleted=True)
        self.assertEquals([hm1, hm2, hm3], list(HiddenModel.objects.all(include_hidden=True)))
        
        # custom, no existing models
        self.assertEquals([], list(CustomHiddenModel.objects.all(include_hidden=True)))
        
        # custom, not deleted
        chm1 = CustomHiddenModel.objects.create(name="test-3241", disabled=False)
        chm2 = CustomHiddenModel.objects.create(name="test-8009", disabled=False)
        self.assertEquals([chm1, chm2], list(CustomHiddenModel.objects.all(include_hidden=True)))
        
        # custom, deleted
        chm3 = CustomHiddenModel.objects.create(name="test-4117", disabled=True)
        self.assertEquals([chm1, chm2, chm3], list(CustomHiddenModel.objects.all(include_hidden=True)))
    
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
        # default, model doesn't exist, no defaults or hidden field specified
        hm1, created = HiddenModel.objects.get_or_create(name="test-1144")
        self.assertFalse(hm1.deleted)
        self.assertTrue(created)
        
        # default, model doesn't exist, hidden field specified
        for deleted, name in ((True, "test-7664"), (False, "test-3191")):
            hm, created = HiddenModel.objects.get_or_create(name=name,
                                                            deleted=deleted)
            self.assertEquals(deleted, hm.deleted)
            self.assertTrue(created)
        
        # default, model doesn't exist, defaults specified
        for deleted, name in ((True, "test-1314"), (False, "3792")):
            hm, created = HiddenModel.objects.get_or_create(name=name,
                                                            defaults={"deleted": deleted})
            self.assertEquals(deleted, hm.deleted)
            self.assertTrue(created)
        
        # default, non-hidden model exists, no defaults or hidden field specified
        hm2, created = HiddenModel.objects.get_or_create(name="test-1144")
        self.assertEquals(hm2, hm1)
        self.assertFalse(created)
        
        # default, hidden model exists, no defaults or hidden field specified
        hm3 = HiddenModel.objects.create(name="test-6840", deleted=True)
        self.assertRaises(HiddenObjectError, HiddenModel.objects.get_or_create,
                          name="test-6840")
        
        # default, non-hiddend and hidden model exists, hidden field specified
        for name, deleted, old_hm in (("test-1144", False, hm1), 
                                      ("test-6840", True, hm3)):
            hm, created = HiddenModel.objects.get_or_create(name=name, deleted=deleted)
            self.assertEquals(hm, old_hm)
            self.assertFalse(created)
        
        for name, deleted in (("test-1144", True), ("test-6840", False)):
            hm, created = HiddenModel.objects.get_or_create(name=name, deleted=deleted)
            self.assertEquals(deleted, hm.deleted)
            self.assertTrue(created)
        
        # default, hidden and non-hidden model exists, defaults specified
        hm4 = HiddenModel.objects.create(name="test-1145", deleted=False)
        hm5 = HiddenModel.objects.create(name="test-6841", deleted=True)
        for name, deleted, old_hm in (("test-1145", False, hm4),
                                      ("test-6841", True, hm5)):
            for default in (True, False):
                hm, created = HiddenModel.objects.get_or_create(name=name, 
                                                                defaults={"deleted": deleted})
                self.assertEquals(hm, old_hm)
                self.assertEquals(deleted, hm.deleted)
                self.assertFalse(created)
        
        # default, hidden and non-hidden model exists, defaults and hidden 
        # field specified (should go with hidden params)
        for name in ("test-1144", "test-6840"):
            for default in (True, False):
                for deleted in (True, False):
                    hm, created = HiddenModel.objects.get_or_create(name=name,
                                                                    deleted=deleted,
                                                                    defaults={"deleted": default})
                    self.assertEquals(deleted, hm.deleted)
                    self.assertFalse(created)

        # custom, model doesn't exist, no defaults or hidden field specified
        chm1, created = CustomHiddenModel.objects.get_or_create(name="test-1144")
        self.assertFalse(chm1.disabled)
        self.assertTrue(created)
        
        # custom, model doesn't exist, hidden field specified
        for disabled, name in ((True, "test-7664"), (False, "test-3191")):
            chm, created = CustomHiddenModel.objects.get_or_create(
                            name=name, disabled=disabled)
            self.assertEquals(disabled, chm.disabled)
            self.assertTrue(created)
        
        # custom, model doesn't exist, defaults specified
        for disabled, name in ((True, "test-1314"), (False, "3792")):
            chm, created = CustomHiddenModel.objects.get_or_create(
                            name=name, defaults={"disabled": disabled})
            self.assertEquals(disabled, chm.disabled)
            self.assertTrue(created)
        
        # custom, non-hidden model exists, no defaults or hidden field specified
        chm2, created = CustomHiddenModel.objects.get_or_create(name="test-1144")
        self.assertEquals(chm2, chm1)
        self.assertFalse(created)
        
        # custom, hidden model exists, no defaults or hidden field specified
        chm3 = CustomHiddenModel.objects.create(name="test-6840", disabled=True)
        self.assertRaises(HiddenObjectError, CustomHiddenModel.objects.get_or_create,
                          name="test-6840")
        
        # custom, non-hiddend and hidden model exists, hidden field specified
        for name, disabled, old_chm in (("test-1144", False, chm1), 
                                      ("test-6840", True, chm3)):
            chm, created = CustomHiddenModel.objects.get_or_create(name=name, disabled=disabled)
            self.assertEquals(chm, old_chm)
            self.assertFalse(created)
        
        for name, disabled in (("test-1144", True), ("test-6840", False)):
            chm, created = CustomHiddenModel.objects.get_or_create(name=name, disabled=disabled)
            self.assertEquals(disabled, chm.disabled)
            self.assertTrue(created)
        
        # custom, hidden and non-hidden model exists, defaults specified
        chm4 = CustomHiddenModel.objects.create(name="test-1145", disabled=False)
        chm5 = CustomHiddenModel.objects.create(name="test-6841", disabled=True)
        for name, disabled, old_chm in (("test-1145", False, chm4),
                                      ("test-6841", True, chm5)):
            for default in (True, False):
                chm, created = CustomHiddenModel.objects.get_or_create(
                                name=name, defaults={"disabled": disabled})
                self.assertEquals(chm, old_chm)
                self.assertEquals(disabled, chm.disabled)
                self.assertFalse(created)
        
        # custom, hidden and non-hidden model exists, defaults and hidden 
        # field specified (should go with hidden params)
        for name in ("test-1144", "test-6840"):
            for default in (True, False):
                for disabled in (True, False):
                    chm, created = CustomHiddenModel.objects.get_or_create(
                                    name=name, disabled=disabled, defaults={"disabled": disabled})
                    self.assertEquals(disabled, chm.disabled)
                    self.assertFalse(created)
        
