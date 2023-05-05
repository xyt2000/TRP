# TRP
## 文件目录
    │  .gitignore
    │  LICENSE
    │  README.md
    ├─data
    │  ├─reports 
    ├─data_process
    │  │  cilin.txt
    │  │  data_divide.py
    │  │  dict_synonym.txt
    │  │  downloadImage.py
    │  │  stop_words.txt
    │  │  text_processing.py
    │  └─RapidOCR
    │      └─python
    │          │  OCR.py
    ├─early_data
    │  │  fill_zero.py
    │  ├─autoencoder
    │  ├─fillzeroAE
    │  ├─min-max
    │  ├─pca
    │  └─pca_minmax
    ├─evaluate
    │  │  apfd.py
    │  │  draw.py
    ├─fusion
    │  ├─early
    │  │  │  autoencoder.py
    │  │  │  PCA.py
    │  │  │  write_min_max.py
    │  │  └─dbm-master
    │  │          dbm_3layer.py
    │  └─late
    │          late_fusion.py
    ├─image_feature
    │  │  feature_OCR.py
    │  │  feature_ssim.py
    │  │  feature_vgg19.py
    │  ├─CEDD
    │  │  │  CEDD.jar
    │  │  │  feature_cedd.py
    │  │  └─Lire-1.0b4
    │  │          │  ├─java
    │  │          │  │  └─net
    │  │          │  │      └─semanticmetadata
    │  │          │  │          └─lire
    │  │          │  │              │  CEDDTest.java
    │  ├─GIST
    │  │  │  feature_gist.py
    │  ├─SIFT
    │  │      orb.py
    │  │      SIFT.py
    │  │      SURF.py
    │  └─SPM
    │      │  feature_spm.py
    ├─model
    ├─output
    ├─pipeline
    │  │  earlyfusion_ae.py
    │  │  earlyfusion_pca.py
    │  │  earlyfusion_sim.py
    │  │  fileUtils.py
    │  │  image_pipeline.py
    │  │  latefusion_pipeline.py
    │  │  ocr_test_which_best.py
    │  │  text_pipeline.py
    ├─  prioritization
    │  │  additional.py
    │  │  art.py
    │  │  ideal.py
    │  │  rdm.py
    ├─  text_feature
    │  │  data.model
    │  │  distance.py
    │  │  feature_bert.py
    │  │  feature_bm25.py
    │  │  feature_doc2vec.py
    │  │  feature_edit_Levenshtein.py
    │  │  feature_edit_manhattan.py
    │  │  feature_one_hot_sequence.py
    │  │  feature_one_hot_word.py
    │  │  feature_tfidf.py
    │  │  feature_tfidf_update.py
    │  │  feature_topic_lda.py
    │  │  feature_topic_lsi.py
    │  │  feature_word2vec.py
    │  │  pipeline.py
