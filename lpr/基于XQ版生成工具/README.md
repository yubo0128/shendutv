# XQ版生成工具使用说明
1. 输入文件的病种名中如果包含Q，需要将Q替换为@。例如：QLXY 替换为 @LXY
2. 输入文件需要包含两个sheet，名称分别为"original sequences"、"element set"。
   1. "original sequences" 包含XQ版序列。表头需要包括'序号', 'title', '封面编号', 'XQ版本A', 'XQ版本正文'，'模块1', '模块2', '模块3', ...
   2. "element set" 包含"模块X"的替换项，可以互相替换的内容在同一行