from abc import ABC, abstractmethod
from typing import List
from core.parser import TranslationTask

class BaseTranslator(ABC):
    @abstractmethod
    def translate_tasks(self, tasks: List[TranslationTask]) -> None:
        pass
