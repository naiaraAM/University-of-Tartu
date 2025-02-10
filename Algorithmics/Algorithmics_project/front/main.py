import extract_info_csv
import matplotlib.pyplot as plt

def draw_map(info_stops):

    latitude = [float(info[0]) for info in info_stops]
    longitude = [float(info[1]) for info in info_stops]
    # point must be smaller
    plt.scatter(latitude, longitude, s=3)
    return plt

def get_input_latitude():
    min_latitude = min([float(info[0]) for info in info_stops])
    max_latitude = max([float(info[0]) for info in info_stops])

    latitude_aux = -1
    while not min_latitude <= latitude_aux <= max_latitude:
        print(f"Latitude must be in the range [{min_latitude}, {max_latitude}]")
        latitude_aux = float(input("Enter latitude: "))
    print(f"Latitude {latitude_aux} is in the range [{min_latitude}, {max_latitude}]")
    return latitude_aux

def get_input_longitude():
    min_longitude = min([float(info[1]) for info in info_stops])
    max_longitude = max([float(info[1]) for info in info_stops])

    longitude_aux = -1
    while not min_longitude <= longitude_aux <= max_longitude:
        print(f"Longitude must be in the range [{min_longitude}, {max_longitude}]")
        longitude_aux = float(input("Enter longitude: "))
    print(f"Longitude {longitude_aux} is in the range [{min_longitude}, {max_longitude}]")
    return longitude_aux

def add_input_point(plot, input_latitude, input_longitude):
    plot.scatter(input_latitude, input_longitude, s=10, c='red')
    return plot

def find_n_nearest_stop(rtree, input_latitude, input_longitude, n):
    return rtree.nearest((input_latitude, input_longitude), n)


if __name__ == "__main__":
    info_stops = extract_info_csv.obtain_tartu_stops()
    plot = draw_map(info_stops)

    input_latitude = get_input_latitude()
    input_longitude = get_input_longitude()

    plot = add_input_point(plot, input_latitude, input_longitude)
    plot.show()






