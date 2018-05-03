A flicker class, with the porpuse of download every photo inside a given geographic box. It does so using the flickr API (more info in the docstring on the flicker.py file). It takes three arguments as input photo_path which is by default a folder named .Photos that the script will create if it has the proper permissions, the user api_key and the coordinates of the most extreme points of the box to download photos from.

This script is as used in Vaz et al., 2018 (in prep)

<h3>Requirements:</h3>
This script only works in Python 3.x and was tested and run in Python 3.5. No external dependencies should be required to run.

<h3>How to use:</h3>

  1)  Download or clone the script (flickr.py) into a working folder.

  2)  The flickr.py script expects two arguments to be passed through the command line:
      <p>my_api_key: The API key that you receive when you sign in in flickr;</p>
      <p>coordinates: Four coordinate values separated by commas, be sure to keep it in the
      order provided below:</p>
      
        <p>&emsp;Westernmost Longitude of the box</p>
        <p>&emsp;Southermost Latitude of the box</p>
        <p>&emsp;Easternmost Longitude of the box</p>
        <p>&emsp;Northermost Latitude of the box</p>
          
  
  
<h3>Examples:</H3>
      
      
  ```
  python3 flickr.py my_api_key -8.42670,41.653104,-7.754076,42.083595
  ```
      
  Alternatively, the script can be launched without passing any arguments, and they can be provided during runtime:
  
  ```
  python3 flickr.py
  ```
      
      
  
    
