# TRP
## 文件目录
    │  .gitignore
    │  LICENSE
    │  README.md
    ├─data
    │  ├─reports 众包测试报告数据
    ├─data_process 数据预处理
    │  │  cilin.txt 同义词库
    │  │  data_divide.py 根据（执行流程和错误描述）划分众包测试报告的文字部分
    │  │  dict_synonym.txt 修改的同义词库
    │  │  downloadImage.py 下载众包测试报告的图像部分到本地
    │  │  stop_words.txt 停止词
    │  │  text_processing.py 文字预处理（分词+去除停用词+同义词替换）
    │  └─RapidOCR
    │      └─python
    │          │  OCR.py OCR提取报告图片中的文字
    ├─early_data 早期融合的向量数据
    │  │  fill_zero.py 给特征向量补0适配自动编码器
    │  ├─fillzeroAE 使用自动编码器融合向量
    │  ├─min-max 归一化
    │  ├─pca pca后的向量
    │  └─pca_minmax pca+归一化
    ├─evaluate 评估
    │  │  apfd.py 计算APFD
    │  │  draw.py 绘制缺陷检测效率图
    ├─fusion 特征融合
    │  ├─early 早期融合
    │  │  │  autoencoder.py 自动编码器
    │  │  │  PCA.py 主成分分析
    │  │  │  write_min_max.py 归一化
    │  │  └─dbm-master  深度玻尔兹曼机
    │  │          dbm_3layer.py
    │  └─late
    │          late_fusion.py 晚期融合（字典序+平均排序）
    ├─image_feature 图像特征提取
    │  │  feature_OCR.py OCR特征提取
    │  │  feature_ssim.py SSIM特征提取
    │  │  feature_vgg19.py VGG特征提取
    │  ├─CEDD
    │  │  │  CEDD.jar
    │  │  │  feature_cedd.py CEDD特征提取
    │  │  └─Lire-1.0b4
    │  │          │  ├─java
    │  │          │  │  └─net
    │  │          │  │      └─semanticmetadata
    │  │          │  │          └─lire
    │  │          │  │              │  CEDDTest.java CEDD对应的java文件
    │  ├─GIST
    │  │  │  feature_gist.py GIST特征提取
    │  ├─SIFT
    │  │      orb.py ORB特征提取
    │  │      SIFT.py SIFT特征提取
    │  │      SURF.py SURF特征提取
    │  └─SPM
    │      │  feature_spm.py SPM特征提取
    ├─model 模型
    │      │  chinese_L-12_H-768_A-12 中文bert预训练模型
    ├─output 提取的特征向量数据
    ├─pipeline
    │  │  earlyfusion_ae.py  基于自动编码器的早期融合的报告排序
    │  │  earlyfusion_pca.py 基于主成分分析的早期融合的报告排序
    │  │  earlyfusion_sim.py 基于相似度融合的早期融合 的报告排序
    │  │  fileUtils.py 文件处理
    │  │  image_pipeline.py 基于单一图像特征的报告排序
    │  │  latefusion_pipeline.py 基于晚期融合的报告排序
    │  │  ocr_test_which_best.py 针对OCR数据哪一个文字特征提取方法最好
    │  │  text_pipeline.py 基于单一文字特征的报告排序
    ├─  prioritization 排序算法
    │  │  additional.py 额外贪心算法
    │  │  art.py 自适应随机测试算法
    │  │  ideal.py 理想排序
    │  │  rdm.py 随机排序
    ├─  text_feature 文本特征提取
    │  │  data.model
    │  │  distance.py 距离函数
    │  │  feature_bert.py BERT特征提取
    │  │  feature_bm25.py bm25特征提取
    │  │  feature_doc2vec.py doc2vec特征提取
    │  │  feature_edit_Levenshtein.py 基于字符Levenshtein距离的特征提取
    │  │  feature_edit_manhattan.py 基于字符曼哈顿距离的特征提取
    │  │  feature_one_hot_sequence.py one_hot_sequence特征提取
    │  │  feature_one_hot_word.py one_hot_word特征提取
    │  │  feature_tfidf.py tfidf特征提取
    │  │  feature_tfidf_update.py 修改的tfidf特征提取
    │  │  feature_topic_lda.py lda特征提取
    │  │  feature_topic_lsi.py lsi特征提取
    │  │  feature_word2vec.py word2vec特征提取
## 使用方法

**step1: 预处理**

data_process/RapidOCR/python/OCR.py 

提取报告中图片的文字信息：

    输入：data/reports
    
    输出：output/

data_process/text_processing.py

预处理报告的文字信息（文字描述+图片的文字信息）

    文字描述      输入：data/reports
                 输出：data/reports
    图片的文字信息 输入：data/reports
                 输出：output/

**step2: 文本特征提取并基于单一文本特征进行报告排序(RQ1)**

pipeline/text_pipeline.py

（注意提取BERT特征需要下载chinese_L-12_H-768_A-12并放到model文件夹下
运行bert-serving-start -model_dir 模型地址 -num_worker=1）

**step3: 图像特征提取并基于单一图像特征进行报告排序(RQ1)**

pipeline/image_pipeline.py（注意该文件直接是根据特征进行报告排序 特征提取参考image_feature的readme）

**step4: 选择特征融合方式融合特征进行报告排序(RQ2 & RQ3)**

注意所有的前端融合均是使用已有的数据，前后端融合部分的实现代码可见fusion/early 和 fusion/late
其中基于深度波尔茨曼机的融合在fusion/early/dbm-master，因为表现不稳定 本文未使用该方法。

pipeline/earlyfusion_ae.py

pipeline/earlyfusion_pca.py

pipeline/earlyfusion_sim.py

pipeline/latefusion_pipeline.py

**step5:评估排序效果**

evaluate/draw.py 评估排序效果，绘制相应图像
