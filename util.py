import discord
import random
import praw
import config

# reddit = praw.Reddit(client_id=config.REDDIT_ID, client_secret=config.REDDIT_SECRET,user_agent=config.USER_AGENT)

# multireddit = 'memes'
# sub = reddit.subreddit(multireddit)


def dice_roller(ctx, arg):
    # contents = arg.content[len("!r"):]
    contents = arg.lower()  # make the contents of the argument lowercase
    # word_list = contents.split(" ")

    output = ctx.author.mention  # Start output with user name
    output += " `" + contents.replace(" ", "") + "` "  # Add the arguments to the output
    summation = 0  # Establish a sum  counter track the sum of the rolls
    # for word in word_list:
    roll_word = contents.split('d')  # Split argument into two parts at the d
    if len(roll_word) > 1:  # If there are more than one components
        output += "("
        for x in range(0, int(roll_word[0])):  # Loop it based on the number of dice
            rand_int = random.randint(1,  int(roll_word[1]))  # Create a random integer based on the number of sides
            output += str(rand_int)  # Add the roll to the output addition section
            if x is not int(roll_word[0]) - 1:  # Add a + if we are not at the end of the loop
                output += ' + '
            summation += rand_int  # Add the new int to the total sum
        output += ") "
    else:
        if roll_word[0].isdigit() is True:
            output = output.strip()
            output += ' + ' + str(roll_word[0])
            summation += int(roll_word[0])
    output += " = " + str(summation)  # Add the sum to the output string
    return output


def test(ctx):
    output = "test1234"
    return output

#def meme(ctx):
    #post = sub.random()
   # msg = "{}\nSource: {}".format(post.url, post.permalink)
   # return msg


def cmd_help(ctx):
    output = "Command: test ---- Arguments: None. ---- Function: Sends a test post"
    output += "\nCommand: roll ---- Arguments: XdY. X = # of dice, Y = # or sides per die. ---- Function: rolls dice"
    output += "\nCommand: meme ---- Arguments: None. ---- Function: Posts a meme from Redit"
    return output
