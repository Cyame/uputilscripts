## 中->日文本转换器

为中文台本添加假名注记。

### 如何使用

1. 配置
    修改`script/language-notator/rules.yml`中`output-rule`字段以改变输出模式
    
    > 如果您希望自定义注记映射或添加自定义字段，亦可以在此修改。
    
    如果您认为当前版本的语音库存在映射上的不准确或错误，欢迎协助本项目开发。您可以通过[提交Issues](https://github.com/Cyame/uptuilscripts/issues)来进行反馈或**提交Pull Request**来提交您的修改。

2. 运行
    ```
    $ python script/language-notator/notation.py <txt文件>
    ```
    会自动在你的工作目录中生成对应文件
### 未来计划

- 添加片假名及罗马音支持
- 添加拼音支持
- 添加现代化Excel(.xlsx)、文字注音(.doc/docx)以及MarkDown等模式支持
- 修正已知的括号与`\n`会造成文本部分错乱的问题

### 更新日志

- Version 1.0
  
  完成语音语料库，提供Excel支持，正确显示日文假名注记

- Version 1.1
  
  完成中文与假名注记对应，支持两种模式的TXT文本生成