import discord
from discord.ext import commands
import requests
import asyncio
from bs4 import BeautifulSoup
import multidict
import re
from wordcloud import WordCloud
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helpy import hell

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://www.cleverbot.com')
browser.execute_script('noteok()')

class MachineLearningShit(commands.Cog, name='Machine Learning Shit'):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(help=hell['word'])
	async def word(self, ctx):

		r = requests.get('https://www.thisworddoesnotexist.com/')
		soup = BeautifulSoup(r.text, 'html.parser')
		defword = soup.find(id='definition-word').string
		deflink = soup.find(id='link-button-a')['href']
		defgrammar = soup.find(id='definition-pos').string
		defgrammar = defgrammar.replace('"','').strip()
		defex = soup.find(id='definition-example').string
		defdef = soup.find(id='definition-definition').string
		defdesc = defgrammar + ' ' + defdef
		e = discord.Embed(title=defword, url=deflink,color=0x002258)
		e.add_field(name=defdesc, value=defex)
		e.set_footer(text='Powered by This Word Does Not Exist',icon_url='https://www.thisworddoesnotexist.com/favicon-32x32.png')
		await ctx.send(embed=e)

	@commands.command(help=hell['wordcloud'])
	async def wordcloud(self, ctx, chanlimit=100, maxim=100):

		def getFrequencyDictForText(sentence):
			fullTermsDict = multidict.MultiDict()
			tmpDict = {}

			for text in sentence.split(" "):
				if text.startswith(('.','f.','!','<','-','?','$','_',':')):
					continue
				if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
					continue
				val = tmpDict.get(text, 0)
				tmpDict[text.lower()] = val + 1
			for key in tmpDict:
				fullTermsDict.add(key, tmpDict[key])
			return fullTermsDict

		messages = []
		for channel in ctx.guild.channels:
			if isinstance(channel, discord.TextChannel) and channel.permissions_for(ctx.guild.me).read_messages:
				async for stuff in channel.history(limit=chanlimit):
					messages.append(stuff.content)
		text = ' '.join(messages)
		wordcloud = WordCloud(max_words=maxim,width=1920, height=1080, min_word_length=2).generate_from_frequencies(getFrequencyDictForText(text))
		wordcloud.to_file('wc.png')
		await ctx.send(file=discord.File('wc.png', filename='wordcloud.png'))

	@commands.command(help=hell['chat'])
	async def chat(self, ctx, *question: str):

		async with ctx.channel.typing():
			q = []
			for word in question:
				if word.startswith('<@'):
					word = re.sub('[^0-9]', '', word)
					word = self.bot.get_user(int(word)).name
				if word.startswith('<#'):
					word = re.sub('[^0-9]', '', word)
					word = self.bot.get_channel(int(word)).name
				if word.startswith('<:') or word.startswith('<a:') or word.startswith(':'):
					continue
				q.append(word)
			q = ' '.join(q)
			inputbox = browser.find_element_by_name('stimulus')
			inputbox.clear()
			inputbox.send_keys(q)
			inputbox.send_keys(Keys.RETURN)
			await asyncio.sleep(5)
			response = browser.find_element_by_xpath("//p[@id='line1']/span")
			await ctx.send(content=response.text)