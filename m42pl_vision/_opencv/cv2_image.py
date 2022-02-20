from __future__ import annotations

import cv2

from m42pl.commands import GeneratingCommand
from m42pl.fields import Field
from m42pl.event import derive


class CV2Image(GeneratingCommand):
    """Reads an image file with OpenCV.
    """

    _aliases_   = ['cv_image',]
    _syntax_    = '[source=]{source file}'
    _about_     = 'Read an image with OpenCV'
    _schema_    = {
        'properties': {
            'cv2': {
                'type': 'object',
                'properties': {
                    'frame': {
                        'description': 'Read frame'
                    },
                    'source': {
                        'description': 'Image file name',
                        'type': 'string'
                    }
                }
            }
        }
    }

    def __init__(self, source: str|int = 0):
        """
        :param source:  Source stream (defaults to `0` (webcam))
        """
        super().__init__(source)
        self.source = Field(source, default=0)

    async def target(self, event, pipeline):
        source = await self.source.read(event, pipeline)
        yield derive(event, {
            'cv2': {
                'frame': cv2.imread(source),
                'source': source
            }
        })
