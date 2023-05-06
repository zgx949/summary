# 自动摘要Bilibili视频内容项目

该项目是一个基于chatgpt的自动摘要Bilibili视频内容的开源项目。该算法将视频中的语音转换为文本，并使用自然语言处理技术对文本进行摘要，以提供用户精简的视频概述。

体验地址：http://bi.lefthand.top/

## 安装

1. 下载代码到本地
2. 创建虚拟环境并激活
3. 使用pip安装依赖项 `pip install -r requirements.txt`
4. 运行程序 `python main.py`
5. 将 `.env.template` 文件重命名为 `.env`
6. 填写api-key

## 使用

1. 🎈运行程序后输入Bilibili视频链接
2. 🚦程序会自动下载视频并将语音转换为文本❌（实际上是爬取字幕🤭）
3. 🔥摘要结果将在控制台打印出来

## 技术细节

该项目使用了以下技术：

- 🔠[pydub](http://pydub.com/)：用于音频处理❌
- 💬[speech_recognition](https://pypi.org/project/SpeechRecognition/)：用于语音识别❌
- 💻[you-get](https://github.com/soimort/you-get)：用于从Bilibili下载视频❌
- 🧛‍♂️字幕爬取
- 📱ChatGPT
- ⚡API接口：[AI智能工具箱](https://www.aiznx.com/#/)

## 注意

本项目对接的接口是[AI智能工具箱](https://www.aiznx.com/#/)，其APIKEY是从该网站中充值获得。请自行购买key（可以修改请求接口参数，每天都有免费使用的额度）



## 贡献

欢迎参与贡献该项目！可以通过以下方式：

1. 在GitHub上提交问题和bug报告
2. 提交Pull Request来改进代码

## 授权

该项目使用MIT开源许可证，详情请查看[LICENSE]()文件。

------

<div align="center">如果您喜欢该项目，请不要吝啬您的Star。谢谢!</div>

<p align="center"> <a href="https://github.com/zgx949/summary"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"></a>   <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>   <a href="https://pypi.org/project/SpeechRecognition/"><img src="https://img.shields.io/pypi/v/SpeechRecognition.svg?style=for-the-badge&color=informational&label=SpeechRecognition"></a>   </p>