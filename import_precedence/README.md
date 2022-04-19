# Import Precedence

本目录演示了一些Python一些import优先级上的机制，正常项目中不应该碰到这么复杂的import关系，如果碰到了，想办法改目录名，尽量不要通过优先级关系来引入指定的模块，容易留下坑。

## 演示目录结构 

这段演示代码中包含三个目录，目录结构如下:

```bash
├── foldera
│   └── pkga
│       ├── modulea.py
│       └── moduleb_fa.py
├── folderb
│   └── pkga
│       ├── modulea.py
│       └── moduleb_fb.py
├── folderc
│   └── pkga
│       ├── __init__.py
│       ├── modulea.py
│       └── moduleb_fc.py
└── test.py
```

## Python Import搜索的基本流程

1. 首先在 sys.modules 这个字典中按照层级搜索，如果存在则直接引入module，如果不存在则在 sys.path 中按照顺序搜索


2. 在搜索中，含有__init__.py 的目录会被视为 NameSpace，不含的会被视为 Package，而Package 的搜索优先于 namespace，这一点上无视 sys.path 中的目录优先顺序，总体来说：
    - package 优先于 namespace
    - package之间或namespace 之间，以 sys.path 的先后次序决定优先级

3. 搜索到的目录会在 sys.modules 建立相应的 key 和 path 信息，下次如果再次import，遇到存储过的母 key，将会直接用 cache 中的 path 信息:

    如 `import pkga.moduleb`，如果 sys.modules 已经存在 `pkga` 的 key，则会在 `pkga['key'].__path__`下继续搜索 `moduleb`，此时即使 sys.path 中优先加入其他能找到 pkga.moduleb 的目录，也不会被搜索。


## 演示程序

运行
```bash
python3 test.py
```

正常输出
```bash
============ DEMO 1 ===========
* folder b is in front of folder a in sys path: 
    I am module A from ./folderb/pkga/modulea.py
* modulefa can only be found in foldera/pkga: 
    I am module FA from ./foldera/pkga/modulefa.py
* modulefb can only be found in folderb/pkga: 
    I am module FB from ./folderb/pkga/modulefb.py
* pkga is treated as namespace instance, which can have multiple path
    pkga is  <module 'pkga' (namespace)>
    pkga path is _NamespacePath(['./folderb/pkga', './foldera/pkga'])

============ DEMO 2 ===========
* folder b is in front of folder c in sys path, but folderc/pkga is a package (have __init__.py) 
    I am module A from ./folderc/pkga/modulea.py
* modulefb can not be found anymore, since pkga is locked as a package name in folderc: 
    import pkga.moduleb_fb failed
    pkga is  <module 'pkga' from './folderc/pkga/__init__.py'>
    pkga path is ['./folderc/pkga']
* of course modulefc be normally imported now: 
    I am module FC from ./folderc/pkga/modulefc.py

============ DEMO 3 ===========
* pkga.modulea from foldera can be normallay imported : 
    I am module A from ./foldera/pkga/modulea.py
* folderc is added to sys path, but sys.modules['pkga'] is locked to namespace: 
    import pkga.modulefc failed
    pkga path is _NamespacePath(['./foldera/pkga'])
```

## 备注
20220420的工作中踩到这个坑，对Python Import 机制有新的理解