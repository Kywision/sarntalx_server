from PIL import Image
from classifier import Classifier

def main():
    img = Image.open('image1.jpg')
    detector = Classifier()
    detector.detect(img)

if __name__ == "__main__":
    main()