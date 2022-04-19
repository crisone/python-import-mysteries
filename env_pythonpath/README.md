# PythonPath 环境变量

正常情况下，Python运行时，会自动读取环境变量 PYTHONPATH 中的路径，并加入到 sys.path 的正前方，但有些情况下可能引入难以意料的错误

## PYTHONPATH 中出现 空字符

如
```
export PYTHONPATH="/aaa/bb::/cc"
```
有时候，由于对字符串拼接处理不当，导致出现 两个冒号 连在一起，这样的 PYTHONPATH 会导致 python 中加入额外的 sys.path（指向当前执行程序的目录)，有时候会产生难以预料的后果

### 真实出现过的案例
bazel的py_binary会自动生成执行脚本和 runfiles，执行脚本中会添加 PYTHONPATH 环境变量指向 runfiles 下的目录，此时如果本机环境中还有额外的PYTHONPATH，可能会导致非 runfiles 下的 module 被找到，产生奇怪的问题

### 演示
```
bash ./test.sh
```
