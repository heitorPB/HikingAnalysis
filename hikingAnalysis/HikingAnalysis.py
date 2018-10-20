import gpxpy
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import geotiler
from matplotlib import animation
from matplotlib.patches import Ellipse
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D


class HikingAnalysis(object):
    def __init__(self, gpx_path, out_dir, statistics, plot_2d, plot_3d):
        self._gpx = gpxpy.parse(open(gpx_path))
        self._out_dir = out_dir
        self._statistics = statistics
        self._plot_2d = plot_2d
        self._plot_3d = plot_3d

    def go(self):
        if self._statistics:
            self.stats()
        if self._plot_2d:
            self.plot2D()
        if self._plot_3d:
            self.plot3D()

    def stats(self):
        print("Statistics of the hike:")
        print("")

        moving_time, stopped_time, moving_distance, stopped_distance, \
            max_speed = self._gpx.get_moving_data()
        print("\tdistance:", self._gpx.length_3d(), "m")
        print("\tduration:", self._gpx.get_duration(), "s")
        print("\tstarted:", self._gpx.get_time_bounds()[0])
        print("\tended:",   self._gpx.get_time_bounds()[1])
        print("\tMax speed:", max_speed, "m/s")
        avg_speed = moving_distance / moving_time
        print("\tAvg speed:", avg_speed, "m/s")

    def plot2D(self):
        gpx_bounds = self._gpx.get_bounds()
        bbox = [gpx_bounds.min_longitude - 0.002,
                gpx_bounds.min_latitude - 0.002,
                gpx_bounds.max_longitude + 0.002,
                gpx_bounds.max_latitude + 0.002]

        fig = plt.figure(figsize=(13, 13))
        ax = plt.subplot(111)

        # download tiles from OSM
        mm = geotiler.Map(extent=bbox, zoom=16)
        img = geotiler.render_map(mm)

        myMap = Basemap(llcrnrlon=bbox[0], llcrnrlat=bbox[1],
                        urcrnrlon=bbox[2], urcrnrlat=bbox[3],
                        projection='merc', ax=ax)
        myMap.imshow(img, interpolation='lanczos', origin='upper')

        # plot hike
        points = self._gpx.get_points_data()
        lon = [p[0].longitude for p in points]
        lat = [p[0].latitude for p in points]
        index = [p.point_no for p in points]  # color sequentially each point

        x, y = myMap(lon, lat)  # map (long, lat) to (x,y) coordinates in plot
        ax.scatter(x, y, c=index, s=4, cmap='brg')

        print("Printing map in", self._out_dir+'/map.png')
        plt.savefig(self._out_dir+'/map.png', quality=100, bbox_inches='tight')
        plt.close()

    def plot3D(self):
        points = self._gpx.get_points_data()
        gps_long = [p[0].longitude for p in points]
        gps_lat = [p[0].latitude for p in points]
        gps_elevation = [p[0].elevation for p in points]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        def init():
            N = len(gps_lat)
            for i in range(N - 1):
                ax.plot(gps_long[i:i + 2],       # x coordinate
                        gps_lat[i:i + 2],        # y,
                        gps_elevation[i:i + 2],  # z
                        color=plt.cm.viridis(i / N))  # sequential color

            ax.set_xlabel("longitude")
            ax.set_ylabel("latitude")
            ax.set_zlabel("altitude (meters)")

            return fig,

        def animate(i):
            ax.view_init(elev=10., azim=i)
            return fig,

        print("Saving animation in", self._out_dir+'/animation.mp4')
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=360, interval=20, blit=True)
        anim.save(self._out_dir+'/animation.mp4', fps=30,
                  extra_args=['-vcodec', 'libx264'])
