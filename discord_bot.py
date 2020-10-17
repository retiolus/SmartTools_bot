import discord
from discord.ext import commands
import os
import os.path
import random
from moviepy.editor import *
from moviepy.video.fx.resize import resize
import ffmpy
import wikipedia
from translate import Translator
from langdetect import detect
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import asyncio
import csv
from datetime import datetime, timedelta, date
import smtplib


intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = 't/', intents = intents)

client.remove_command('help')

TOKEN = '<TOKEN>'

glob_path = '</bot/path>'

def make_list(lst):
    return ' '.join(lst).split()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='Making your day easier'))

@client.event
async def on_message(message):

    await client.process_commands(message)

    if message.author == client.user:
        return

    guild = message.guild.id
    channels = message.guild.channels
    roles = message.guild.roles

    logs_status = glob_path + str(guild) + '/logs.txt'

    if not os.path.isfile(logs_status):
        return

    else:
        with open(logs_status, 'r') as text_file:
            for line in text_file:
                log_channel_id = client.get_channel(int(line))
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                await log_channel_id.send("[" + now + "] [" + str(message.channel.mention) + '] [' + str(message.author) + '] : Sent --> ' + message.content + '')
            return

@client.event
async def on_message_delete(message):

    await client.process_commands(message)

    if message.author == client.user:
        return

    guild = message.guild.id
    channels = message.guild.channels
    roles = message.guild.roles

    logs_status = glob_path + str(guild) + '/logs.txt'

    if not os.path.isfile(logs_status):
        return

    else:
        with open(logs_status, 'r') as text_file:
            for line in text_file:
                log_channel_id = client.get_channel(int(line))
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                await log_channel_id.send("[" + now + "] [" + str(message.channel.mention) + '] [' + str(message.author) + '] : Removed --> ' + message.content + '')
            return

@client.event
async def on_message_edit(before, after):

    await client.process_commands(after)

    if after.author == client.user:
        return

    guild = after.guild.id
    channels = after.guild.channels
    roles = after.guild.roles

    logs_status = glob_path + str(guild) + '/logs.txt'

    if not os.path.isfile(logs_status):
        return

    else:
        with open(logs_status, 'r') as text_file:
            for line in text_file:
                log_channel_id = client.get_channel(int(line))
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                await log_channel_id.send("[" + now + "] [" + str(after.channel.mention) + '] [' + str(after.author.mention) + '] : Edited --> ' + before.content + ' --> ' + after.content)
            return

@client.command()
async def mp3(ctx):
    if ctx.message.attachments:
        files = []
        for i in ctx.message.attachments:
            files.append(i)
            await i.save(glob_path + i.filename)

        video = VideoFileClip(i.filename)
        video.audio.write_audiofile(i.filename + '.mp3')
        await ctx.message.channel.send(file=discord.File(glob_path + i.filename+'.mp3', filename=str(i.filename+'.mp3')))
        os.remove(glob_path + i.filename+'.mp3')

    os.remove(glob_path + i.filename)
    await ctx.message.delete(delay=None)

@client.command()
async def gif(ctx):
    if ctx.message.attachments:
        files = []
        for i in ctx.message.attachments:
            files.append(i)
            await i.save(glob_path + i.filename)

        video = VideoFileClip(i.filename).resize(width=350)
        video = video.subclip(0,3)
        video.write_gif(i.filename + '.gif', fps=6)
        await ctx.message.channel.send(file=discord.File(glob_path + i.filename+'.gif', filename=str(i.filename+'.gif')))
        os.remove(glob_path + i.filename+'.gif')

    os.remove(glob_path + i.filename)
    await ctx.message.delete(delay=None)

@client.command()
async def wiki(ctx, arg):
    print(arg)
    summary = wikipedia.summary(arg)
    summary_url = wikipedia.page(arg).url
    await ctx.message.channel.send(summary + '\n\n<' + summary_url + '>')

@client.command()
async def trad(ctx, arg, arg2):

    print(arg2)

    language_out = arg.split(' ')
    language_out = language_out[0]

    language_in = detect(arg2)
    translator = Translator(to_lang=language_out, from_lang=language_in)
    translation = translator.translate(arg2)
    await ctx.message.channel.send(translation)

@client.command()
async def img(ctx):
    if ctx.message.attachments:
        files = []
        for i in ctx.message.attachments:
            files.append(i)
            await i.save(glob_path + i.filename)

        pages = convert_from_path(glob_path + i.filename, dpi=200)

        for idx,page in enumerate(pages):
            page.save(glob_path + i.filename+str(idx)+'.jpg', 'JPEG')
            await ctx.message.channel.send(file=discord.File(glob_path + i.filename+str(idx)+'.jpg', filename=str(i.filename+str(idx)+'.jpg')))
            os.remove(glob_path + i.filename+str(idx)+'.jpg')

        os.remove(glob_path + i.filename)

        await ctx.message.delete(delay=None)
    else:
        print("Where is the fucking document?!")
        await ctx.message.delete(delay=None)

@client.command()
async def rdm(ctx, arg):
    await ctx.message.delete(delay=None)

    lst = [arg]
    random_choices = (make_list(lst))
    random_result = random.choice(random_choices)
    await ctx.message.channel.send("Suspens...", delete_after=4)
    await asyncio.sleep(1)
    await ctx.message.channel.send(":three:", delete_after=1)
    await asyncio.sleep(1)
    await ctx.message.channel.send(":two:", delete_after=1)
    await asyncio.sleep(1)
    await ctx.message.channel.send(":one:", delete_after=1)
    await asyncio.sleep(1)
    await ctx.message.channel.send("Résultat : " + random_result + "\
    \nLes éléments étaient : " + str(random_choices) + "")

@client.command()
async def update(ctx, arg=None):

    guild = ctx.guild.id
    channels = ctx.guild.channels
    roles = ctx.guild.roles
    members = ctx.guild.members

    def update_channel():

        #channels
        with open(glob_path + str(guild) + '/channels.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file)

            new_content = []
            for channel in channels:
                csv_writer.writerow([channel.id, channel])
        csv_file.close()

        #roles
        with open(glob_path + str(guild) + '/roles.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file)

            new_content = []
            for role in roles:
                csv_writer.writerow([role.id, role])
        csv_file.close()

        #users
        with open(glob_path + str(guild) + '/members.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file)

            new_content = []
            for member in members:
                csv_writer.writerow([member.id, member])
        csv_file.close()

    if os.path.isdir(glob_path + str(guild)):
        update_channel()

    else:
        os.mkdir(glob_path + str(guild))
        update_channel()

    print(channels)
    print(roles)
    print(repr(ctx.guild.id))
    print(ctx.guild.members)

@client.command()
@commands.has_guild_permissions(administrator=True)
async def logs(ctx, arg1, arg2=None):

    guild = ctx.guild.id
    channels = ctx.guild.channels
    roles = ctx.guild.roles
    logs_status = glob_path + str(guild) + '/logs.txt'

    if not os.path.isdir(glob_path + str(guild)):
        await ctx.message.channel.send('You need to run t/update before turning on/off logs for your server')

    else:
        if arg1 == 'off':
            if not os.path.isfile(logs_status):
                await ctx.message.channel.send('Logs are already disabled.')
            else:
                 os.remove(logs_status)
                 await ctx.message.channel.send('Logs have been disabled.')
        elif arg1 == 'on':
            if not arg2:
                await ctx.message.channel.send('You need to specify in which text channel logs will be sent.')
            else:
                if os.path.isfile(logs_status):
                    await ctx.message.channel.send('Logs are already enabled.')
                else:
                    os.mknod(logs_status)

                    with open(glob_path + str(guild) + '/channels.csv', 'r') as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        for channel in csv_reader:
                            if channel[1] == arg2:
                                arg2_id = channel[0]
                                print(arg2_id)
                                if len(arg2_id) > 1:
                                    logs_file = open(logs_status, 'w')
                                    logs_file.write(arg2_id)
                                    logs_file.close()
                                    await ctx.message.channel.send('Logs have been enabled.')
                                else:
                                    await ctx.message.channel.send('This channel does not exist.')
        elif arg1 == "status":
            with open(logs_status, 'r') as text_file:
                for line in text_file:
                    log_channel_id = client.get_channel(int(line))
                    message = 'Logs are sent to this channel: ' + str(log_channel_id.mention) + ' ' + str(line)
                    await ctx.message.channel.send(message)

        else:
            await ctx.message.channel.send('The first argument is not correct. t/logs <on/off>.')


@logs.error
async def logs_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.channel.send('You are missing Administrator permission(s) to run this command.', delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.channel.send('<on/off> is a required argument that is missing.', delete_after=5)
    else:
        await ctx.message.channel.send("I'm sure you were wrong, but I don't know where... ", delete_after=5)

@client.command()
async def smtp(ctx, arg1, arg2=None, arg3=None, arg4=None, arg5=None):

    smtp_data = glob_path + str(ctx.author.id) + '/smtp.txt'
    print(smtp_data)

    async def set_smtp():

        if arg1 == "set":
            if not arg2:
                await ctx.message.channel.send('Missing password.')
            elif not arg3:
                await ctx.message.channel.send('Missing email account.')
            elif not arg4:
                await ctx.message.channel.send('Missing SMTP server port.')
            elif not arg5:
                await ctx.message.channel.send('Missing SMTP server.')
            else:
                with open(smtp_data, 'w') as csv_file:
                    csv_writer = csv.writer(csv_file)

                    new_content = [arg2, arg3, arg4, arg5]
                    print(new_content)
                    csv_writer.writerows(new_content)
                    csv_file.close()
                print("Nince!")

    if os.path.isdir(glob_path + str(ctx.author.id)):
        set_smtp()

    else:
        os.mkdir(glob_path + str(ctx.author.id))
        set_smtp()

@client.command()
async def help(ctx, arg=None):

    gif = "gif: send an mp4 or avi video file with /gif to convert it to a gif"
    help = "Fuck you bitch"
    img = "img: send a pdf file with /pdf to convert each page to an image"
    logs = 'logs: t/logs <on/off/status> <channel-name>'
    mp3 = "mp3: send an mp4 video file with /mp4 to convert it to an mp3 audio file"
    rdm = 'rdm: send /rdm <"arg1 arg2 arg2 ..."> to get a random choice of a list'
    trad = 'trad: send /trad <language> <"text to translate"> to get the translation of a text'
    wiki = 'wiki: send /wiki <key_word> to make a search on Wikipedia'

    list = ["gif", gif, "help", help, "img", img, "mp3", mp3, "rdm", rdm, "trad", trad, "wiki", wiki, 'logs', logs]

    if arg == None:
        print(arg)
        await ctx.message.channel.send("```Commands:\n\ngif\nhelp\nimg\nlogs\nmp3\nrdm\ntrad\nwiki\n\nType t/help <command> for mor info on a command.```")

    else:
        if arg in list:
            index = list.index(arg)
            index += 1
            command = list[index]
            await ctx.message.channel.send("```" + command + "```" )

client.run(TOKEN)
