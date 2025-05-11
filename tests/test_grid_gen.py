from unittest import TestCase

from src.grid_gen import grid_is_completable
from src.models.club import Club


class Test(TestCase):
    def test_is_valid_grid(self):
        grid_solution = [
            [
                [Club(id=1)],
                [Club(id=2)],
                [Club(id=3)]
            ],
            [
                [Club(id=4)],
                [Club(id=5)],
                [Club(id=6)]
            ],
            [
                [Club(id=7)],
                [Club(id=8)],
                [Club(id=9)]
            ],
        ]

        result = grid_is_completable(grid_solution)

        self.assertTrue(result)

    def test_is_valid_grid_2(self):
        grid_solution = [
            [
                [Club(id=1), Club(id=2)],
                [Club(id=2), Club(id=1)],
                [Club(id=3)]
            ],
            [
                [Club(id=4)],
                [Club(id=5)],
                [Club(id=6)]
            ],
            [
                [Club(id=7)],
                [Club(id=8)],
                [Club(id=9)]
            ],
        ]

        result = grid_is_completable(grid_solution)

        self.assertTrue(result)

    def test_is_invalid_grid(self):
        grid_solution = [
            [
                [Club(id=1)],
                [Club(id=1)],
                [Club(id=3)]
            ],
            [
                [Club(id=4)],
                [Club(id=5)],
                [Club(id=6)]
            ],
            [
                [Club(id=7)],
                [Club(id=8)],
                [Club(id=9)]
            ],
        ]

        result = grid_is_completable(grid_solution)

        self.assertFalse(result)

    def test_is_invalid_grid_2(self):
        grid_solution = [
            [
                [],
                [Club(id=2)],
                [Club(id=3)]
            ],
            [
                [Club(id=4)],
                [Club(id=5)],
                [Club(id=6)]
            ],
            [
                [Club(id=7)],
                [Club(id=8)],
                [Club(id=9)]
            ],
        ]

        result = grid_is_completable(grid_solution)

        self.assertFalse(result)

    def test_is_invalid_grid_3(self):
        grid_solution = [
            [
                [Club(id=1), Club(id=2), Club(id=3), Club(id=4), Club(id=5), Club(id=6), Club(id=7), Club(id=8)],
                [Club(id=1), Club(id=2), Club(id=3), Club(id=4), Club(id=5), Club(id=6), Club(id=7), Club(id=8)],
                [Club(id=1), Club(id=2), Club(id=3), Club(id=4), Club(id=5), Club(id=6), Club(id=7), Club(id=8)],
            ],
            [
                [Club(id=1), Club(id=2), Club(id=3), Club(id=4), Club(id=5), Club(id=6), Club(id=7), Club(id=8)],
                [Club(id=1), Club(id=2), Club(id=3), Club(id=4), Club(id=5), Club(id=6), Club(id=7), Club(id=8)],
                [Club(id=1), Club(id=2), Club(id=3), Club(id=4), Club(id=5), Club(id=6), Club(id=7), Club(id=8)],
            ],
            [
                [Club(id=1), Club(id=2), Club(id=3), Club(id=4), Club(id=5), Club(id=6), Club(id=7), Club(id=8)],
                [Club(id=1), Club(id=2), Club(id=3), Club(id=4), Club(id=5), Club(id=6), Club(id=7), Club(id=8)],
                [Club(id=1), Club(id=2), Club(id=3), Club(id=4), Club(id=5), Club(id=6), Club(id=7), Club(id=8)],
            ],
        ]

        result = grid_is_completable(grid_solution)

        self.assertFalse(result)
