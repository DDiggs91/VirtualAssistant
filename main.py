# Import statements
import logging
import os
import sys

from client.conversation import Conversation
'''from client import diagnose'''
local = True
if local:
  from client.local_mic import Mic
else:
  from client.mic import Mic


# Determine if the code is open


class VirtualAssistant(object):

  def __init__(self):

    self._logger = logging.getLogger(__name__)

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'PATH_TO_SERVICEAUTH_FILE'

    #Load Config file when applicable
    self.config = None

    #Initialize Mic
    self.mic = Mic()
  
  def run(self):
    self.mic.say("Wakeup Message")
    converstation = Conversation("AssistantName", self.mic, self.config)
    converstation.handleForever()

if __name__ == "__main__":
  print('{:*^32}'.format(''))
  print('*{:^30}*'.format('VIRTUAL ASSISTANT'))
  print('*{:^30}*'.format(' CREATED BY DANIEL DIGGS'))
  print('{:*^32}'.format(''))

  logging.basicConfig()
  logger = logging.getLogger()
  logger.getChild('client.stt').setLevel(logging.INFO)

  debug = True
  if debug:
    logger.setLevel(logging.DEBUG)
    #not sure if diagnose is useful
  '''elif diagnose:
    failed_checks = diagnose.run()
    sys.exit(0 if not failed_checks else 1)'''

  try:
    app = VirtualAssistant()
  except Exception:
    logger.error('Error occured!', exc_info=True)
    sys.exit(1)
  app.run()