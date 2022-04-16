import mediapipe as mp

from m42pl.commands import StreamingCommand
from m42pl.fields import Field


class MPHolistic(StreamingCommand):
    """Mediapipe holistic binding.
    """
    
    _aliases_   = ['mp_holistic',]
    _about_     = 'Detects human body movements'
    _syntax_    = '[[frame=]{source frame}]'
    _schema_    = {'properties': {}}

    def __init__(self, field: str = 'cv2.frame'):
        super().__init__(field)
        self.field = Field(field)
        self.landmarks = Field('mp.landmarks')

    async def setup(self, event, pipeline, context):
        self.mps_holistic = mp.solutions.holistic.Holistic(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            refine_face_landmarks=True
        ).__enter__()

    async def target(self, event, pipeline, context):
        frame = await self.field.read(event, pipeline, context)
        if frame is not None:
            # frame.flags.writeable = False
            results = self.mps_holistic.process(frame)
            # results = self.mps_face_detection.process(frame)
            # frame.flags.writeable = True
            if results.pose_landmarks:
                await self.landmarks.write(event, results.pose_landmarks)
        yield event

    async def __aexit__(self, *args, **kwargs) -> None:
        try:
            self.mps_face_detection.__exit__(*args, **kwargs)
        except Exception:
            pass
