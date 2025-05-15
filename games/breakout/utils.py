import pygame

from PIL import Image, ImageFilter
from typing import Union, Callable, TypeVar, Any
from functools import wraps
from random import randint

T = TypeVar("T")


def singleton(cls: Callable[..., T]) -> Callable[..., T]:
	instances: dict[Callable[..., T], T] = {}

	@wraps(cls)
	def get_instance(*args: Any, **kwargs: Any) -> T:
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]

	return get_instance


def no_null(a: float):
	if int(a) == 0:
		return 1 if a > 0 else -1

	return a


def limit(a: Union[int, float], left: Union[int, float], right: Union[int, float]) -> Union[int, float]:
	return min(right, max(left, a))


def choose(options: list[tuple[Any, int]]) -> Any:
	all = sum([i[1] for i in options])
	rand = randint(1, all)
	for opt in options:
		rand -= opt[1]
		if rand <= 0:
			return opt[0]


def glow(surface: pygame.Surface, falloff: float = 15, quality: float = 0.5) -> pygame.Surface:
	"""
	Returns surface with glowing. It should be later blitted with BLEND_RGB_ADD.

	Args:
		surface: A pygame.Surface with SRC_ALPHA flag where the solid shapes
				 (e.g., a circle) have already been drawn.
		falloff: The radius of the Gaussian blur, controlling how wide and soft
				 the glow effect spreads.
		quality: A scaling factor for the resolution of the intermediate surface,
				 affecting performance and quality of the glow effect.
	"""
	resolution: tuple[int, int] = (int(surface.get_width() * quality), int(surface.get_height() * quality))

	resized = pygame.transform.scale(surface, resolution)

	img_str = pygame.image.tostring(resized, "RGBA", False)
	img = Image.frombytes("RGBA", resolution, img_str)

	img = img.filter(ImageFilter.GaussianBlur(falloff))

	pil_bytes = img.tobytes()
	py_img = pygame.image.fromstring(pil_bytes, resolution, "RGBA")

	final = pygame.transform.scale(py_img, (surface.get_width(), surface.get_height()))

	return final
