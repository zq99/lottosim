
# Lottery Simulation

Dr Marcus du Sautoy gave a presentation at the 2014 IFTA Conference in London,
organized by the UK Society of Technical Analysts.

During the talk, he asked the audience to participate in an exercise
demonstrating the probabilities behind the UK National Lottery.

This project is a Python simulation of that exercise.

## Approach

The intention is not to begin with a known probability distribution or
mathematical formula. Instead, the program models the process performed by the
audience:

1. Draw six lottery balls without replacement.
2. Generate a six-number selection for each player.
3. Compare each selection with the lottery draw.
4. Record how many players matched each number of balls.

The `Rules`, `Lottery`, `Ball`, `Player`, `Result`, and `Simulation` classes
reflect the different parts of that process.

The number of matches follows a hypergeometric distribution
because both the lottery draw and each player's selection sample from a finite
set without replacement. The simulation estimates that distribution empirically
by repeating the selection process many times.

## Running the simulation

```bash
python lottery_sim.py
```

The program prints the lottery numbers and the number and percentage of players
who matched each observed number of balls.

## Background

The presentation can be watched [on YouTube](https://www.youtube.com/watch?v=QpyOKEHhTeI).

> This was originally written as an early Python learning project. It has since
> received minor maintenance, type annotations, and bug fixes while retaining
> its original design.








