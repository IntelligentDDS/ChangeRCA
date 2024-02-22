# ChangeRCA

This repository is the basic implementation of our publication in FSE'24 conference paper [ChangeRCA: Finding Root Causes from Software Changes in Large Online Systems](https://yuxiaoba.github.io/publication/changerca24/changerca24.pdf)

## Description

In large-scale online service systems, the occurrence of software changes is inevitable and frequent. Despite rigorous pre-deployment testing practices, the presence of defective software changes in the online environment cannot be completely eliminated. We propose a novel concept called `root cause change analysis (RCCA)` to identify the underlying root causes of change-inducing incidents. In order to apply the RCCA concept to practical scenarios, we have devised an intelligent RCCA framework named `ChangeRCA`. 

## Quick Start

### Requirements 

- Python3.9 is recommended to run the anomaly detection. Otherwise, any python3 version should be fine.
- Git is also needed.
- Linux OS

### Setup

Download `ChangeRCA` first via `git clone git@github.com:IntelligentDDS/ChangeRCA.git`

Enter `ChangeRCA` content by `cd ChangeRCA` 

`python3 -m pip install -r requirements.txt` to install the dependency for ChangeRCA

### Running
```
$ python3 main.py
[INFO]2023-09-26 03:07:00,667 main.py:78: case_number:51
[INFO]2023-09-26 03:07:00,667 main.py:81: -------------------Change Task Top1 score------------------
[INFO]2023-09-26 03:07:00,667 main.py:83: HR@1:0.8823529411764706
[INFO]2023-09-26 03:07:00,667 main.py:86: -------------------Change Task Top3 score------------------
[INFO]2023-09-26 03:07:00,667 main.py:88: HR@3:1.0
[INFO]2023-09-26 03:07:00,667 main.py:91: -------------------Change Task Top5 score------------------
[INFO]2023-09-26 03:07:00,667 main.py:93: HR@5:1.0
[INFO]2023-09-26 03:07:00,667 main.py:96: -------------------Change Task MAR Result------------------
[INFO]2023-09-26 03:07:00,667 main.py:97: 1.1372549019607843
```

The results will be printed and recorded in `./log`

## Dataset 

OnlineBoutique dataset is available at [./data](./data/README.md)

## Reference
```
@inproceedings{yu2024changerca,
  title={ChangeRCA: Finding Root Causes from Software Changes in Large Online Systems},
  author={Yu, Guangba and Chen, Pengfei and He, Zilong and Yan, Qiuyu and Luo, Yu and Li, Fangyuan and Zheng, Zibin},
  booktitle={Proc. ACM Softw. Eng. 1},
  pages={1--23},
  year={2024}
}     
```

