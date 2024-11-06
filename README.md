# VoiceControlledChess
Project implementation for Soft Computing course.
## Problem Description
This project tackles the problem of playing chess where the plazer commands are given verbally in the Serbian language. Two neural networks are used for speech recognition, one for letters and the other for digits.
## Dataset
The data for the speech-recognizing neural networks were manuallz gathered and created specifically for this project. The dataset itself can be divided into two parts. Dataset where the data are numbers with classes 1-8 and another - letters with classes A-H. The first dataset counts 105 original audio records per class where the ratio of female and male voices is about 40:60. The dataset for letters contains slightly more recordings per class, i.e. 151 recordings with a similar ratio of male and female samples. Both datasets are strictly balanced and each class contains an equal number of elements. The expansion of the initial dataset was introduced by various augmentation procedures, described in detail in augmentations.py, which primarily consisted of adding different levels of background noise, changing pitch, speeding up, slowing down and boosting as needed (certain groups of recordings were of very low intensity and was amplified by 30db). After the augmentation procedure, the classes of the two datasets counted 1155 and 1661 elements, respectively, that is, the initial dataset was enlarged 11 times. The data obtained in this way was normalized and scaled to 128x128 pixels, considering the hardware limitation of the machine on which the test was performed (4 GB of memory on the graphics card).
## Agent Algorithm
Given that chess represents a zero-sum game, chosen agent algorithm was minimax with alpha-beta pruning. The need of evaluating a large number of positions for the minimax algorithm is imposed as a fundamental limitation in the agent's work, and in this sense a less complex heuristic function is implemented that takes into account the number and type of pieces on the board, as well as their position based of the type of the piece.

## Sound Modul
The module for working with sound includes the functionalities required for the recognition and classification of spoken chess fields (representing the input data), as well as functionalities for recording, further processing, manipulation, augmentation and model training.

## Setup and Start
In order to start the game, it is needed to install all the necessary dependencies from the requirements.txt file with the command ```pip install -r requirements.py```
After that, run ``python main.py`` command and select the level and algorithm. Finally, after the speech sign is displayed on the console, you should clearly say the field you are selecting (e.g. E2) with a small pause between voices. Then, after the network recognizes the selection, it is necessary to enter the destination in the same way.

## Documentation
The accompanying presentation as well as a demo of the application can be found in the "dokumentacija" folder.

## System Design

![Untitled](https://github.com/user-attachments/assets/8d78d3eb-dbab-4f83-be84-b96cc33207da)
