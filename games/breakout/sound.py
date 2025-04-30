import pygame

from pathlib import Path
from .utils import singleton


@singleton
class SoundManager:
	def __init__(self) -> None:
		pygame.mixer.init()
		self.sfx_volume: float = 1.0
		self.sounds: dict[str, pygame.mixer.Sound] = {}
		self._load_sounds()

	def _load_sounds(self) -> None:
		path: Path = Path(__file__).parent / "assets"
		wav_files = path.glob("*.wav")

		for sound_path in wav_files:
			sound_name: str = sound_path.stem  # filename without suffix
			sound: pygame.mixer.Sound = pygame.mixer.Sound(str(sound_path))
			sound.set_volume(self.sfx_volume)
			self.sounds[sound_name] = sound

	def play(self, name: str) -> None:
		sound: pygame.mixer.Sound | None = self.sounds.get(name)
		if sound:
			sound.play()
		else:
			print(f"Warning: No sound loaded with name '{name}'.")

	def set_volume(self, volume: float) -> None:
		self.sfx_volume = max(0.0, min(1.0, volume))
		for sound in self.sounds.values():
			sound.set_volume(self.sfx_volume)
