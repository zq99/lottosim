# *************************************************************************************
# UK Lottery simulation to calculate the probabilities behind players matching N balls
# *************************************************************************************

from __future__ import annotations

import logging
import random as rand


log = logging.getLogger("lottery sim")
logging.basicConfig(level=logging.INFO)


def full_range(start: int, stop: int) -> range:
    """Return a range that includes both its start and stop values."""
    return range(start, stop + 1)


class Rules:
    """Define the lottery setup."""

    def __init__(
        self,
        min_number: int = 1,
        max_number: int = 49,
        required_selection_count: int = 6,
    ) -> None:
        self.min_number = min_number
        self.max_number = max_number
        self.required_selection_count = required_selection_count

    def get_range(self) -> int:
        return abs(self.max_number - self.min_number) + 1

    def is_valid(self) -> bool:
        return (
                self.max_number > self.min_number >= 1
                and 0 < self.required_selection_count <= self.get_range()
        )


class Lottery:
    """Handle the lottery draw."""

    def __init__(self, rules: Rules) -> None:
        if not rules.is_valid():
            raise ValueError("Incorrect parameters for lottery")

        self.balls: list[Ball] = []
        self.draw: list[Ball] = []
        self.rules = rules

    def __setup(self) -> None:
        self.balls = [
            Ball(number)
            for number in full_range(
                self.rules.min_number,
                self.rules.max_number,
            )
        ]
        rand.shuffle(self.balls)
        self.draw = []

    def __get_random_ball(self) -> Ball:
        return self.balls.pop()

    def draw_numbers(self) -> None:
        self.__setup()
        for _ in full_range(1, self.rules.required_selection_count):
            self.draw.append(self.__get_random_ball())

    def __is_ball_drawn(self, ball: Ball) -> bool:
        if not self.draw:
            raise ValueError("Draw has not happened yet")

        return ball in self.draw

    def check_numbers(self, num_list: list[int]) -> int:
        """Return how many of a player's selected numbers match the draw."""
        matched_count = 0
        for number in num_list:
            matched_count += 1 if self.__is_ball_drawn(Ball(number)) else 0
        return matched_count

    def get_drawn_numbers(self) -> list[int]:
        return sorted(ball.number for ball in self.draw)


class Ball:
    def __init__(self, number: int) -> None:
        self.number = number

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ball):
            return NotImplemented
        return self.number == other.number


class Player:
    def __init__(self, rules: Rules) -> None:
        choices = list(full_range(rules.min_number, rules.max_number))
        rand.shuffle(choices)

        self.selection: list[int] = []
        for _ in full_range(1, rules.required_selection_count):
            self.selection.append(choices.pop())


class Result:
    """Record and report the simulation results."""

    def __init__(self, total: int) -> None:
        self.total = total
        self.results: dict[int, int] = {}
        self.lottery_numbers: list[int] = []

    def log_player_matches(self, ball_count: int) -> None:
        """Record that a player matched ``ball_count`` numbers."""
        self.results[ball_count] = self.results.get(ball_count, 0) + 1

    def print_results(self) -> None:
        """Log a summary of the simulation output."""
        log.info("Total players = %s", f"{self.total:,}")
        log.info("Lottery numbers = %s", self.lottery_numbers)

        for matched_count, player_count in sorted(self.results.items()):
            percent = round(100 * player_count / self.total, 2)
            log.info(
                "Matched count = %d | Players = %s | Percentage = %.2f%%",
                matched_count,
                f"{player_count:,}",
                percent,
            )


class Simulation:
    """Run a lottery simulation for a specified number of players."""

    def __init__(self, players: int, rules: Rules) -> None:
        if players <= 0:
            raise ValueError("Player count must be greater than zero")

        self.player_count = players
        self.rules = rules

    def start(self) -> Result:
        result = Result(self.player_count)
        lottery = Lottery(self.rules)
        lottery.draw_numbers()

        for _ in full_range(1, self.player_count):
            player = Player(lottery.rules)
            matched_count = lottery.check_numbers(player.selection)
            result.log_player_matches(matched_count)

        result.lottery_numbers = lottery.get_drawn_numbers()
        return result


def run_simulation() -> None:
    """Run the simulation and print its results."""
    rules = Rules(min_number=1, max_number=49, required_selection_count=6)
    simulation = Simulation(players=10_000, rules=rules)
    result = simulation.start()
    result.print_results()


if __name__ == "__main__":
    run_simulation()
