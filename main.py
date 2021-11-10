# *********************************************************************************
# Lottery simulation to calculate the probabilities behind players matching N balls
# *********************************************************************************

import random as rand
import logging

log = logging.getLogger("lottery sim")
logging.basicConfig(level=logging.INFO)


def full_range(start, stop): return range(start, stop + 1)


class Rules:
    """
    defines the lottery setup
    """
    def __init__(self, min_number=1, max_number=49, required_selection_count=6):
        self.min_number = min_number
        self.max_number = max_number
        self.required_selection_count = required_selection_count

    def is_valid(self):
        return (self.min_number < self.required_selection_count < self.max_number) & self.min_number >= 1


class Lottery:
    """
    Handles the lottery draw
    """
    def __init__(self, rules):
        if not rules.is_valid():
            ValueError("incorrect parameters for lottery!")
        self.balls = []
        self.draw = []
        self.rules = rules

    def __setup(self):
        self.balls = [Ball(i) for i in full_range(self.rules.min_number, self.rules.max_number)]

    def __get_random_ball(self):
        rand.shuffle(self.balls)
        return self.balls.pop()

    def draw_numbers(self):
        self.__setup()
        for _n in full_range(1, self.rules.required_selection_count):
            self.draw.append(self.__get_random_ball())

    def __is_ball_drawn(self, ball):
        if not self.draw:
            ValueError("Draw has not happened yet!")
            return False
        else:
            return ball in self.balls

    def check_numbers(self, num_list):
        """
        num_list = list of numbers selected by a player
        this method checks the players numbers against the lotto draw numbers
        """
        count = 0
        for n in num_list:
            count += 1 if Ball(n) in self.draw else 0
        return count

    def get_drawn_numbers(self):
        return sorted([ball.number for ball in self.draw])


class Ball:
    def __init__(self, number):
        self.number = number

    def __eq__(self, other):
        return self.number == other.number


class Player:
    def __init__(self, rules):
        choice = [n for n in full_range(rules.min_number, rules.max_number)]
        rand.shuffle(choice)
        self.selection = []
        for _n in full_range(1, rules.required_selection_count):
            self.selection.append(choice.pop())


class Result:
    """
    The simulation results are recorded in this class
    """
    def __init__(self, total):
        self.total = total
        self.results = {}
        self.lottery_numbers = []

    def log_player_matches(self, ball_count):
        """
        ball_count is the number of matches a player gets
        This method when called just records that a player
        received a N matches in their selection
        """
        self.results[ball_count] = self.results.get(ball_count, 0) + 1

    def print_results(self):
        """
        Summary of the simulation output
        """
        log.info("total players = {:,}".format(self.total))
        log.info("numbers = {}".format(self.lottery_numbers))
        sorted_dict = {k: v for k, v in sorted(self.results.items())}
        for r in sorted_dict:
            percent = round(100 * (self.results[r] / self.total), 2)
            row = "Ball count = {} Players Matched = {:,} Percentage = {}%".format(r, self.results[r], percent)
            log.info(row)


class Simulation:
    """
    Run a lottery for N number of players
    """
    def __init__(self, players, rules):
        self.player_count = players
        self.rules = rules

    def start(self):
        result = Result(self.player_count)
        lottery = Lottery(self.rules)
        lottery.draw_numbers()
        for _n in full_range(1, self.player_count):
            player = Player(self.rules)
            count = lottery.check_numbers(player.selection)
            result.log_player_matches(count)
        result.lottery_numbers = lottery.get_drawn_numbers()
        return result


def process():
    """
    Main method to execute
    """
    rules = Rules(min_number=1, max_number=49, required_selection_count=6)
    simulation = Simulation(players=10000, rules=rules)
    result = simulation.start()
    result.print_results()


if __name__ == '__main__':
    process()
