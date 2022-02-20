import cv2
import mediapipe as mp

from m42pl.commands import StreamingCommand
from m42pl.fields import Field, FieldsMap


class MPFaces(StreamingCommand):
    """Mediapipe faces detection binding.
    """
    
    _aliases_   = ['mp_facesmesh', 'mp_facemesh']
    _about_     = 'Detects faces structure'
    _syntax_    = '[[frame=]{source frame}]'

    def __init__(self, frame: str = 'cv2.frame', landmarks: str = 'mp.landmarks'):
        super().__init__(frame)
        self.frame = Field(frame)
        self.landmarks = Field(landmarks)

        # self.max_num_faces = Field(kwargs.get('max_num_faces'), default=6)
        # ---
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh
        # ---
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        # ---
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_faces=6).__enter__()

    async def target(self, event, pipeline, context):
        frame = await self.frame.read(event, pipeline, context)
        frame.flags.writeable = False
        results = self.face_mesh.process(frame)
        frame.flags.writeable = True
        # ---
        if results.multi_face_landmarks:
            await self.landmarks.write(event, results.multi_face_landmarks)

            # for face_landmarks in results.multi_face_landmarks:
            #     self.mp_drawing.draw_landmarks(
            #         image=frame,
            #         landmark_list=face_landmarks,
            #         # connections=self.mp_face_mesh.FACE_CONNECTIONS,
            #         connections=self.mp_face_mesh.FACEMESH_TESSELATION,
            #         landmark_drawing_spec=self.drawing_spec,
            #         connection_drawing_spec=self.drawing_spec)
        
        # yield await self.field.write(event, frame)
        yield event

    # async def __aexit__(self, *args, **kwargs):
    #     self.face_mesh.__exit__()
