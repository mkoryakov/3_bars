import json
import argparse


def get_seats_count_in_bar(bar):
    return bar['Cells']['SeatsCount']
    
    
def load_data(filepath):
    with open(filepath, 'r') as json_handler:
        data = json.load(json_handler)
    return data


def get_biggest_bar(data):
    biggest_bar = max(data, key=get_seats_count_in_bar)
    seats_count = biggest_bar['Cells']['SeatsCount']
    name = biggest_bar['Cells']['Name']
    address = biggest_bar['Cells']['Address']
    return seats_count, name, address


def get_smallest_bar(data):
    smallest_bar = min(data, key=get_seats_count_in_bar)
    seats_count = smallest_bar['Cells']['SeatsCount']
    name = smallest_bar['Cells']['Name']
    address = smallest_bar['Cells']['Address']
    return seats_count, name, address


def get_closest_bar(data, longitude, latitude):
    distance = lambda bar: (
            (longitude - bar['Cells']['geoData']['coordinates'][0])**2.0 + 
            (latitude - bar['Cells']['geoData']['coordinates'][1])**2.0)**0.5
    closest_bar = min(data, key=distance)
    name = closest_bar['Cells']['Name']
    address = closest_bar['Cells']['Address']
    return name, address


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Поиск ближайшего бара')
    parser.add_argument('--longitude', '-lg', type=float, 
                            default=37.614784240914, help='Долгота')
    parser.add_argument('--latitude', '-lt', type=float, 
                            default=55.882243910520, help='Широта')
    args = parser.parse_args()
    data = load_data('bars.json')
    (smallest_bar_seats_count, smallest_bar_name, 
        smallest_bar_address) = get_smallest_bar(data)
    (biggest_bar_seats_count, biggest_bar_name, 
        biggest_bar_address) = get_biggest_bar(data)
    (closest_bar_name, closest_bar_address) = get_closest_bar(data, 
                                    args.longitude, args.latitude)
    smallest_bar_format_str = '''Минимальное количество мест: %d
\tназвание: %s, адрес: %s\n'''
    biggest_bar_format_str = '''Максимальное количество мест: %d
\tназвание: %s, адрес: %s\n'''
    closest_bar_format_str = 'Ближайший бар "%s", адрес: %s'
    print(smallest_bar_format_str % 
        (smallest_bar_seats_count, smallest_bar_name, smallest_bar_address))
    print(biggest_bar_format_str % 
        (biggest_bar_seats_count, biggest_bar_name, biggest_bar_address))
    print(closest_bar_format_str % (closest_bar_name, closest_bar_address))
