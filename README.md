# P4_ML_Project

## 项目简介
本项目实现了将机器学习模型（决策树和随机森林）部署到P4交换机，实现网络内的智能流量分类和检测。

## 目录结构
P4_ML_Project/
├── data/
│ ├── westermo_traffic.csv
├── models/
│ ├── decision_tree_model.pkl
│ ├── random_forest_model.pkl
├── src/
│ ├── data_preprocessing.py
│ ├── train_model.py
│ ├── generate_p4_code.py
│ ├── p4_program/
│ ├── decision_tree.p4
│ ├── decision_tree.json
├── test/
│ ├── mininet_test.py
├── README.md
└── requirements.txt