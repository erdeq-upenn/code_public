import argparse
import cfg
from network import East
from predict import predict
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import torch.utils.data
from torch.autograd import Variable
import os
from crnn import util
from crnn import dataset
from crnn.models import crnn
from crnn import keys
import cv2
import json
import pandas as pd

# This demo

def parse_args():
    """define the working dir"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p',
                        default='',
                        help='image path')
    parser.add_argument('--threshold', '-t',
                        default=cfg.pixel_threshold,
                        help='pixel activation threshold')
    return parser.parse_args()
def work(vnum):
    zh = []
    ocr = []
    for fla in tqdm(range(vnum)):
        try:
            cap.set(cv2.CAP_PROP_POS_FRAMES, fla)
            zh.append(fla)
            ret, frame = cap.read()
            image0 = predict(east_detect, frame, threshold)
            ocrstr = []
            n = 0
            for l, img in image0:
                n += 1
                image = img.convert('L')
                scale = image.size[1] * 1.0 / 32
                w = image.size[0] / scale
                w = int(w)
                # print(w)

                transformer = dataset.resizeNormalize((w, 32))
                image = transformer(image).cuda()
                image = image.view(1, *image.size())
                image = Variable(image)
                model.eval()
                preds = model(image)
                _, preds = preds.max(2)
                preds = preds.squeeze(-2)
                preds = preds.transpose(1, 0).contiguous().view(-1)
                preds_size = Variable(torch.IntTensor([preds.size(0)]))
                raw_pred = converter.decode(preds.data, preds_size.data, raw=True)
                sim_pred = converter.decode(preds.data, preds_size.data, raw=False)
                if len(image0) == 0:
                    ocr.append([fla,0])
                elif len(image0) == 1:
                    ocr.append([fla, all[l, sim_pred]])
                else:
                    ocrstr.append([l, sim_pred])
                    ocr.append([fla, ocrstr])
                # print(dict(zip(zh, ocr)))
                if len(zh) == int(cap.get(7)):
                    break
                    # focr = dict(zip(zh, ocr))
        except:
            pass
        continue

    return [ocr]


if __name__ == '__main__':
    """use pretrained weights and RNN model to run CV on cuda environement """
    args = parse_args()
    img_path = args.path
    threshold = float(args.threshold)

    east = East()
    east_detect = east.east_network()
    east_detect.load_weights(cfg.saved_model_weights_file_path)

    alphabet = keys.alphabet

    converter = util.strLabelConverter(alphabet)
    model = crnn.CRNN(32, 1, len(alphabet) + 1, 256, 1).cuda()
    path = './crnn/samples/netCRNN63.pth'
    model.load_state_dict(torch.load(path))
    videopath = '/home/username/PycharmProjects/videos/'
    finish = []
    for file in os.listdir('./result'):
        if file.endswith('.xlsx'):
            finish.append(file[:-5] + '.mp4')
    flag = 0
    for file in os.listdir(videopath):
        if file not in finish:
            flag += 1
            print('Processing the {} video...'.format(flag))
            size = os.path.getsize(videopath + file)
            if size == 0:
                zong = dict([("Video_Name", file[:-4]), ("Video_Time", 0), ("Total_Frames", 0),("Video_Ocr", 0)])
            else:
                clip = VideoFileClip(videopath + file)
                file_time = clip.duration
                cap = cv2.VideoCapture(videopath + file)
                vnum = int(cap.get(7))
                zong = dict([("Video_Name", file[:-4]), ("Video_Time", file_time), ("Total_Frames", vnum)])
                ocr = work(vnum)
                # focr = dict(zip(zh, ocr))
                print("focr:", ocr)
                zong["Video_Ocr"] = ocr

            df = pd.DataFrame(zong, index=[0])
            cols = ['Video_Name', 'Video_Time', 'Total_Frames', 'Video_Ocr']
            df = df.ix[:, cols]
            df.to_excel("./result/"+file[:-4]+".xlsx", index=False)
            df.to_hdf("./result/"+file[:-4]+".h5", "data")
            print(df.head())
