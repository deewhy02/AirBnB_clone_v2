#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import models
from os import getenv

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if kwargs.get("created_at"):
                kwargs["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.created_at = datetime.now()
            if kwargs.get("created_at"):
                kwargs["updated_at"] = datetime.strptime(
                    kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.updated_at = datetime.now()
            for key, val in kwargs.items():
                if "__class__" not in key:
                    setattr(self, key, val)
            if not self.id:
                self.id = str(uuid.uuid4())
        # if not kwargs:
        #     self.id = str(uuid.uuid4())
        #     self.created_at = datetime.now()
        #     self.updated_at = datetime.now()
        # else:
        #     if kwargs:
        #         for key, value in kwargs.items():
        #             if key == "__class__":
        #                 pass
        #             elif key == "updated_at" or key == "created_at":
        #                 setattr(self, key, datetime.strptime(
        #                         value, "%Y-%m-%dT%H:%M:%S.%f"))
        #             else:
        #                 setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))
        # cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        # return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        cp_dct = dict(self.__dict__)
        cp_dct['__class__'] = self.__class__.__name__
        cp_dct['updated_at'] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        cp_dct['created_at'] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        if hasattr(self, "_sa_instance_state"):
            del cp_dct["_sa_instance_state"]
        return (cp_dct)
         
        # dictionary = {}
        # dictionary.update(self.__dict__)
        # dictionary.update({'__class__':
        #                   (str(type(self)).split('.')[-1]).split('\'')[0]})
        # dictionary['created_at'] = self.created_at.isoformat()
        # dictionary['updated_at'] = self.updated_at.isoformat()
        # if hasattr(self, "_sa_instance_state"):
        #     dictionary.pop("_sa_instance_state", None)
        # return dictionary

    def delete(self):
        """delete the current instance from the storage """
        models.storage.delete(self)
