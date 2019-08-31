import logging
#from notifier import Notifier to handle timed events

#probably change this import when not on REPL.IT
from client.brain import Brain

class Conversation(object):
  
  def __init__(self, WakeWord : str, mic, config):

    self.logger = logging.getLogger(__name__)
    self.WakeWord = WakeWord
    self.config = config
    self.brain = Brain(mic, config)
    # self.notifier = Notifier(profile)
  
  def handleForever(self):

    self._logger.info('Starting to handle conversation with keyword {}'.format(self.WakeWord))
    
    while True:
      #handle notifications from list here

      self._logger.info('Began listening for WakeWord')
      threshold, transcribed = self.mic.passiveListen(self.wakeWord)
      self._logger.info('Finished listening for WakeWord')

      if not transcribed or not threshold:
        self._logger.info('Volume was not above threshold or was not transcribed')
      self._logger.info('WakeWord was detected')

      self._logger.debug("Started to listen actively with threshold: %r", threshold)
      input = self.mic.activeListenToAllOptions(threshold)
      self._logger.debug("Stopped to listen actively with threshold: %r", threshold)

      if input:
          self.brain.query(input)
      else:
          self.mic.say("Pardon?")
