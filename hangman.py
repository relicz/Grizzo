import os
import discord
import asyncio
import logging
import random

class Hangman:
    chosen_word = ""
    guessed_letters = ""
    remaining_guesses = 6
    words = {
        1: 'grizzo',
        2: 'beekeeper',
        3: 'blitz',
        4: 'spritz',
        5: 'abyss',
        6: 'banjo'}
    has_ended = False
    has_won = False

    def start_game(self):
        random.seed()
        key = random.randint(1, len(self.words))
        self.chosen_word = self.words[key]
        new_string = ""
        for i in range(0, len(self.chosen_word)):
            new_string += "?"
        self.guessed_letters = new_string

    def game_status(self):
        # return a string containing the current status and if
        # the player has won or not
        message = ""

        if not self.has_ended:
            # print each letter followed by a space
            letters = ""
            for i in range(0, len(self.guessed_letters)):
                letters += self.guessed_letters[i] + ' '
            message = '{} guesses left \n'.format(self.remaining_guesses)
            message += letters

        if self.has_ended and self.has_won:
            message += '\n You won! You correctly guessed ' + '`{}`'.format(self.chosen_word)
        elif self.has_ended and not self.has_won:
            message += '\n You lost! The correct word was ' + '`{}`'.format(self.chosen_word)

        return message

    def guess(self, message):
        args = message.split(' ')
        guess = ""
        contains_guess = False

        if len(args) > 1:
            guess = args[1]

        for i in range(0, len(self.chosen_word)):
            if guess[0] == self.chosen_word[i]:
                self.guessed_letters = self.guessed_letters[:i] + guess[0] + self.guessed_letters[i + 1:]
                contains_guess = True
        if not contains_guess:
            self.remaining_guesses -= 1

        # check for letters that haven't been guessed
        unguessed_letters = False
        for letter in self.guessed_letters:
            if letter == '?':
                unguessed_letters = True

        # player has won the game
        if not unguessed_letters:
            self.has_ended = True
            self.has_won = True

        # no more guesses, so the player has lost
        if self.remaining_guesses < 0:
            self.has_ended = True
            self.has_won = False
