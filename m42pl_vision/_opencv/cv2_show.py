from __future__ import annotations

import cv2

from m42pl.commands import StreamingCommand
from m42pl.fields import Field


class CV2Show(StreamingCommand):
    """Displays a frame with OpenCV.
    """

    _aliases_   = ['cv_show',]
    _syntax_    = '[[field=]{frame field}]'
    _about_     = 'Display a frame or freame stream'
    _schema_    = {'properties': {}}

    def __init__(self, field: str = 'cv2.frame', title: str|None = None):
        super().__init__(field)
        self.field = Field(field)
        self.title = Field(title, default=self._aliases_[0])
    
    async def setup(self, event, pipeline, context):
        self.title = await self.title.read(event, pipeline, context)

    async def target(self, event, pipeline, context):
        try:
            cv2.imshow(self.title, await self.field.read(event, pipeline, context))
            cv2.waitKey(1)
        except Exception as error:
            self.logger.exception(error)
        yield event

    async def __aexit__(self, *args, **kwargs):
        try:
            cv2.waitKey(1)
            cv2.destroyAllWindows()
        except Exception:
            pass
