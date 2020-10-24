import fastbook
from fastbook import *
from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import request
from flask import render_template
import datetime

fastbook.setup_book()

learn = load_learner("model.pkl")

app = Flask(__name__,template_folder='',
          static_folder='',
          root_path='/home/isen/ai-emotion-detection/flask',
          )

run_with_ngrok(app)   #starts ngrok when the app is run

def imageSetup(old):
  img_name = datetime.datetime.now().strftime("%f")+str(old)
  images_folder_server_path = "/home/isen/ai-emotion-detection/flask/images/"
  images_folder_web_path = "/images/"
  return img_name, os.path.join(images_folder_server_path,img_name), os.path.join(images_folder_web_path,img_name)

@app.route("/",methods=['GET', 'POST'])
def home():
    if request.method == "POST":
      image_file = request.files["image"]
      if image_file:
        image_name, image_path_server, image_path_web = imageSetup(image_file.filename)
        image_file.save(image_path_server)
        pred = learn.predict(image_path_server)
        print(pred)
        return render_template("result.html", imagePath=image_path_web, 
                               percent_angry=str("{:10.0f}".format(pred[2][0].item()*100)),
                               percent_disgust=str("{:10.0f}".format(pred[2][1].item()*100)),
                               percent_fear=str("{:10.0f}".format(pred[2][2].item()*100)),
                               percent_happy=str("{:10.0f}".format(pred[2][3].item()*100)),
                               percent_neutral=str("{:10.0f}".format(pred[2][4].item()*100)),
                               percent_sad=str("{:10.0f}".format(pred[2][5].item()*100)),
                               percent_surprise=str("{:10.0f}".format(pred[2][6].item()*100)),
                               )
    return render_template("file.html")

if __name__ == '__main__':
  app.run()