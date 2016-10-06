import json
import argparse


def load_data(filepath):
    with open(filepath, 'r') as jsonObj:
        data = json.load(jsonObj)
    return data


def get_biggest_bar(data):
    max = -1
    for d in data:
        if d['Cells']['SeatsCount'] > max:
            max = d['Cells']['SeatsCount']
            name = d['Cells']['Name']
            addr = d['Cells']['Address']
    return max, name, addr


def get_smallest_bar(data):
    min = data[0]['Cells']['SeatsCount']
    for d in data:
        if d['Cells']['SeatsCount'] < min:
            min = d['Cells']['SeatsCount']
            name = d['Cells']['Name']
            addr = d['Cells']['Address']
    return min, name, addr


def get_closest_bar(data, longitude, latitude):
    distance = 100.0
    for d in data:
        dist_temp = ((longitude - d['Cells']['geoData']['coordinates'][0])**2.0
            + (latitude - d['Cells']['geoData']['coordinates'][1])**2.0)**0.5
        if dist_temp < distance:
            distance = dist_temp
            name = d['Cells']['Name']
            addr = d['Cells']['Address']
    return name, addr


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Поиск ближайшего бара')
    parser.add_argument('--longitude', '-lg', type=float, 
                            default=37.614784240914, help='Долгота')
    parser.add_argument('--latitude', '-lt', type=float, 
                            default=55.882243910520, help='Широта')
    args = parser.parse_args()
    data = load_data('bars.json')
    min_seats_count, min_name, min_addr = get_smallest_bar(data)
    max_seats_count, max_name, max_addr = get_biggest_bar(data)
    closest_name, closest_addr = get_closest_bar(data, args.longitude,
                                                    args.latitude)
    min_str = 'Минимальное количество мест: %d\n\tназвание: %s, адрес: %s\n'
    max_str = 'Максимальное количество мест: %d\n\tназвание: %s, адрес: %s\n'
    closest_str = 'Ближайший бар "%s", адрес: %s'
    print(min_str % (min_seats_count, min_name, min_addr))
    print(max_str % (max_seats_count, max_name, max_addr))
    print(closest_str % (closest_name, closest_addr))
