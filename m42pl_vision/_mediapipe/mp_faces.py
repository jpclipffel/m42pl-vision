import cv2
import mediapipe as mp

from m42pl.commands import StreamingCommand
from m42pl.fields import Field


class MPFaces(StreamingCommand):
    """Mediapipe faces detection binding.
    """
    
    _aliases_   = ['mp_faces', 'mp_face']
    _about_     = 'Detects faces'
    _syntax_    = '[[frame=]{source frame}]'
    _schema_    = {'properties': {}}

    def __init__(self, field: str = 'cv2.frame'):
        super().__init__(field)
        self.field = Field(field)
        self.detections = Field('mp.detections')

    async def setup(self, event, pipeline, context):
        self.mps_face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5
        ).__enter__()

    async def target(self, event, pipeline, context):
        frame = await self.field.read(event, pipeline, context)
        if frame is not None:
            # frame.flags.writeable = False
            results = self.mps_face_detection.process(frame)
            # frame.flags.writeable = True
            if results.detections:
                await self.detections.write(event, results.detections)
        yield event

    async def __aexit__(self, *args, **kwargs) -> None:
        try:
            self.mps_face_detection.__exit__(*args, **kwargs)
        except Exception:
            pass
