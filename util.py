import discord
import random
import praw
import config

reddit = praw.Reddit(client_id=config.REDDIT_ID, client_secret=config.REDDIT_SECRET,user_agent=config.USER_AGENT)


ROLL_COMMAND = "!r"
TEST_COMMAND = "!test1234"
MEME_COMMAND = "!meme"

multireddit = 'memes+dankmemes+animemes+wholesomeanimemes'
sub = reddit.subreddit(multireddit)

def dice_roller(message):
    contents = message.content[len("!r"):]
    contents = contents.lower().strip()
    word_list = contents.split(" ")

    output = message.author.mention
    output += " `" + contents.replace(" ", "") + "` "
    summation = 0
    for word in word_list:
        roll_word = word.split('d')
        if len(roll_word) > 1:
            output += "("
            for x in range(0,int(roll_word[0])):
                rand_int = random.randint(1,  int(roll_word[1]))
                output += str(rand_int)
                if x is not int(roll_word[0]) - 1:
                    output += ' + '
                summation += rand_int
            output += ") "
        else:
            if roll_word[0].isdigit() is True:
                output = output.strip()
                output += ' + ' + str(roll_word[0])
                summation += int(roll_word[0])
    output += " = " + str(summation)
    return output

def test(message):
    output = "test1234"
    return output

def meme(message):
    post = sub.random()
    msg = "{}\nSource: {}".format(post.url, post.permalink)
    return msg
