## VAD效果测试

这个项目用来直接体验vad效果

### add wav head

`add_wav.py` 用来给pcm添加wav头，文件查看数据

修改源码里的路径，可以指定文件夹

### 测试vad

安装依赖

```
pip3 install -r requirements.txt
```

执行测试

```
python3 vadtest.py
```

会遍历文件夹，对所有`.wav`文件进行测试。

下面功能通过源码修改：

* SHOW_UI: 控制是否显示界面，用来显示音频文件、vad端点，以及播放音频
* wav_dir: 要遍历测试的文件夹，文件名带 `.wav` 后缀的文件，才会被测试
* output_dir: 测试结果会保存到该文件夹，命名为`result.csv`