# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import drjit as dr
import mitsuba as mi
import matplotlib.pyplot as plt
import numpy as np
import cv2


from tqdm import tqdm

def load_scene(Sun_Azimuth_deg, Elevation_Deg):

    X = np.sin(float(Sun_Azimuth_deg) * np.pi / 180.) * np.cos(Elevation_Deg * np.pi / 180.)
    Y = np.cos(float(Sun_Azimuth_deg) * np.pi / 180.) * np.cos(Elevation_Deg * np.pi / 180.)
    Z = np.sin(Elevation_Deg * np.pi / 180.)


    # Create a scene
    scene_dict = {
        'type': 'scene',
        #'integrator': {'type': 'prbvolpath'},
        'integrator': {'type': 'volpathmis'},
        'object': {
            'type': 'cube',
            'bsdf': {'type': 'null'},
            'interior': {
                'type': 'heterogeneous',
                'sigma_t': {
                    'type': 'gridvolume',
                    'filename': '/scenes/volume.vol',
                    'filename': 'D:\\Ofer\\cloudCT\\Clouds data\\BOMEX_57600_58x72x69_7611.vol',
                    'to_world': mi.ScalarTransform4f.rotate([1, 0, 0], -90).scale(2).translate(-0.5)
                },
                'scale': 40
            }
        },


        #'emitter':
        #    {'type': 'directional', #'directional',
        #     'direction': [X, Y, Z],
        #     'irradiance': {
        #             'type': 'rgb',
        #             'value': 10.0,
        #        }
        #    }
    }

    scene_dict['emitter'] = []
    scene_dict.update({'emitter':
            {'type': 'directional', #'directional',
             'direction': [X, Y, Z],
             'irradiance': {
                     'type': 'rgb',
                     'value': 10.0,
                }
            }},)

    scene_ref = mi.load_dict(scene_dict)
    return scene_ref, scene_dict


def set_sensor(Range_m, Aimuth_deg, Elevation_deg, FOV_Deg, N_pixels_x, N_pixels_y):

        #sensor_rotation = mi.ScalarTransform4f.rotate([0, 1, 0], yaw)
        X = Range_m * np.sin(Aimuth_deg * np.pi / 180.)
        Y = Range_m * np.cos(Aimuth_deg * np.pi / 180.)
        sensor_to_world = mi.ScalarTransform4f.look_at(target=[0, 0, 0], origin=[X, 0, Y], up=[0, 1, 0])

        #sensors.append(mi.load_dict({
        sensor = mi.load_dict({
            'type': 'perspective',
            'fov': FOV_Deg,
            #'to_world': sensor_rotation @ sensor_to_world,
            'to_world':  sensor_to_world,
            'film': {
                'type': 'hdrfilm',
                'width': N_pixels_x, 'height': N_pixels_y,
                'filter': {'type': 'tent'}
            }
        })
        return sensor

def set_light_source(type, Aimuth_deg, Elevation_Deg, ProjectorRange_m, scene_dict):

    if type == 'Sun':
        X = np.sin(Aimuth_deg * np.pi / 180.)# * np.cos((90+Elevation_Deg) * np.pi / 180.)
        Y = np.cos(Aimuth_deg * np.pi / 180.)# * np.cos((90+Elevation_Deg) * np.pi / 180.)
        Z = np.sin((90+Elevation_Deg) * np.pi / 180.)
        Sun_to_world = mi.ScalarTransform4f.look_at(target=[0, 0, 0], origin=[X, Y, Z], up=[0, 0, 1])

        scene_dict['emitter'] = []
        scene_dict.update({'emitter':
                               {'type': 'directional',  # 'directional',
                                'direction': [X, Y, Z],
                                'irradiance': {
                                    'type': 'rgb',
                                    'value': 10.0,
                                }
                                }}, )



        #scene_dict[]
        #scene_dict['direction'] : [1.0, 1.0, -1.0],
             #'direction': [1.0, 1.0, -1.0],
             #'irradiance': {
             #        'type': 'rgb',
             #        'value': 1.0,
             #                    })


    elif type == 'projector':


        #ProjectorRange_m = 50
        X = ProjectorRange_m * np.sin(Aimuth_deg * np.pi / 180.) * np.cos(Elevation_Deg * np.pi / 180.)
        Y = ProjectorRange_m * np.cos(Aimuth_deg * np.pi / 180.) * np.cos(Elevation_Deg * np.pi / 180.)
        Z = ProjectorRange_m * np.sin(Elevation_Deg * np.pi / 180.)
        proj_to_world = mi.ScalarTransform4f.look_at(target=[0, 0, 0], origin=[X, Y, Z], up=[0, 0, 1])

        scene_dict['emitter'] = []
        scene_dict.update({'emitter':
                               {'type': 'projector',
                                'irradiance': {
                                    'type': 'rgb',
                                    'value': 10.0,
                                },
                                'fov': 45,
                                'to_world': proj_to_world
                                }}, )

        """light_dict = {
            'type': 'projector',
            'irradiance': {
                'type': 'rgb',
                'value': 10.0,
            },
            'fov': 45,
            'to_world': mi.ScalarTransform4f.look_at(
                origin=[X, Y, Z],
                target=[0, 0, 0],
                up=[0, 0, 1]
                )

        }"""
    elif type == 'constant':
        light_dict =  {'type': 'constant',
                      #'radiance': {
                      #    'type': 'rgb',
                      #    'value': 1.0,
                      #}
                    }

    scene_ref = mi.load_dict(scene_dict)
    return scene_ref





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Import the library using the alias "mi"

    # Set the variant of the renderer
    #mi.set_variant('llvm_ad_rgb')
    #mi.set_variant('scalar_rgb')
    mi.set_variant('scalar_spectral')

    dirctions = 50
    Sensor_Azimuth_deg = 0
    Sensor_Elevation_deg = 0
    FOV_Deg = 45
    Range_m = 4
    ProjectorRange_m = 50
    N_pixels_x = 512
    N_pixels_y = 512
    SppNo = 16 #256
    sensor = []
    ref_images = []
    Sun_Azimuth_deg = 180   # clockwize from north
    Sun_Elevation_Deg = 45  # above horion

    scene_ref, scene_dict = load_scene(Sun_Azimuth_deg, Sun_Elevation_Deg )

    """---------- (1) check sensor viewpint --------"""
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = 10
    video_path = "D:\\Ofer\\cloudCT\\view_dirs\\cloud_view_dir.avi"
    video = cv2.VideoWriter(video_path, fourcc, fps, (N_pixels_x, N_pixels_y))


    for i in  tqdm(range(0, dirctions), desc ="Rendering view directions..."):
    ##for i in tqdm(range(0, 2), desc="Rendering view directions..."):
        Sensor_Azimuth_deg = 360.0 / float(dirctions) * i #- 90.0
        Sun_Azimuth_deg = 0
        Sun_Elevation_Deg = 0


        scene_ref = set_light_source('Sun', Sun_Azimuth_deg, Sun_Elevation_Deg, ProjectorRange_m, scene_dict)
        #
        #set_light_source('constant', Sun_Azimuth_deg, Sun_Elevation_Deg, ProjectorRange_m)
        #[scene_ref, scene_dict] = load_scene(Sensor_Azimuth_deg, Sun_Elevation_Deg)
        sensor = set_sensor(Range_m, Sensor_Azimuth_deg, Sensor_Elevation_deg, FOV_Deg, N_pixels_x, N_pixels_y)
        scene_ref = set_light_source('Sun', Sun_Azimuth_deg, Sun_Elevation_Deg, ProjectorRange_m, scene_dict)

        # Render the scene
        ref_image = mi.render(scene_ref, sensor=sensor, spp=SppNo)#spp=256)
        #ref_image = 1 - ref_image
        #plt.style.use('dark_background')
        plt.imshow(ref_image)
        plt.axis('off')



        ImageFileName = "D:\\Ofer\\cloudCT\\view_dirs\\cloud_view_dir_" + str(i) + ".jpg"
        mi.util.write_bitmap(ImageFileName, ref_image)


        # convert to video
        bmp_np = np.array(ref_image)
        type(bmp_np), bmp_np.dtype, bmp_np.shape
        (np.ndarray, type('float32'), (N_pixels_x, N_pixels_y, 3))
        # It is also possible to create a Bitmap object from a numpy array
        bmp_np = mi.Bitmap(np.tile(np.linspace(0, 1, 100), (100, 1)))
        video.write(np.array(bmp_np))
        plt.imshow(bmp_np)
        plt.axis('off')

    video.release()
    
    """---------- (2) check lighting direction change --------"""

    sensor = set_sensor(Range_m, 0, 0, FOV_Deg, N_pixels_x, N_pixels_y)

    for i in tqdm(range(0, dirctions), desc ="Rendering light directions ..."):
        Sun_Azimuth_deg = (360.0 / float(dirctions)) * i #- 90.0

        scene_ref = set_light_source('Sun', Sun_Azimuth_deg, Sun_Elevation_Deg, ProjectorRange_m, scene_dict)
        #scene_ref = load_scene(Sun_Azimuth_deg)
        # Render the scene
        ref_image = mi.render(scene_ref, sensor=sensor, spp=SppNo)#spp=256)
        #ref_image = 1 - ref_image
        #plt.style.use('dark_background')
        plt.imshow(ref_image)
        plt.axis('off')

        ImageFileName = "D:\\Ofer\\cloudCT\\\Sun_dir\\cloud_light_dir_" + str(i) + ".jpg"
        mi.util.write_bitmap(ImageFileName, ref_image)

    """---------- (3) check "fly thrugh" --------"""
    Sun_Azimuth_deg = 180   # clockwize from north
    Sun_Elevation_Deg = 45  # above horion
    Sensor_Azimuth_deg = 180

    scene_ref = set_light_source('Sun', Sun_Azimuth_deg, Sun_Elevation_Deg, ProjectorRange_m, scene_dict)
    Range_m = 5

    for i in tqdm(range(1, 200), desc="Rendering fly through ..."):
        Range_m = Range_m - 0.1
        sensor = set_sensor(Range_m, Sensor_Azimuth_deg, Sensor_Elevation_deg, FOV_Deg, N_pixels_x, N_pixels_y)

        # Render the scene
        ref_image = mi.render(scene_ref, sensor=sensor, spp=SppNo)#spp=256)
        #ref_image = 1 - ref_image
        #plt.style.use('dark_background')
        plt.imshow(ref_image)
        plt.axis('off')

        ImageFileName = "D:\\Ofer\\cloudCT\\fly\\fly_through_dir_" + str(i) + ".jpg"
        mi.util.write_bitmap(ImageFileName, ref_image)
