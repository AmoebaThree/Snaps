if __name__ == '__main__':
    import systemd.daemon
    import picamera
    import redis
    import os

    print('Startup')

    camera = picamera.PiCamera()
    root_dir = '~/snaps/pi/'
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    r = redis.Redis(host='192.168.0.1', port=6379, db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('snaps.pi')

    print('Startup complete')
    systemd.daemon.notify('READY=1')

    try:
        for message in p.listen():
            filename = message['data']
            camera.capture(root_dir + filename + ".jpg")
            p.publish('snaps.pi.capture', filename)
    except:
        p.close()
        print('Goodbye')
