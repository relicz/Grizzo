import discord
import random
import praw
import config
import pymysql
import asyncio

# sql database login
DB_IP = "a2plcpnl0761.prod.iad2.secureserver.net"
DB_USER = "grizzobot"
DB_PASSWORD = "7755929"
DB_NAME = "grizzobot"

reddit = praw.Reddit(client_id=config.REDDIT_ID, client_secret=config.REDDIT_SECRET,user_agent=config.USER_AGENT)

multireddit = 'GrizzoBot'
sub = reddit.subreddit(multireddit)


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
            rand_int = random.randint(1, int(roll_word[1]))  # Create a random integer based on the number of sides
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


def meme(ctx):
 post = sub.random()
 msg = "{}\nSource: {}".format(post.url, post.permalink)
 return msg

# define function for creating initial vote
def vote_start(question, choices_arr, emojis):
    print("Vote is being made...")

    # create embed
    vote_announce = discord.Embed(title="Time for a vote!")
    vote_announce.add_field(name="Question", value=question)  # add question field to embed

    # assign emojis to choices as a string and add to embed
    choices_string = ""
    i = 0
    while i < len(choices_arr):  # until all choices have been assigned
        choices_string += (emojis[i] + "" + choices_arr[i] + "\n")
        i += 1  # concatenate string that will be displayed in embed
    vote_announce.add_field(name="Choices", value=choices_string)

    # return embedded vote announcement
    return vote_announce


# define function for counting the votes
def tally_up(question, choices_arr, message):
    vote_string = "vote"  # singular or plural amount of votes?
    tie_flag = 0  # was there a tie?

    # tally dictionary
    tallies = {react.emoji: react.count for react in message.reactions}

    # check for a tie
    tallies_sorted = sorted(tallies.values(), reverse=True)  # sort highest numbers
    if tallies_sorted[0] != tallies_sorted[1]:  # if there is only one maximum, find the winner
        winner_count = max(tallies.values()) - 1  # assign winner count
        winner_emoji = max(tallies, key=tallies.get)  # assign winner emoji

        winner = choices_arr[list(tallies.keys()).index(winner_emoji)]  # assign winner using the index of winner_emoji

        # if more than one vote or no votes, change string to votes
        if winner_count > 1 or winner_count == 0:  #
            vote_string = "votes"

    else:  # there's a tie
        tie_flag = 1

    vote_winner = discord.Embed(title="We have a winner!")
    if tie_flag == 0:  # add field based on whether there's a tie or not
        vote_winner.add_field(name="And your winner is...", value=
        "__**" + winner + "**__ (" + winner_emoji + ")" +
        " with __**" + str(winner_count) + "**__ " + vote_string + "!")
    else:
        vote_winner.add_field(name="And your winner is...", value=
        "No one! It's a tie!")

    return vote_winner


# define function for pulling a certain amount of messages
def pull(ctx, message_list, num):  # context, channel, number of messages
    random.shuffle(message_list)  # randomize message list
    message_list = message_list[0:num]  # strip to number of inputted messages

    pulled_messages_string = ""  # string to place in embed
    for message in message_list:
        pulled_messages_string += message + "\n"  # concatenate messages

    # create embed
    pulled_messages_embed = discord.Embed(title=None)
    pulled_messages_embed.add_field(name="Messages:", value=pulled_messages_string)

    return pulled_messages_embed


def cmd_help(prefix):
    output = prefix
    output += "\nCommand: test ---- Arguments: None. ---- Function: Sends a test post."
    output += "\nCommand: roll or r ---- Arguments: XdY. X = # of dice, Y = # or sides per die. ---- Function: rolls " \
              "dice."
    output += "\nCommand: meme ---- Arguments: None. ---- Function: Posts a meme from Redit."
    output += "\nCommand: join or j ---- Arguments: None. ---- Function: Joins current voice channel of the author of" \
              " the command."
    output += "\nCommand: disconnect or d ---- Arguments: None. ---- Function: Disconnects from voice."
    output += "\nCommand: youtube, yt, or y ---- Arguments: Youtube search query. ---- Function: Plays audio to a" \
              " voice channel."
    output += "\nCommand: volume or v ---- Arguments: Number between 0 and 1. ---- Function: Changes bot audio volume."
    output += "\nCommand: censor or censorword ---- Arguments: a word to censor. ---- Function: censors a word from the chat channel."
    output += "\nCommand: uncensor or uncensorword ---- Arguments: a word to uncensor. ---- Function: removes word from the censor list."
    output += "\nCommand: censorlist or listcensors ---- Arguments: none. ---- Function: displays all censored words."
    output += "\nCommand: pins or pinnedlist ---- Arguments: none. ---- Function: shows all items pinned by gizzo."
    output += "\nTo pin messages in chat, add a 📌 reaction to the message ---- Function: pins message to view later"
    return output


def npc(ctx):
    strength = [random.randint(1, 6) for _ in range(4)]  # creates array with 4 random numbers
    strength.sort()  # sorts array
    a = strength[1] + strength[2] + strength[3]  # adds 3 highest values

    dex = [random.randint(1, 6) for _ in range(4)]
    dex.sort()
    b = dex[1] + dex[2] + dex[3]

    constitution = [random.randint(1, 6) for _ in range(4)]
    constitution.sort()
    c = constitution[1] + constitution[2] + constitution[3]

    intellligence = [random.randint(1, 6) for _ in range(4)]
    intellligence.sort()
    d = intellligence[1] + intellligence[2] + intellligence[3]

    wisdom = [random.randint(1, 6) for _ in range(4)]
    wisdom.sort()
    e = wisdom[1] + wisdom[2] + wisdom[3]

    charisma = [random.randint(1, 6) for _ in range(4)]
    wisdom.sort()
    f = charisma[1] + charisma[2] + charisma[3]

    output = "Strength: " + str(a) + "\nDexterity: " + str(b) + "\nConstitution: " + str(c) + "\nIntelligence: " + str(
        d) + "\nWisdom: " + str(e) + "\nCharisma: " + str(f)
    return output


# profanity filter
def censorword(phrase, message):
    phrase = phrase.lower()
    phrase += ""
    output = ""
    # sql
    # if has_value("words", "word", phrase):
    if phrase in DBGetCensors(message.channel.guild.id):
        output = ('{}, {} is already censored.'.format(message.author.mention, phrase))
    else:
        # sql
        # DBQuery("INSERT INTO words(words.serverID, word) VALUES('"+GUILD+"','"+phrase+"');")
        # arrayCensoredWords.append(phrase)
        output = ('{}, has added "{}" to the censoring list'.format(message.author.mention, phrase))
        print("Censoring: " + phrase)
        DBAddCensor(message.channel.guild.id, phrase)
        # sql
        # getWords()
    return output


# profanity filter
def uncensorword(phrase, message):
    phrase = phrase.lower()
    phrase += ""
    output = ""
    if phrase not in DBGetCensors(message.channel.guild.id):
        output = ('{}, {} is not censored.'.format(message.author.mention, phrase))
    else:
        DBRemoveCensors(message.channel.guild.id, phrase)
        output = ('{}, has uncensored "{}"'.format(message.author.mention, phrase))
        print("Uncensoring: " + phrase)

    return output


# profanity filter
def censorlist(message):
    print(message.channel.guild.id)
    arrayCensoredWordsDB = []
    arrayCensoredWordsDB = DBGetCensors(message.channel.guild.id)
    if not arrayCensoredWordsDB:
        return '{}, Nothing is censored yet.'.format(message.author.mention)
    arrayCensoredWordsDB.sort()
    censoredwords = ""
    for x in arrayCensoredWordsDB:
        if arrayCensoredWordsDB.index(x) > 0:
            censoredwords += " |  "
        censoredwords += str(x) + ""
    output = '{}, Here is the list of censored words: \n{}'.format(message.author.mention, censoredwords)
    return output


# display pins
async def listPins(ctx, index):
    pinMessageIDs = DBGetPins(ctx)
    output = ctx.author.mention + ", pinned messages: ```"
    x = 0
    for i in range(int(index), len(pinMessageIDs)):
        print(i)
        message = await ctx.channel.fetch_message(pinMessageIDs[i])
        print(message)
        if len(message.content) > 300:
            messageContent = message.content[0:299] + "... \nuse !pin " + str(i) + " to see full message"
        else:
            messageContent = message.content
        outputTest = output + "\n{}: {} {}, 📌 by {}:\n{}\n".format(str(i), message.author.name,
                                                                    message.created_at.strftime("%Y-%m-%d"),
                                                                    message.author.name, messageContent)
        if len(outputTest) < 1800:
            output = outputTest
        else:
            output += "\nShowing pin {} out of {}".format(str((i - 1)), str(len(pinMessageIDs) - 1))
            break
        x += 1
    x = 0
    return output + "\nTo jump to a specific pin use command: !pin <ID> \nTo view next batch of pins, use command !pins <ID to start at> ```"


# display pin
async def pin(ctx, id):
    pinMessageIDs = DBGetPins(ctx)
    message = await ctx.channel.fetch_message(pinMessageIDs[int(id)])
    embed = discord.Embed(colour=discord.Colour(0x4771c0), description=" ```{}```".format(message.content),
                          timestamp=message.created_at)
    embed.set_author(name="{}".format(message.author.name), url="https://discordapp.com",
                     icon_url="{}".format(message.author.avatar_url))
    embed.set_footer(text="Grizzo")
    embed.add_field(name=':pushpin:',
                    value="[Jump to pin]({})".format(message.jump_url))

    # await bot.say(content="Pinned by Grizzo", embed=embed)
    return embed


async def unpin(message, id):
    pinMessageIDs = DBGetPins(message)
    messageToUnpin = await message.channel.fetch_message(pinMessageIDs[int(id)])
    output = ""
    print(int(id))
    # sql
    # if has_value("words", "word", phrase):
    if int(id) > len(pinMessageIDs) or int(id) < 0:
        output = ('{}, {} out of index.'.format(message.author.mention, str(id)))
    else:
        # sql
        # DBQuery("DELETE FROM words WHERE word='"+badWord+"';")
        output = ('{}, has unpinned "{}"'.format(message.author.mention, messageToUnpin.content))
        DBUnpin(message, id)
        # sql
        # getWords()
    return output


def DBAddCensor(serverID, phrase):
    # Open database connection
    db = pymysql.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute(
        "INSERT ignore INTO server (server_alias_id) SELECT * FROM (SELECT '{}') AS tmp WHERE NOT EXISTS ( SELECT server_alias_id FROM server WHERE server_alias_id='{}') LIMIT 1;".format(
            serverID, serverID))
    cursor.execute(
        "INSERT ignore INTO word ( phrase) SELECT * FROM ( SELECT '{}') AS tmp WHERE NOT EXISTS ( SELECT phrase FROM word WHERE phrase='{}') LIMIT 1;".format(
            phrase, phrase))
    cursor.execute(
        "Insert ignore server_word (server_id, word_id) Select server_id , word_id from server CROSS Join word where server_alias_id = '{}' and phrase = '{}';".format(
            serverID, phrase))

    # disconnect from server
    db.commit()
    db.close()


def DBGetCensors(serverID):
    censoredWords = []
    # Open database connection
    db = pymysql.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute(
        "select phrase from server, word, server_word where server.server_id = server_word.server_id and word.word_id = server_word.word_id and server_alias_id='{}';".format(
            serverID))

    # Fetch a all rows using fetchall() method.
    # print(list(cursor))
    # censoredWords=list(cursor)
    # loads words from list to array
    censoredWords = []
    for i in list(cursor.fetchall()):
        stringTemp = i
        string = str(i)
        censoredWords.append(string[string.find("('") + 2: string.find("',)")])

    print(censoredWords)
    # disconnect from server
    db.commit()
    db.close()
    # print(censoredWords)
    return censoredWords


def DBRemoveCensors(serverID, phrase):
    censoredWords = []
    # Open database connection
    db = pymysql.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute(
        "DELETE from server_word where (SELECT server_id from server where server.server_alias_id='{}' ) = server_word.server_id and (SELECT word_id from word where word.phrase='{}' ) = server_word.word_id;".format(
            serverID, phrase))

    print(censoredWords)
    # disconnect from server
    db.commit()
    db.close()
    # print(censoredWords)
    return censoredWords


def DBAddPin(message):
    # Open database connection
    db = pymysql.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute(
        "INSERT ignore INTO server (server_alias_id) SELECT * FROM (SELECT '{}') AS tmp WHERE NOT EXISTS ( SELECT server_alias_id FROM server WHERE server_alias_id='{}') LIMIT 1;".format(
            message.channel.guild.id, message.channel.guild.id))
    cursor.execute(
        "INSERT INTO pins (server_id,message_id,date,channel_id,author,content) SELECT * FROM (SELECT (select server_id from server where server.server_alias_id='{}'),'{}',DATE_FORMAT('{}', '%Y/%c/%e'),'{}','{}','{}') AS tmp WHERE NOT EXISTS ( SELECT message_id FROM pins WHERE message_id='{};') LIMIT 1;".format(
            message.channel.guild.id, message.id, message.created_at.strftime("%Y-%m-%d"), message.channel.id,
            message.author, message.content, message.id))

    # disconnect from server
    db.commit()
    db.close()


def DBGetPins(message):
    pinsMessageIDs = []
    db = pymysql.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
    cursor = db.cursor()

    cursor.execute(
        "select message_id from server, pins where server.server_id = pins.server_id and server_alias_id='{}' and channel_id='{}';".format(
            message.channel.guild.id, message.channel.id))

    # message.channel.get_message('message_id')
    pinsMessageIDs = []
    for i in list(cursor.fetchall()):
        stringTemp = i
        string = str(i)
        pinsMessageIDs.append(string[string.find("('") + 2: string.find("',)")])

    print(pinsMessageIDs)

    db.commit()
    db.close()
    return pinsMessageIDs


def DBUnpin(message, ID):
    serverID = message.channel.guild.id
    channelID = message.channel.id
    messageID = DBGetPins(message)[int(ID)]

    # Open database connection
    db = pymysql.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute(
        "DELETE from pins where (SELECT server_id from server where server.server_alias_id='{}' ) = pins.server_id and message_id = '{}' and channel_id='{}';".format(
            serverID, messageID, channelID))

    # disconnect from server
    db.commit()
    db.close()
    return "done"
