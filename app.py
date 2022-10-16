from flask import Flask, render_template, request, jsonify
from search import search
from caption import predict
import os
from PIL import Image
from ib64 import image_to_base64
app = Flask(__name__, template_folder="templateFiles", static_folder="static")

#This is just for testing purpose
@app.route("/hello")
def hello():
  return "Hello World!"

@app.route("/", methods=["GET", "POST"])
def land():
    if request.method=="GET":
      return render_template("test.html");
    if request.method=="POST":
      recievedFile = request.files['fileUpload']
      print('File Recieved')
      if recievedFile.filename != '':
            recievedFile.save( str(recievedFile.filename))
            image_path =  str(recievedFile.filename) 
            search_query = predict(image_path) 
            print(search_query) # this is the caption
            os.remove(image_path) # remove the image from the server
            lt = search(search_query) # this is the list of images
            lt = [image_to_base64(Image.open(f"artifacts/{photo_id}.jpg")) for photo_id in lt] # convert the images to base64
            for i in range(len(lt)):
              lt[i]=str(lt[i])
            for i in range(len(lt)):
              x=''
              for j in range(len(lt[i])-5):
                if j<2:
                  continue
                x+=str(lt[i][j])
              lt[i]=x
            return render_template("img.html", img=lt) 
            #str(lt) # return the list of images
      else:
            return "No file recieved"

#Driver Code
if __name__ == "__main__":
  app.run()