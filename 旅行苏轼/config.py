import os

#api
DEEPSEEK_API_KEY = "enter your api here"
API_URL = "https://api.deepseek.com/chat/completions"
#图片
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR,"assets")
IMG_LOBBY = os.path.join(ASSETS_DIR,"lobby_bg.png")
IMG_MAP = os.path.join(ASSETS_DIR, "map.png")
IMG_MEIZHOU = os.path.join(ASSETS_DIR,"meizhou.png")
IMG_SCROLL = os.path.join(ASSETS_DIR, "scroll.png")
#基础颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
PURPLE = (128, 0, 128)

# 天空/水
SKY_BLUE = (135, 206, 235)
DEEP_BLUE = (0, 105, 148)
OCEAN_BLUE = (0, 119, 190)

# 大地/石头
BROWN = (139, 69, 19)
SAND = (244, 164, 96)
STONE_GRAY = (128, 128, 128)
SLATE_GRAY = (112, 128, 144)

# 植物
FOREST_GREEN = (34, 139, 34)
GRASS_GREEN = (124, 252, 0)
OLIVE = (128, 128, 0)
MOSS = (173, 223, 173)

# 木头
WOOD = (156, 102, 68)
DARK_WOOD = (101, 67, 33)
LIGHT_WOOD = (205, 170, 125)

# 暖色
WARM_WHITE = (255, 244, 229)
CREAM = (255, 253, 208)
PEACH = (255, 218, 185)
TERRACOTTA = (204, 114, 67)
BRICK = (178, 85, 53)

# 宣纸颜色
XUAN_PAPER = (245, 235, 210)
OLD_PAPER = (230, 215, 180)
INK_BLACK = (30, 30, 30)

# 青铜/古物
BRONZE = (205, 127, 50)
COPPER = (184, 115, 51)
RUST = (183, 65, 14)

# 墨色系
INK_LIGHT = (80, 80, 80)
INK_MEDIUM = (50, 50, 50)
INK_DARK = (20, 20, 20)

# 玉石
JADE_GREEN = (64, 145, 108)
MOSS_JADE = (99, 139, 101)

#暗色
DREAM_BLUE = (200, 220, 255)
NIGHT_BLUE = (25, 25, 112)
DUSK = (84, 103, 143)
FOG = (220, 230, 240)

# 场景背景色
BANSHANYUAN = (200, 230, 200)  # 半山园绿
CHAOTANG = (150, 100, 50)      # 朝堂棕
ZHONGSHAN = (100, 150, 200)    # 钟山蓝
NEISHI = (200, 180, 150)       # 内室暖

# 物品颜色
STONE = (128, 128, 128)
BOOK = (205, 170, 125)
MEDICINE = (150, 50, 150)

# 宋体/新宋体系列
SIM_SUN = "C:/Windows/Fonts/simsun.ttc"           # 宋体/新宋体
SIM_SUN_BOLD = "C:/Windows/Fonts/simsunb.ttf"     # 新宋体粗体
NSIM_SUN = "C:/Windows/Fonts/nsimsun.ttf"         # 新宋体

# 黑体系列
SIM_HEI = "C:/Windows/Fonts/simhei.ttf"           # 黑体
MICROSOFT_YAHEI = "C:/Windows/Fonts/msyh.ttc"     # 微软雅黑
MICROSOFT_YAHEI_BOLD = "C:/Windows/Fonts/msyhbd.ttc"  # 微软雅黑粗体

# 楷体系列
SIM_KAI = "C:/Windows/Fonts/simkai.ttf"           # 楷体
KAI_TI = "C:/Windows/Fonts/kaiti.ttf"             # 楷体（另一种）

# 仿宋系列
SIM_FANG = "C:/Windows/Fonts/simfang.ttf"         # 仿宋
FANG_SONG = "C:/Windows/Fonts/fangsong.ttf"       # 仿宋（另一种）

# 隶书/幼圆
LI_SU = "C:/Windows/Fonts/simli.ttf"              # 隶书
YOU_YUAN = "C:/Windows/Fonts/simyou.ttf"          # 幼圆

# 华文系列
ST_SONG = "C:/Windows/Fonts/stsong.ttf"           # 华文宋体
ST_HEI = "C:/Windows/Fonts/stheiti.ttf"           # 华文黑体
ST_KAI = "C:/Windows/Fonts/stkaiti.ttf"           # 华文楷体
ST_FANG = "C:/Windows/Fonts/stfangsong.ttf"       # 华文仿宋
ST_YAHEI = "C:/Windows/Fonts/msyahei.ttf"         # 华文雅黑

# 书法类
LI_SHUTI = "C:/Windows/Fonts/ls.ttf"              # 隶书体
XINGKAI = "C:/Windows/Fonts/xingkai.ttf"          # 行楷
CAOSHU = "C:/Windows/Fonts/caoshu.ttf"            # 草书（如果有）
ZHUANSHU = "C:/Windows/Fonts/zhuanshu.ttf"        # 篆书（如果有）

# 艺术类
HUA_WEN_CAI_YUN = "C:/Windows/Fonts/HYCuYun.ttf"  # 华文彩云
HUA_WEN_XING_KAI = "C:/Windows/Fonts/hwxingkai.ttf" # 华文行楷
HUA_WEN_LI_SHU = "C:/Windows/Fonts/hwlisu.ttf"    # 华文隶书

print("fonts is executable")
print("colors is executable")
