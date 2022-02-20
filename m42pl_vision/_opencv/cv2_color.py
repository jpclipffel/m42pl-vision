import cv2
import regex

from functools import partialmethod

from m42pl.commands import StreamingCommand
from m42pl.fields import Field


class CV2Color(StreamingCommand):
    """Changes the color space of an OpenCV2 frame.
    """

    _aliases_   = ['cv_color',]
    _about_     = 'Change an OpenCV2 frame color space'
    _syntax_    = '[[field=]{frame}] [[code=]<code name>]'
    _schema_    = {'properties': {}}

    def __init__(self, field: str = 'cv2.frame', code = None):
        super().__init__(field)
        self.field = Field(field)
        self.code = Field(code)

    async def setup(self, event, pipeline, context):
        code_rx = regex.match(
            r'(COLOR_)?(?P<code>.+)',
            await self.code.read(event, pipeline, context)
        )
        if code_rx is not None:
            self.code = getattr(cv2, f"COLOR_{code_rx.groupdict()['code'].upper()}")

    async def target(self, event, pipeline, context):
        try:
            if self.code is not None:
                await self.field.write(
                    event,
                    cv2.cvtColor(
                        await self.field.read(event, pipeline, context),
                        self.code
                    )
                )
        except Exception as error:
            self.logger.exception(error)
        yield event
