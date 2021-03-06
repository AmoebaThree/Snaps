import systemd.daemon
import redis
import os
import http.server
import socketserver
import threading

root_dir = '/home/pi/snaps/cam/'


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=root_dir, **kwargs)


def serve():
    with socketserver.TCPServer(("", 7999), Handler) as httpd:
        httpd.serve_forever()


def execute():
    print('Startup')

    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    r = redis.Redis(host='192.168.0.1', port=6379,
                    db=0, decode_responses=True)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('snaps.cam')

    t = threading.Thread(target=serve, daemon=True)
    t.start()

    r.publish('services', 'snaps.cam.on')
    systemd.daemon.notify('READY=1')
    print('Startup complete')

    try:
        for message in p.listen():
            filename = message['data']
            os.system(
                'fswebcam --device v4l2:/dev/video0 --input 0 --no-banner --resolution 640x360 ' + root_dir + filename + '.jpg')
            r.publish('snaps.cam.capture', filename)
    except:
        p.close()
        r.publish('services', 'snaps.cam.off')
        print('Goodbye')


if __name__ == '__main__':
    execute()
