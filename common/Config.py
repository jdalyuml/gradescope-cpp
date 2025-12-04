import configparser
cfg = configparser.ConfigParser(inline_comment_prefixes=['#'])
cfg.read('Projects.cfg')

def ProjName():
    import os
    return os.environ['ASSIGNMENT_TITLE']

def ConfigFlag(setting: str):
    return cfg['Settings'].getboolean(setting)

def ConfigValue(setting: str):
    return cfg['Settings'].getfloat(setting)

def RunDiscernment():
    name = ProjName()
    separateTests = ConfigFlag('SeparateTestsAndImp')
    isTest = 'test' in name.lower()
    return isTest or not separateTests

def RunImp():
    name = ProjName()
    separateTests = ConfigFlag('SeparateTestsAndImp')
    isTest = 'test' in name.lower()
    return not isTest or not separateTests
