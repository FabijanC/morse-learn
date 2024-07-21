"""Definitions of all game modes"""

from abc import ABC
import random
from typing import Dict, List, Tuple, Type

from musicalbeeps import Player

import data


def _normalize_text(text: str) -> str:
    """Normalize the text for comparison."""
    return text.strip().lower()


class GameMode(ABC):
    """Abstraction of game mode"""

    def __init__(self, prompt_length: int, prompt_to_response: Dict[str, str]):
        self.prompt_length = prompt_length

        # data
        self.__prompt_to_response = prompt_to_response
        self.__prompts = list(prompt_to_response.keys())

        # stats
        self.generated_questions_count = 0
        self.attempts_count = 0
        self.correct_attempts_count = 0

    @classmethod
    def get_selector(cls):
        """Return the CLI selector."""
        raise NotImplementedError

    def get_startup_message(self) -> str:
        """Return the message to be displayed on startup."""
        raise NotImplementedError

    def display_prompt(self, prompt_tokens: List[str]) -> str:
        """Return displayable format of prompt."""
        raise NotImplementedError

    def generate_next(self) -> Tuple[str, List[str]]:
        """Generate a prompt and the expected answer."""
        random_keys = []
        correct = []

        while len(random_keys) < self.prompt_length:
            random_key = random.choice(self.__prompts)
            if random_key in random_keys:
                continue
            random_keys.append(random_key)
            correct.append(_normalize_text(self.__prompt_to_response[random_key]))

        self.generated_questions_count += 1

        return self.display_prompt(random_keys), correct

    def get_normalized_input_tokens(self) -> List[str]:
        """Receive input from the user and return a list of normalized tokens."""
        raise NotImplementedError


class LetterToCodeMode(GameMode):
    """
    Game mode where the user is prompted with letter and needs to
    provide the corresponding Morse code.
    """

    def __init__(self, prompt_length: int):
        super().__init__(prompt_length, data.letter2code)

    @classmethod
    def get_selector(cls):
        return "letter-to-code"

    def get_startup_message(self) -> str:
        msg = "Respond with dots and dashes."
        if self.prompt_length > 1:
            msg += " Separate the codes with spaces."
        return msg

    def display_prompt(self, prompt_tokens: List[str]):
        return "".join(prompt_tokens)

    def get_normalized_input_tokens(self) -> List[str]:
        return [part for part in input().split()]


class CodeToLetterMode(GameMode):
    """
    Game mode where the user is prompted with Morse code and needs to
    provide the corresponding letters.
    """

    def __init__(self, prompt_length: int):
        super().__init__(
            prompt_length, {code: letter for letter, code in data.letter2code.items()}
        )

    @classmethod
    def get_selector(cls):
        return "code-to-letter"

    def get_startup_message(self) -> str:
        msg = "Respond with letters. Case is ignored."
        if self.prompt_length > 1:
            msg += " You may optionally separate the letters with spaces."
        return msg

    def display_prompt(self, prompt_tokens: List[str]):
        return " ".join(prompt_tokens)

    def get_normalized_input_tokens(self) -> List[str]:
        return [_normalize_text(part) for part in input().split()]


class AudioToLetterMode(CodeToLetterMode):
    """
    Game mode where the user listens to audio, recognize the encoded letters, and type them.
    """

    DEFAULT_NOTE = "A"
    DURATION_MAP = {
        ".": 0.2,
        "-": 0.5,
    }
    SYMBOL_PAUSE_DURATION = 0.2
    LETTER_PAUSE_DURATION = 0.5

    def __init__(self, prompt_length: int):
        super().__init__(prompt_length)
        self.player = Player(volume=0.5, mute_output=True)

    @classmethod
    def get_selector(cls):
        return "audio-to-letter"

    def display_prompt(self, prompt_tokens: List[str]):
        for token in prompt_tokens:
            for morse_symbol in token:
                duration = self.DURATION_MAP[morse_symbol]
                self.player.play_note(self.DEFAULT_NOTE, duration=duration)
                self.player.play_note("pause", duration=self.SYMBOL_PAUSE_DURATION)
            self.player.play_note("pause", duration=self.LETTER_PAUSE_DURATION)

        return "(Press Enter to replay)"


SELECTOR_TO_MODE: Dict[str, Type[GameMode]] = {
    mode.get_selector(): mode
    for mode in [LetterToCodeMode, CodeToLetterMode, AudioToLetterMode]
}
