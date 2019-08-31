import logging
import os
import pkgutil

class Brain(object):

  def __init__(self, mic, config):

    self.mic = mic
    self.config = config
    self.modules = self.get_modules()
    self._logger = logging.getLogger(__name__)
  
  @classmethod
  def get_modules(cls):
    """
    Load the modules from the modules folder
    Sorts them by PRIORITY to omit overlaps
    PRIORITY defaults to 0
    """

    logger = logging.getLogger(__name__)
    locations = '../modules' #This needs to be changed when migrating off repl
    logger.debug('Looking for modules')
    
    modules = []
    for finder, name, ispkg in pkgutil.walk_packages(locations):
      try:
        loader = finder.find_modules(name)
        mod = loader.load_module(name)
      except:
        logger.warning('Skipped loading module {} due to an error'.format(name), exc_info=True)
      else:
        if hasattr(mod, 'WORDS'):
          logger.debug('Found module {} with keywords {}'.format(name, mod.WORDS))
          modules.append(mod)
        else:
          logger.warning('Skipped loading module {} due to no keywords'.format(name))
      modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, "PRIORITY") else 0, reverse=True)
      return modules
  def query(self, texts):

    for module in self.modules:
        for text in texts:
          if module.IsValid(text):
            self._logger.debug('{} is a valid phrase for module {}'.format(text, module.__name__))
            try:
              module.handle(text, self.mic, self.config)
            except Exceptions:
              self._logger.error('Failed to excecute module {}'.format(module.__name__, exc_info=True))
              self.mic.say("I'm sorry, I had trouble operating module {}.".format(module.__name__))
            else:
              self._logger.debug('{} was completed'.format(module.__name__))
            finally:
              return
    self._logger.debug('No module was able to handle any of the phrases : {}'.format(texts  ))