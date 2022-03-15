import discord
import asyncio
import sys
import threading
#import requests

key = open("key.txt", "r").read();

url = "https://musicbird.leanstream.co/JCB033"
# audiosource = requests.get(url, stream=True).iter_content(chunk_size=None).__next__

# https://discordapp.com/oauth2/authorize?client_id=876291964063076412&scope=bot
class MyClient(discord.Client):
  
  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))
    self.beep = False
    self.audiosource = False

  async def on_message(self, message):
    if message.content[:13] == 'get over here':
      try:
        channel = message.author.voice.channel
      except AttributeError:
        print("wrong channel")
        return;
      if not channel in [i.channel for i in self.voice_clients]:
        vc = await channel.connect()
        audiosource = discord.FFmpegPCMAudio(url)
        vc.play(audiosource, after=print)
        #self.beep.play(self.audiosource, after=lambda e: (await close_audio(e) for _ in [None]).__anext__())
    elif message.content[:7] == 'goodbye':
      # todo: check that sender is in channel with bot
      try:
        channel = message.author.voice.channel
      except AttributeError:
        print("wrong channel")
        return;
      vc = None
      for i in self.voice_clients:
        if i.channel == channel:
          vc = i
      await self.close_audio(vc = vc)
  
  async def close_audio(self, e=None, vc = None):
    print('done ', e)
    # do something before disconnecting
    if vc != None:
      await vc.disconnect()
  
  async def console_command(self, query):
    print("query is", query)
    if query == "stop":
      await self.close()
      return False
    elif query == "test":
      print(len(self.voice_clients))
    elif query == "connection":
      print(self.user)
    return True
  
  async def listen_console(self):
    loop = True
    while loop:
      thing = input("put it in: ")
      loop = await self.console_command(thing)
    pass
  
    
  
# https://musicbird.leanstream.co/JCB033  
# ?listening-from-radio-garden=1629001670

async def main():
  client = MyClient()
  loop = asyncio.get_event_loop()
  loop.add_reader(sys.stdin.fileno(), client.console_command)
  await asyncio.gather(client.start(key))
#asyncio.run(main())
def thread_main():
  client = MyClient()
  threads = [threading.Thread(target=client.run, args=(key,)), threading.Thread(target=asyncio.run, args=(client.listen_console(),))]
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()
thread_main()

#def real_thread_main():
#  lock1 = threading.Lock()
#  lock2 = threading.Lock()
#  console_message = ""
#  def bot_thread():
#    client = MyClient()
#  def con_thread():
#    online = True
#    while online:
#      console_message = input("type a command: ")
#      lock stuff: release M2
#      lock stuff: block acquire M1
#      lock stuff: 
#      lock stuff: 
    
  
#client.run(key)
