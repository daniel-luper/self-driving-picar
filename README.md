# Self-Driving Picar
Code for a Raspberry Pi Model B self-driving car (heavily modified version of [picar](https://github.com/lawsonkeith/picar)).

<img src=https://media.giphy.com/media/U2RDbvwigNaMPm3HtQ/giphy.gif width=640 height=360>

## How it works
### Components
* Raspberry Pi Model B
* GETIHU Power Bank BG-120
* HP Webcam HD-4110
* Ovonic 11.1V 2200mAh Lipo Battery (yes, it's overkill)
* L298N H-bridge motor controller
* 4-Wheel Drive Yellow Robot Smart Car Chassis

### Artificial Intelligence
The car uses image recognition to determine which direction the car should go in (left, right, or straight).
It is built to stay on a track made with two lines of black duct tape.

To teach the car to drive, I captured 20,000 images of me controlling the car with my phone.
From this data, I trained a deep neural network with [Keras](https://keras.io/).

## Getting started
### Prerequisites
Install Node.js on your Raspberry Pi

```sudo apt-get install -y nodejs```

Install node modules on your Raspberry Pi

```npm install zerorpc socket.io node-static```

Install python libraries on your Raspberry Pi

```pip3 install zerorpc opencv-python tensorflow numpy```

Install [Python](https://www.python.org/downloads/) (with pip) on your Windows PC

Install python libraries on your Windows PC

```pip install opencv-python tensorflow numpy```

### Setting up the car
1. Build a car using the same (or similar) [components](#components)
2. Set the pi's hostname in ```hostname.txt```
3. Move files from ```pi_code``` to your Raspberry Pi (under ```Documents/sdc/```)

```.\upload_to_pi.bat```

4. Make the scripts executable
```chmod u+x manual.sh auto.sh record.sh```

## Usage
### Driving
Run the following script on the Pi to drive in "manual" mode

```./manual.sh```

or in "auto" mode

```./auto.sh```

or in "record" mode

```./record.sh```

Then navigate to ```[raspberry-pi-ip-address]:8080/socket.html``` on your phone's web browser. 

Example link: ```http://192.168.1.106:8080/socket.html```

Wait a few seconds for everything to initialize... and enjoy!

### Recording your own training and testing data

                                                                File to run
    1. Modify 'constants.txt' if necessary                  |   ---------------
    2. Clear 'train_data/' of all files                     |   ---------------
    3. Record raw data on pi                                |   record.sh
    4. Download raw data from pi                            |   update_data.bat
    5. Process data                                         |   process_data.py
    6. Add processed data to training data                  |   merge_data.py
    7. Repeat steps 3-6 until training data is full         |   ---------------
    8. Duplicate and flip training data                     |   flip.py
    9. Repeat steps 2-8, but this time for test data        |   ---------------

### Training your own neural network
1. Download and unzip the [dataset](https://www.dropbox.com/s/qi5x0g04etvrbe5/dataset.zip?dl=0) or use your own
2. Put training data under ```train_data``` and testing data under ```test_data```
3. Edit the hyperparameters in ```train.py```
4. Train the neural network:
```python train.py```

## License
[MIT](LICENSE.md)
