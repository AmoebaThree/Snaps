import systemd.daemon
import picamera
import redis
import os


def execute():
    print('Startup')

    camera = picamera.PiCamera()

    root_dir = '/home/pi/snaps/pi/'
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    r = redis.Redis(host='192.168.0.1', port=6379,
                    db=0, decode_responses=True)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('snaps.pi')

    r.publish('services', 'snaps.pi.on')
    systemd.daemon.notify('READY=1')
    print('Startup complete')

    try:
        for message in p.listen():
            filename = message['data']
            camera.capture(root_dir + filename + ".jpg")
            r.publish('snaps.pi.capture', filename)
    except:
        p.close()
        r.publish('services', 'snaps.pi.off')
        print('Goodbye')


if __name__ == '__main__':
    execute()
