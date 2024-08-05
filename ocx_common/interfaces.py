#  Copyright (c) 2023. OCX Consortium https://3docx.org. See the LICENSE
"""Interfaces module."""

# System imports
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import uuid4
from typing import Dict, Iterator
import threading


class _Singleton:
    """A threadsafe singleton class.
    https://medium.com/gitconnected/design-patterns-in-python-singleton-pattern-f76dc26281f8
    """

    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        """
        Initializes a new instance with a randomly generated UUID value.

        Args:
            self: The instance itself.

        Returns:
            None
        """
        self.value = uuid4()

    @classmethod
    def get_instance(cls):
        """
        Returns the instance of the class. If the instance does not exist, it creates one.

        Returns:
            The instance of the class.

        Examples:
            instance = ClassName.get_instance()
        """
        with cls.__lock:
            if not cls.__instance:
                cls.__instance = cls()
        return cls.__instance


class IModuleDeclaration(ABC):
    """Abstract module import declaration Interface"""

    @staticmethod
    @abstractmethod
    def get_declaration() -> str:
        """Abstract Method: Return the module declaration string."""
        pass


class IObserver(ABC):
    """The observer interface"""

    @abstractmethod
    def update(self, event: str, payload: Dict):
        """Interface update method"""


class IObservable(ABC):
    """Interface. The observable object."""

    @abstractmethod
    def subscribe(self, observer: IObserver):
        """subscription"""

    @abstractmethod
    def unsubscribe(self, observer: IObserver):
        """unsubscribe"""

    @abstractmethod
    def update(self, event: str, message: Dict):
        """
        update method.

        Args:
            event: The event type
            message: The event message
        """


class IParser(ABC):
    """Abstract IParser interface."""

    @abstractmethod
    def parse(self, model: str) -> dataclass:
        """
        Abstract method for parsing a data model,

        Args:
            model: the data model source

        Returns:
            the root dataclass of the parsed data model.
        """
        pass

    @abstractmethod
    def iterator(self, model) -> Iterator:
        """
        Abstract method for iterating a data model.

        Args:
            model: the data model to iterate on.
        Returns:
             An iterator
        """
        pass


class ISerializer(ABC):
    """OcxSerializer interface"""

    def __init__(self, model: dataclass):
        self.model = model

    @abstractmethod
    def serialize_to_file(self, to_file: str) -> bool:
        """Abstract XML serialize to file method"""
        pass

    @abstractmethod
    def serialize_to_string(self) -> str:
        """Abstract XML serialize to string method"""
        pass
