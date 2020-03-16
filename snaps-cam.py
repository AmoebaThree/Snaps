import systemd.daemon
import redis
import os


def execute():
    print('Startup')

    root_dir = '/home/pi/snaps/cam/'
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    r = redis.Redis(host='192.168.0.1', port=6379,
                    db=0, decode_responses=True)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('snaps.cam')

    print('Startup complete')
    systemd.daemon.notify('READY=1')

    try:
        for message in p.listen():
            filename = message['data']
            os.system(
                'fswebcam --device v4l2:/dev/video0 --input 0 --no-banner --resolution 640x360 ' + root_dir + filename + '.jpg')
            r.publish('snaps.cam.capture', filename)
    except:
        p.close()
        print('Goodbye')


if __name__ == '__main__':
    execute()
