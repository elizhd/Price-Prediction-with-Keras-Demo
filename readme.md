# Price Prediction with Keras Demo
使用Tensorflow Kera API进行价格预测 使用模型为简单的DNN模型

## 实现功能
1. 爬虫 使用BeautifulSoup4,爬取了全国农产品商务信息公共服务平台的价格数据 (网址为http://nc.mofcom.gov.cn/channel/jghq2017/price_list.shtml),没有使用多线程,速度很慢
2. 数据处理 所有价格数据存入mysql数据库,根据需求取出数据,使用pandas处理取出的数据
3. 预测模型 简单的DNN模型
4. 数据展示 网页部分，使用了bootstrap前端框架，后端使用flask框架和pyechart库进行数据图表的展现。

## 界面
1. 表单
    ![表单](https://github.com/ErGouBigDevil/Price-Prediction-with-Keras-Demo/blob/master/img/index.jpg)
2. 预测界面
    ![预测](https://github.com/ErGouBigDevil/Price-Prediction-with-Keras-Demo/blob/master/img/prediction.jpg)

