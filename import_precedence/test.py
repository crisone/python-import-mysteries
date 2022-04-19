import sys

def demo_1():
    sys.path.append("./folderb")
    sys.path.append("./foldera")

    print("* folder b is in front of folder a in sys path: ")
    import pkga.modulea
    pkga.modulea.hello()

    print("* modulefa can only be found in foldera/pkga: ")
    import pkga.modulefa

    pkga.modulefa.hello()

    print("* modulefb can only be found in folderb/pkga: ")
    import pkga.modulefb
    pkga.modulefb.hello()

    print("* pkga is treated as namespace instance, which can have multiple path")
    print("    pkga is ", sys.modules["pkga"])
    print("    pkga path is", sys.modules["pkga"].__path__)

    sys.path.remove("./folderb")
    sys.path.remove("./foldera")
    sys.modules.pop("pkga")
    sys.modules.pop("pkga.modulea")
    sys.modules.pop("pkga.modulefa")
    sys.modules.pop("pkga.modulefb")

def demo_2():
    sys.path.append("./folderb")
    sys.path.append("./folderc")

    print("* folder b is in front of folder c in sys path, but folderc/pkga is a package (have __init__.py) ")
    import pkga.modulea
    pkga.modulea.hello()

    print("* modulefb can not be found anymore, since pkga is locked as a package name in folderc: ")
    try:
        import pkga.moduleb_fb
        pkga.moduleb_fb.hello()
    except:
        print("    import pkga.moduleb_fb failed")
    print("    pkga is ", sys.modules["pkga"])
    print("    pkga path is", sys.modules["pkga"].__path__)

    print("* of course modulefc be normally imported now: ")
    import pkga.modulefc
    pkga.modulefc.hello()

    sys.path.remove("./folderb")
    sys.path.remove("./folderc")
    sys.modules.pop("pkga")
    sys.modules.pop("pkga.modulea")
    sys.modules.pop("pkga.modulefc")

def demo_3():
    sys.path.append("./foldera")

    print("* pkga.modulea from foldera can be normallay imported : ")
    import pkga.modulea
    pkga.modulea.hello()

    sys.path.insert(0, "./folderc")
    print("* folderc is added to sys path, but sys.modules['pkga'] is locked to namespace: ")
    try:
        import pkga.modulefc
        pkga.modulefc.hello()
    except:
        print("   ", "import pkga.modulefc failed")
        print("    pkga path is", sys.modules["pkga"].__path__)


if __name__ == "__main__":
    print("============ DEMO 1 ===========")
    demo_1()
    print("")

    print("============ DEMO 2 ===========")
    demo_2()
    print("")

    print("============ DEMO 3 ===========")
    demo_3()
    print("")