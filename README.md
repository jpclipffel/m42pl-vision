# M42PL - Computer vision commands

This repository host a set of commands to use computer vision with M42PL.
M42PL extensively wraps [OpenCV](opencv) and [MediaPipe](mediapipe).

## Installation

* Ensure [M42PL](m42pl-core) is installed
* Clone the repository: `git clone https://github.com/jpclipffel/m42pl-vision`
* Install the package: `pip install -e m42pl-vision`

## Usage

Include the package when starting M42PL, e.g. `m42pl repl -m m42pl_vision`.

## Use cases

### Camera stream

```
| cv_stream
| cv_show
```

* `cv_stream` read frames from a video device
* `cv_show` display a video stream

### Camera stream over ZMQ

From the device having access to the video device(s):

```
| cv_stream
| cv_resize ratio=0.5
| zmq_pub topic='video'
```

* `cv_stream` read frames from a video device
* `cv_resize` resize the video size
* `zmq_pub` automatically encode and forward the stream on a ZMQ socket

From the device processing the video stream:

```
| zmq_sub topic='video'
| decode {zmq.frames[0]} with 'msgpack'
| fields cv2
| cv_show
```

* `zmq_sub` receives a stream of ZMQ event
* `decode` decodes the ZMQ stream (by default, ZMQ stream encode the events with `msgpack`)
* `fields` filter all events excepts `cv2`
* `cv_show` display a video stream

### Faces recognition

```
| cv_stream
| cv_resize ratio=0.5
| mp_faces
| mp_draw
```

* `cv_stream` read frames from a video device
* `cv_resize` resize the video size
* `mp_faces` detects faces
* `mp_draw` draw detected faces

---

[opencv]: ?
[mediapipe]: ?
