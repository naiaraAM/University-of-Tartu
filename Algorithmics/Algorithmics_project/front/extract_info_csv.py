import os

def convert_to_csv():
    with open("Data/stops.txt", 'r') as file:
        lines = file.readlines()
        with open('stops.csv', 'w') as new_file:
            for line in lines:
                new_file.write(line.replace(',', ';'))

def extract_relevant_info():
    with open("stops.csv", 'r') as file:
        lines = file.readlines()
        with open('tartu_stops.csv', 'w') as new_file:
            # write header only stop_id;stop_name;latitude;longitude
            new_file.write("stop_id;stop_name;latitude;longitude\n")
            for line in lines:
                if line.split(';')[-1] == "Tartu LV\n": # filter by Tartu Linn
                    stop_id = line.split(';')[0]
                    stop_name = line.split(';')[2]
                    latitude = line.split(';')[3]
                    longitude = line.split(';')[4]
                    new_file.write(f"{stop_id};{stop_name};{latitude};{longitude}\n")
    # remove stops.csv
    os.remove("stops.csv")


def obtain_coordinates():
    # this is the header, obtain pair latitude, longitude, stop_id and stop_name: stop_id;stop_code;stop_name;stop_lat;stop_lon;zone_id;alias;stop_area;stop_desc;lest_x;lest_y;zone_name;authority
    info_stops = []
    with open("tartu_stops.csv", 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            latitude = line.split(';')[2]
            longitude = line.split(';')[3]
            stop_id = line.split(';')[0]
            stop_name = line.split(';')[1]

            info_stops.append((latitude, longitude, stop_id, stop_name))
    return info_stops

def obtain_tartu_stops():
    convert_to_csv()
    extract_relevant_info()
    print(f"File tartu_stops.csv created in {os.getcwd()}")
    print("Obtain coordinates from the file")
    return obtain_coordinates()