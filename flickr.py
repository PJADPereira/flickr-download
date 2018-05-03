import datetime
import urllib.request as getURL
import xml.etree.ElementTree as ET
import os
import sys

'''
A flicker class, that takes care of downloading photos through the flicker API and
saving the related info to a csv file. It takes three arguments as input photo_path which
is by default a folder named .Photos that the script will create if it has the proper 
permissions, the user api_key and the coordinates of the most extreme points of the box 
to download photos from.

The class has two internal methods:

    __get_photo_xml:
        builds a list with the xml of each of the photos retrieved from the flickr api
        that are present in the box provided. It uses the flickr.photos.search API method 
        and produces a list of all photos found in the area of interest.

        

    __run:
        calls __get_photo_xml to build the list of photos, goes through it and downloads 
        the photo and compiles the respective that in a file called results.csv
        
        It uses the flickr.photos.getInfo API method to get the data of interest and downloads
        the through the staticflickr. 


static methods:
    progress_bar:
        a simple progress bar to help users keep track of the work

        args: count(int), total(int)


'''


def progress_bar(count, total):

    p_bar_len = 50
    at_len = round(p_bar_len * (count / total))
    percent = round((100 * (count / total)))
    bar = "=" * at_len + "-" * (p_bar_len - at_len)
    sys.stdout.write('\r[%s]%s%s' % (bar, percent, '%'))


class Flickr(object):
    def __init__(self, photo_path, key, box):
        self.__photos = list()
        self.__key = key
        self.__box = box
        self.__run(photo_path)

    def __get_photo_xml(self):
        print("\n\nGathering photo list\n")
        page = 1
        total = 1
        count = 0
        while page <= total:
            progress_bar(count, total)

            photo_url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key="\
                        + self.__key + "&bbox=" + ",".join([str(x) for x in self.__box])\
                        + "&page=" + str(page) + "&sort= date-posted-asc"

            xml_file = getURL.urlopen(photo_url)
            xml_data = xml_file.read().decode()
            xml_file.close()

            rsp = ET.fromstring(xml_data)

            photo_set = rsp.getchildren()[0]
            total = int(photo_set.get('pages'))

            photos = rsp.findall('*/photo')
            for photo in photos:
                self.__photos.append(photo)

            count += 1
            page += 1
        progress_bar(total, total)
        print("\n")

    def __run(self, photo_path):

        self.__get_photo_xml()

        total = len(self.__photos)
        print("Downloading "+str(total)+" photos\n")
        with open("results.csv", "w")as out:
            out.write("Photo_ID\tPhoto_secret\tLatitude\tLongitude\tdate_posted\tdate_taken\n")
            count = 0
            for photo in self.__photos:
                progress_bar(count, total)
                p_id = photo.get("id")
                p_secret = photo.get("secret")
                p_farm = photo.get("farm")
                p_server = photo.get("server")

                photo_info_url = "https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key="\
                                 + self.__key + "&photo_id=" + str(p_id)

                photo_url = "https://farm" + p_farm + ".staticflickr.com/" + p_server + "/"\
                            + p_id + "_" + p_secret + ".jpg"

                xml_file = getURL.urlopen(photo_info_url)
                xml_data = xml_file.read().decode()
                xml_file.close()

                rsp = ET.fromstring(xml_data)
                for child in rsp[0]:

                    if child.tag == "location":
                        p_latitude = child.get('latitude')
                        p_longitude = child.get('longitude')

                    elif child.tag == "dates":
                        p_taken = child.get('taken')
                        p_posted = child.get('posted')

                out.write(str(p_id) + "\t" + str(p_secret) + "\t" + str(p_latitude) + "\t" + str(
                    p_longitude) + "\t" + datetime.datetime.fromtimestamp(int(p_posted)).strftime(
                    '%Y-%m-%d %H:%M:%S') + "\t" + str(p_taken) + "\n")

                photo_name = photo_path + p_id + ".jpg"
                getURL.urlretrieve(photo_url, photo_name)
                count += 1

            progress_bar(total, total)
            print("\n\n")
            
if __name__ == "__main__":

    if not os.path.isdir("./Photos"):
        os.makedirs("./Photos")
    if len(sys.argv) == 1 or len(sys.argv) < 3:
        print("No arguments provided in the command line please type them in following the provided description:")

        api_key = input("API key: ")

        nLat = float(input("Northern Latitude: "))
        sLat = float(input("Southern Latitude: "))
        wLon = float(input("Western Longitude: "))
        eLon = float(input("Eastern Longitude: "))

        bbox = [wLon, sLat, eLon, nLat]

    elif len(sys.argv) == 3:

        try:
            api_key = sys.argv[1]
            bbox = [float(x) for x in sys.argv[2].split(",")]

        except:
            print("Error: Coordinate inputs is badly formated")

    Flickr("./Photos/", api_key, bbox)
