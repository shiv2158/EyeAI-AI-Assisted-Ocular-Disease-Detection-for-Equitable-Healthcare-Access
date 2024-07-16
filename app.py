import os
import uuid
import flask
import urllib
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask , render_template  , request , send_file
from tensorflow.keras.preprocessing.image import load_img , img_to_array

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'SGModelBIN.hdf5'))


ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

classes = ['Diabetic retinopathy', 'Age-related macular degeneration', 'Media haze', 'Drusen', 'Myopia', 'Branch retinal vein occlusion', 'Tessellation', 'Epiretinal membrane', 'Laser scars', 'Macular scars', 'Central serous retinopathy', 'Optic disc cupping', 'Central retinal vein occlusion', 'Tortuous vessels', 'Asteroid hyalosis', 'Optic disc pallor', 'Optic disc edema', 'Optociliary shunt', 'Anterior ischemic optic neuropathy', 'Parafoveal telangiectasia', 'Retinal traction', 'Retinitis', 'Chorioretinitis', 'Exudation', 'Retinal pigment epithelium changes', 'Macular hole', 'Retinitis pigmentosa', 'Cotton-wool spots', 'Coloboma', 'Optic disc pit maculopathy', 'Preretinal hemorrhage', 'Myelinated nerve fibers', 'Hemorrhagic retinopathy', 'Central retinal artery occlusion', 'Tilted disc', 'macular edema', 'Post-traumatic choroidal rupture', 'Choroidal folds', 'Vitreous hemorrhage', 'Macroaneurysm', 'Vasculitis', 'Branch retinal artery occlusion', 'Plaque', 'Hemorrhagic pigment epithelial detachment', 'Collateral']

"""
def predict(filename , model):
    img = load_img(filename , target_size = (150 , 150))
    img = img_to_array(img)
    img = img.reshape(1 , 150 ,150 ,3)
    img = img.astype('float32')
    img = img/255.0
    result = model.predict(img)

    dict_result = {}
    for i in range(45):
        dict_result[result[0][i]] = classes[i]

    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:3]
    
    prob_result = []
    class_result = []
    for i in range(3):
        prob_result.append((prob[i]*100).round(2))
        class_result.append(dict_result[prob[i]])

    return class_result , prob_result
"""
def predict(filename , model):
    img = load_img(filename , target_size = (150 , 150))
    img = img_to_array(img)
    img = img.reshape(1 , 150 ,150 ,3)
    img = img.astype('float32')
    img = img/255.0
    result = model.predict(img)
    print(result[0][0])
    dict_result = {}
    #for i in range(45):
    #    dict_result[result[0][i]] = classes[i]
    dict_result[result[0][0]] = "Diseased Retina"
    dict_result[1-result[0][0]] = "Healthy Retina"
    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:3]
    
    prob_result = []
    class_result = []
    #for i in range(45):
    #    prob_result.append((prob[i]*100).round(2))
    #    class_result.append(dict_result[prob[i]])
    prob_result.append((prob[0]*100).round(2))
    class_result.append(dict_result[prob[0]])
    prob_result.append(((1-prob[0])*100).round(2))
    class_result.append(dict_result[(1-prob[0])])
    return class_result , prob_result


@app.route('/')
def home():
        return render_template("index2.html")

@app.route('/success' , methods = ['GET' , 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd() , 'static/images')
    if request.method == 'POST':
        if(request.form):
            link = request.form.get('link')
            try :
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img , filename)
                output = open(img_path , "wb")
                output.write(resource.read())
                output.close()
                img = filename

                class_result , prob_result = predict(img_path , model)

                predictions = {
                      "class1":class_result[0],
                      "class2":class_result[1],
                      "prob1": prob_result[0],
                      "prob2": prob_result[1],
                }

            except Exception as e : 
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                return render_template('index2.html' , error = error) 

            
        elif (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename

                class_result , prob_result = predict(img_path , model)

                predictions = {
                      "class1":class_result[0],
                      "class2":class_result[1],
                      "prob1": prob_result[0],
                      "prob2": prob_result[1],
                }

            else:
                error = "Please upload images of jpg, jpeg, and png files only."

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                return render_template('index2.html' , error = error)

    else:
        return render_template('index2.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


