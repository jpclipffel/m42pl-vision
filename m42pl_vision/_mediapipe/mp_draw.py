import numpy
import mediapipe as mp

from m42pl.commands import StreamingCommand
from m42pl.fields import Field


class MPDraw(StreamingCommand):
    """MediaPipe drawing utils bindings.
    """
    
    _aliases_   = ['mp_draw',]
    _about_     = 'Draw MediaPipe objects'
    _syntax_    = '[[frame=]{source frame}]'
    _schema_    = {'properties': {}}

    def __init__(self, frame: str = 'cv2.frame',
                    detections: str = 'mp.detections',
                    landmarks: str = 'mp.landmarks',
                    clear = None):
        """
        :param frame: OpenCV2 frame
        :param detections: MediaPipe detections data
        :param landmarks: MediaPipe landmarks data
        :param clean: Switch to remove frame content before drawing
            the objects
        """
        super().__init__(frame, detections, landmarks)
        self.frame = Field(frame)
        self.detections = Field(detections)
        self.landmarks = Field(landmarks)
        self.clear = Field(clear, default=False)
        # ---
        self.mps_drawing_spec = mp.solutions.drawing_utils.DrawingSpec(
            thickness=1,
            circle_radius=1
        )

    async def setup(self, event, pipeline, context):
        self.clear = await self.clear.read(event, pipeline, context)

    async def target(self, event, pipeline, context):
        frame = await self.frame.read(event, pipeline, context)
        if frame is not None:
            # ---
            # Remove frame content
            if self.clear:
                frame = numpy.zeros(frame.shape, numpy.uint8)
                frame[:] = (0, 0, 0)
            # ---
            # Get MediaPipe found objects
            detections = await self.detections.read(event, pipeline, context)
            landmarks = await self.landmarks.read(event, pipeline, context)
            # ---
            # Draw MediaPipe's detections
            if detections is not None:
                for detection in detections:
                    mp.solutions.drawing_utils.draw_detection(
                        image=frame,
                        detection=detection,
                        keypoint_drawing_spec=self.mps_drawing_spec
                    )
            # ---
            # Draw MediaPipe's landamrks
            if landmarks is not None:
                for landmark in landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        image=frame,
                        landmark_list=landmark,
                        # connections=self.mp_face_mesh.FACE_CONNECTIONS,
                        # connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=self.mps_drawing_spec,
                        connection_drawing_spec=self.mps_drawing_spec)
            # ---
            # Update frame field
            await self.frame.write(event, frame)
        # ---
        # Done
        yield event
