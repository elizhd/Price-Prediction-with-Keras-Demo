import flask
import json
import numpy as np
from flask import Flask, render_template, request
from keras.models import load_model
from sklearn import preprocessing
import pandas as pd
from pyecharts import Line

app = Flask(__name__)


@app.route("/")
@app.route("/pricePredictor")
def index():
    return flask.render_template('pricePredictor.html')


@app.route("/predict", methods=['POST'])
def returnData():
    line = drawLine()
    return render_template(
        'predictResult.html',
        myechart=line.render_embed(),
        host='http://chfw.github.io/jupyter-echarts/echarts',
        script_list=line.get_js_dependencies())


def drawLine():
    pred, Y, datelist = make_predictions()
    line = Line(
        width=1200,
        height=600,
    )
    line.add(
        "预测价格",
        datelist,
        pred,
        is_fill=True,
        line_width=3,
        line_opacity=0.5,
        # yaxis_min=0,
        # yaxis_max=5.5,
        is_toolbox_show=True,
        is_more_utils=True,
        is_datazoom_show=True,
        datazoom_type="both",
        datazoom_range=[0, 100],
    )
    line.add(
        "真实价格",
        datelist,
        Y,
        is_fill=True,
        line_width=3,
        line_opacity=0.5,
        # yaxis_min=0,
        # yaxis_max=5.5,
        is_toolbox_show=True,
        is_more_utils=True,
        is_datazoom_show=True,
        datazoom_type="both",
        datazoom_range=[0, 100],
    )
    return line


def make_predictions():
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        datelist = pd.date_range(startDate, endDate)
        datelist = [x.strftime('%Y-%m-%d') for x in datelist]

        # 载入数据集
        df = pd.read_csv('./data/dataset_wx_web.csv', index_col='date')
        X_data = df.iloc[:, 0:-1]
        Y_data = df['price'].values.reshape(-1, 1)
        scaler_X = preprocessing.StandardScaler(
            copy=True, with_mean=True, with_std=True).fit(X_data)
        scaler_Y = preprocessing.StandardScaler(
            copy=True, with_mean=True, with_std=True).fit(Y_data)

        df = df.loc[startDate:endDate]
        X = scaler_X.transform(df.iloc[:, 0:-1])
        Y = scaler_Y.transform(df['price'].values.reshape(-1, 1))
        pred = model.predict(X)
        pred = scaler_Y.inverse_transform(pred)
        pred = pred.flatten()
        Y = scaler_Y.inverse_transform(Y).flatten()

        return pred, Y, datelist


if __name__ == '__main__':
    model = load_model('./best_model_tanh/model.hdf5')
    print('----test model: ', model.predict(np.array([[0, 0, 0, 0, 0, 0]])))
    print('----test done.')
    app.run(host='127.0.0.1', port=8001, debug=True)
