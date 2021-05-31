import logging

from game.plugins import base


logger = logging.getLogger(__name__)


class ExampleGamePlugin(base.Base):

    def on_init(self):
        # logger.info('on_init')
        pass