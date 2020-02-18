from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import time
geolocator = Nominatim(user_agent="app")


def read_data():
    '''
    () -> tuple(int,tuple(float,float))
    get data from user
    '''a
    try:
        year = int(input('Year:'))
        latitude = float(input('latitude:'))
        longitude = float(input('longitude:'))
        return year, (latitude, longitude)
    except:
        print('Input error')
        return None


def get_data_csv(path):
    '''
    (str) -> dict
    get data from csv file
    '''
    data = {}
    file = open(path)
    for line in file:
        line = line.strip()
        title = line.split(',')[0]
        try:
            year = line.split(' ,')[1][0:4]
            year = int(year)
        except:
            continue
        location = line.split(',')[-1]
        if (title, year) not in data:
            data[(title, year)] = [location]
        else:
            data[(title, year)].append(location)
    return data


def write_data(data):
    '''
    dict -> int
    one time write data in files(sorted by years) to optimize program
    '''
    losed = 0
    checked = 0
    for i in data:
        p1 = '/home/bogdan/Documents/1yr_2sm_lab/lab_2/'
        p2 = 'lab_2_t2/locations_years/'
        title_f = p1 + p2 + \
            str(i[1]) + '.txt'
        file = open(str(title_f), 'a')
        for j in data[i]:
            try:
                file.write('e')
                print(1)
                location = geolocator.geocode(j)
                file.write(i[0] + '\t' + str(location.latitude) +
                           ' ' + str(location.longitude) + '\n')
                checked += 1
                print(1)
                print(str(checked) + '---------' + j)
                losed = 0
            except:
                try:
                    location = geolocator.geocode(j)
                    file.write(i[0] + '\t' + str(location.latitude) +
                               ' ' + str(location.longitude) + '\n')
                    checked += 1
                    print(1)
                    print(str(checked) + '---------' + j)
                    losed = 0
                except:
                    losed += 1
            print('losed: ' + str(losed))
            if losed >= 20:
                print('sleep_on')
                time.sleep(300)
                print('sleep_off')
                losed = 0
    return losed


def capitals():
    '''
    None -> None
    create third layer
    '''
    rez = []
    s_america = [
        'Brazil',
        'Argentina',
        'Chile',
        'Colombia',
        'Peru',
        'Bolivia',
        'Venezuela',
        'Ecuador',
        'Uruguay',
        'Paraguay',
        'Guyana',
        'Suriname',
        'Fremch Guiana',
        'Aruba',
        'Trinidad and Tobago']
    file = open(
        '/home/bogdan/Documents/1yr_2sm_lab/lab_2/lab_2_t2/countries.txt')
    for line in file:
        line = line.strip().split('\t')
        if line[3] in s_america:
            rez.append((float(line[1]), float(line[2])))
    return rez


def get_map(year, latitude, longitude):
    '''
    (int, float, float) -> None
    create map(HTML file)
    '''
    map_ = folium.Map()
    map_.add_child(folium.Marker(
        location=[latitude, longitude], popup="Ви тут!"))
    p1 = '/home/bogdan/Documents/1yr_2sm_lab/lab_2/'
    file = open(p1 + 'lab_2_t2/locations_years/' +
                str(year) + '.txt')
    markers = find_nearest(year, (latitude, longitude))
    shift = 0
    for line in markers:
        folium.Marker((line[1][0] + shift, line[1][1] + shift),
                      popup='<i>' + str(line[0])+'</i>').add_to(map_)
        shift += 0.001
    for j in capitals():
        folium.Marker(j, popup='<i>Capital</i>',
                      icon=folium.Icon(color='green')).add_to(map_)
    map_.save('Map_1.html')
    return None


def find_nearest(year, curent_cord):
    '''
    (int, tuple) -> list
    return list of nearest cordinates
    '''
    rez = []
    p1 = '/home/bogdan/Documents/1yr_2sm_lab/lab_2/'
    title = p1 + 'lab_2_t2/locations_years/' + \
        str(year) + '.txt'
    file = open(title)
    for line in file:
        line = line.strip().split('\t')
        rez.append(
            (line[0], (float(line[1].split()[0]), float(line[1].split()[1]))))
    rez.sort(key=lambda x: geodesic(x[1], curent_cord).miles)
    if len(rez) < 10:
        return rez
    else:
        return rez[0:10]


if __name__ == '__main__':
    try:
        data = read_data()
        get_map(data[0], data[1][0], data[1][1])
    except:
        print('No films')
