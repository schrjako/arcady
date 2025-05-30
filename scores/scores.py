import json
from pathlib import Path
from typing import Union


class Scores:
	def __init__(self, filename: str = ".SCORES") -> None:
		self._file: Path = Path(__file__).parent / filename
		self._game: str = ""

	def set_game(self, game: str) -> None:
		self._game = game

	def write(self, score: Union[int, float]) -> None:
		data = {}
		if self._file.exists():
			with open(self._file) as fin:
				data = json.load(fin)
		data.setdefault(self._game, []).append(score)
		with open(self._file, "w") as fout:
			json.dump(data, fout)

	def get(self) -> list[Union[int, float]]:
		if not self._file.exists():
			return []
		with open(self._file) as fin:
			data = json.load(fin)
		return data.get(self._game, [])
