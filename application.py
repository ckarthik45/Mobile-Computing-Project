from flask import Flask, request, jsonify
import werkzeug, os, cv2, requests
from keras.models import load_model
import numpy as np
app = Flask(__name__)


@app.route('/')
def index():
    return 'App with Python Flask!'
    
@app.route('/upload', methods=["POST"])
def upload():
    if request.method == "POST" :
        imagefile = request.files['image']
        # imageCategory = request.form['category']

        filename = werkzeug.utils.secure_filename(imagefile.filename)
        print("\nReceived image File name : " + imagefile.filename)

        imagefile.save(filename)
        # print(imagefile)
        image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (28,28))
        imagePart1 = image[:14,:14]
        imagePart2 = image[:14,14:]
        imagePart3 = image[14:,:14]
        imagePart4 = image[14:,14:]
        
        cv2.imwrite('imagePart1.png', imagePart1)
        cv2.imwrite('imagePart2.png', imagePart2)
        cv2.imwrite('imagePart3.png', imagePart3)
        cv2.imwrite('imagePart4.png', imagePart4)

        # model = load_model('deepLearningModel')

        # res = model.predict([image])[0]
        # number = np.argmax(res)

        data1 = {'image': open('imagePart1.png', 'rb')}
        data2 = {'image': open('imagePart2.png', 'rb')}
        data3 = {'image': open('imagePart3.png', 'rb')}
        data4 = {'image': open('imagePart4.png', 'rb')}

        r1 = requests.post("http://192.168.121.241:9001/upload", files = data1)
        r2 = requests.post("http://192.168.121.226:9002/upload", files = data2)
        r3 = requests.post("http://192.168.121.9:9003/upload", files = data3)
        r4 = requests.post("http://192.168.121.203:9004/upload", files = data4)

        number1 = r1.json()['number']
        print("Number predicted by first model is " + str(number1))
        number2 = r2.json()['number']
        print("Number predicted by second model is " + str(number2))
        number3 = r3.json()['number']
        print("Number predicted by third model is " + str(number3))
        number4 = r4.json()['number']
        print("Number predicted by fourth model is " + str(number4))

        list = [0] * 10
        list[number1] += 1
        list[number2] += 1
        list[number3] += 1
        list[number4] += 1

        number = list.index(max(list))

        os.remove("imagePart1.png")
        os.remove("imagePart2.png")
        os.remove("imagePart3.png")
        os.remove("imagePart4.png")

        path = str(number) + '/'

        if(os.path.exists(path)):
            os.rename(filename, path+filename)
            
        else:
            os.mkdir(path)
            os.rename(filename, path + filename)

        return jsonify({
            "message": "Image Uploaded Successfully ",
            "number": int(number),
        })

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=9000)
