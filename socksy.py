import os
import json

from clarifai.rest import ClarifaiApp


APP_ID = '3584qKpSSfE0Y0DJworOQlOLIE8IDuOxehnOCPzj'
APP_SECRET = 'aQbYII5qdgVPIoqkD-jHVNFEnI3Lip-gvmyKXWb-'

app = ClarifaiApp(APP_ID, APP_SECRET)

moods = ['neutral', 'happy', 'angry', 'sleepy', 'surprised', 'smug']

cmodel = app.models.get('expressions')


def ctfaces():
    imgpath = [os.path.join(os.getcwd(), 'ctfaces')]
    imgs = []
    for img in os.listdir(imgpath[0]):
        imgs.append(img)
    return imgs, imgpath


def gtfaces():
    imgpath = [os.path.join(os.getcwd(), 'gtfaces')]
    imgs = []
    for dir in os.listdir(imgpath[0]):
        for img in os.listdir(os.path.join(imgpath[0], dir)):
            imgs.append(os.path.join(dir, img))
    return imgs, imgpath


def create(imgs, imgpaths):
    for img in imgs:
        for imgpath in imgpaths:
            print 'path ' + os.path.join(imgpath, img)
            app.inputs.create_image_from_filename(os.path.join(imgpath, img), concepts=[], not_concepts=[])


def gen_model():
    cmodel = app.models.create(model_id='expressions', concepts=moods)
    cmodel = cmodel.train()
    return cmodel


def predict():
    imgpath = os.path.join(os.getcwd(), 'dumpimg')
    preds = []
    for i, img in enumerate(os.listdir(imgpath)):
        pred = cmodel.predict_by_filename(os.path.join(imgpath, img))
        with open('dumpjson/face' + str(i) + '.json', 'w') as outfile:
            json.dump(pred, outfile, indent=4)
        with open('dumpjson/face' + str(i) + '.json') as contactfile:
            data = json.loads(contactfile.read())
        concepts = data['outputs'][0]['data']['concepts']
        for concept in concepts:
            preds.append((concept['id'], concept['value']))
    return preds


def evaluate(preds):
    moodvals = [0, 0, 0, 0, 0, 0]
    for pred in preds:
        for i, mood in enumerate(moods):
            if pred[0].encode('ascii', 'ignore') == mood:
                moodvals[i] = moodvals[i] + pred[1]
    print moodvals
    moodlist = []
    for i in range(len(moods)):
        moodlist.append((moods[i], moodvals[i]))
    return max(moodlist, key=lambda item: item[1])

print evaluate(predict())
