# masonry
Inception model retrained to recognize construction site images

## Dependencies

Masonry uses the following packages:
  1. Image library creation:
      * http
      * urllib
      * time
      * imagehash
      * PIL
  Usage of fix_jpeg.sh requires that ImageMagick be installed on the system.

  2. Retraining Inception and Image Classification
      * Tensorflow
      * Numpy

  3. Training the simple CNN and Image Classification
      * Keras
      * Tensorflow
      * Numpy
      * Scikit Learn
    
  4. Visualization of Model Performance
      * Matplotlib
      * Numpy
      * Scikit Learn
      
## Image library creation

### Image search and download
Retrieve bing image search results by running `create_im_lib.py`:

```
python create_im_lib.py <api-key> <query> <count> <offset> [<output-dir> (optional)]
```
* `<api-key>` is the API key to access Bing Image search. [Get a 30-day free
  trial key](https://azure.microsoft.com/en-us/try/cognitive-services/?api=bing-image-search-api).
* `<query>` is the search string to use to fetch images.
* `<count>` is the number of images to fetch.
* `<offset>` is the offset in the search results to start retrieving images.
(That is, skip the first `<offset>` images in the result.)
* `<output-dir>` is the location to save the image files. If omitted, save
  in the current directory. Images are saved with the filename
  `img_###.jpeg`.
  
The image library should contain one subdirectory per image class. The subdirectory name should be the name of the image class, as in the example below:

```
      img_lib/
            bulldozer/
                img_000.jpeg
                img_001.jpeg
                ...
            excavator/
                img_000.jpeg
                img_001.jpeg
                ...
```
### Removal of incompatible image formats
Non-JPEG images can be removed from the image library directory by running `fix_jpeg.sh`

### Removal of duplicate images
Removal of duplicates is important for correctly assessing model performance. Duplicate images can be removed with `detect_duplicates.py`:

```
python detect_duplicates.py <root-dir>
```
* `<root-dir>` is the parent directory containing the images  
___
## Retraining Inception v3

The Inception model can be downloaded and retrained with `retrain_kfold.py`:

```
python retrain_kfold.py --logdir ~/img_lib 
```
The `--logdir` flag must be used to specify the location of the parent directory of the image library. Additional command line arguments for retraining the model are:
  * `--kfold`: Number of stratified train and test splits for model training and cross-validation. Default is 10. 
  * `--num_runs`: Number of runs to perform training and cross-validation
  * `--learning_rate`: Learning rate for calculating the gradient. `retrain_kfold.py` uses a Stochastic Gradient Descent optimizer.
  
  **Command line arguments for specifying output directories, using image distortion, etc. are commented in `retrain_kfold.py`**
___
## Training a simple CNN from scratch

The simple CNN has 3 convolutional layers with ReLU activation and 2x2 MaxPool. These layers are followed by a 128 neuron fully connected layer with ReLU activation and 50% dropout. The output layer contains 8 neurons with softmax activation. 

![architecture](simple_cnn/simple_cnn_arch.png)

A simple CNN can be built and trained with `simple_cnn.py`:

```
python simple_cnn.py <img_dir> <img_width> <img_height>
```
  * `<img_dir>`: the parent directory containing images for training and validation
  * `<img_width>`: the width of the images in the library
  * `<img_height>`: the height of the images in the library
  
  The `<img_width>` and `<img_height>` arguments will be used to specify the dimensions of the expected input to the first layer of the model. `simple_cnn.py` splits the data in `<img_dir>` into 10-fold training and validation sets. The model is trained for 15 epochs. Model checkpoints are created after each epoch in which the validation accuracy increases. Training progress can be monitored with TensorBoard when pointed to the `./logs` directory that is created when the script is executed.
  
  

