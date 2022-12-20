import carla
import random
import time
client = carla.Client('localhost' , 2000)
client.set_timeout(15.0)
world = client.get_world()
world = client.load_world('Town01')
spectator = world.get_spectator()
settings = world.get_settings()
settings.fixed_delta_seconds = 0
settings.synchronous_mode = True
world.apply_settings(settings)

actorsList = world.get_actors()

for actor in actorsList:
    if ('vehicle' in actor.type_id) and (actor.is_alive):
        actor.destroy()
for camera in actorsList:
    if ('sensor' in camera.type_id) and (camera.is_alive):
        camera.destroy()
for walker in actorsList:
    if ('walker' in walker.type_id) and (walker.is_alive):
        walker.destroy()

bp_lip = world.get_blueprint_library()
spawn_points = world.get_map().get_spawn_points()

vehicle_bp = bp_lip.find('vehicle.lincoln.mkz_2020')
vehicle = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))
for i in range(100):
    vehicle_bp = random.choice(bp_lip.filter('vehicle'))
    npc = world.try_spawn_actor(vehicle_bp , random.choice(spawn_points))
vs = world.get_actors().filter('*vehicle*')
for v in vs:
    v.set_autopilot(True)

camera_bp = bp_lip.find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '1920')
camera_bp.set_attribute('image_size_y', '1080')
camera_bp.set_attribute('fov', '110')
camera_bp.set_attribute('sensor_tick', '1.0')
camera = world.try_spawn_actor(camera_bp, carla.Transform(carla.Location(x=0.4, z=1.7)), attach_to=vs[0])
camera.listen(lambda image: image.save_to_disk('%.6d.jpg' % image.frame))
while(True):
    time.sleep(0.1)
    world.tick()