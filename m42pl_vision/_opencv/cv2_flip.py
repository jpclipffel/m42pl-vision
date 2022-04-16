import cv2

from functools import partialmethod

from m42pl.commands import StreamingCommand
from m42pl.fields import Field


class CV2Flip(StreamingCommand):
    """Flips an OpenCV2 frame.
    """

    _aliases_   = ['cv_flip',]
    _about_     = 'Flip an OpenCV2 frame'
    _syntax_    = '[[field=]{frame}] [[direction=]<u(p)|d(own)|r(ight)|l(eft)>]'
    _schema_    = {'properties': {}}

    def __init__(self, field: str = 'cv2.frame', direction = None):
        super().__init__(field)
        self.field = Field(field)
        self.direction = Field(direction, default='u')
        self.flip = None

    async def setup(self, event, pipeline, context):
        direction = await self.direction.read(event, pipeline, context)
        if direction in ["u", "up", "d", "down"]:
            self.flip = 0
        elif direction in ["l", "left", "r", "right"]:
            self.fliip = 1
        elif direction in ['f', 'full']:
            self.flip = -1

        # match direction:
        #     case ("u"|"up"|"d"|"down"):
        #         self.flip = 0
        #     case ("l"|"left"|"r"|"right"):
        #         self.flip = 1
        #     case ("f"|"full"):
        #         self.flip = -1
        #     case _:
        #         pass

    async def target(self, event, pipeline, context):
        try:
            if self.flip is not None:
                await self.field.write(
                    event,
                    cv2.flip(
                        await self.field.read(event, pipeline, context),
                        self.flip
                    )
                )
        except Exception as error:
            self.logger.exception(error)
        yield event
