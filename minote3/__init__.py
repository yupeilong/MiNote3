from airscript.system import R
from airscript.ui import Window
from airscript.action import click  # 导入click包
from airscript.node import Selector  # 导入Selector包
from airscript.action import key  # 导入Key包
from airscript.action import slide  # 导入slide包
from airscript.action import touch  # 导入touch包
from ascript.android import action  # 导入action包
from ascript.android.ui import Screen  # 导入Screen包
from ascript.android import node  # 导入node包
from ascript.android.screen import Ocr  # 谷歌OCR 识别中文,并使用自动分割
from ascript.android.screen import FindImages  # 导入FindImages包
from airscript.action import gesture  # 导入gesture包
from airscript.action import path  # 导入path包
from airscript.ui.dialog import alert  # 导入alert包
from airscript.ui.dialog import toast  # 导入toast包
from ascript.android.screen import FindColors # 导入FindColors包
from ascript.android.system import Clipboard
from datetime import datetime
from ascript.android.ui import FloatWindow
import time
import random
import json
import re
import os
import tempfile

# # 添加计数器变量
# publish_count = 0

# 模拟随机延迟
def random_delay(min_delay=2, max_delay=4):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
    print(f"模拟延迟: {delay:.2f} 秒")


# 模拟随机鼠标移动到控件
def move_to_node_simulation(node_selector):
    offset_x = random.uniform(-5, 5)  # 随机偏移，模拟人类鼠标移动不精确
    offset_y = random.uniform(-5, 5)
    print(f"移动到节点位置，模拟偏移: ({offset_x:.1f}, {offset_y:.1f})")
    random_delay(0.2, 0.6)  # 模拟鼠标移动延迟


# 模拟点击控件
def click_node_simulation(node_selector):
    node = node_selector.find()
    move_to_node_simulation(node)
    random_delay(0.1, 0.3)  # 模拟点击前的停顿
    print(f"点击控件: {node}")
    node_selector.click().find()  # 实际点击操作


# 等待并查找控件
def wait_for_node(node_selector, timeout=45):
    start_time = time.time()
    attempts = 0

    while time.time() - start_time < timeout:
        node = node_selector.find()  # 使用传入的 Selector 查找节点
        if node:
            print(f"找到控件: {node}")
            return node

        attempts += 1
        random_delay(0.4, 1.0)  # 随机间隔模拟人为的操作速度

        if attempts % 5 == 0:
            print(f"轮询次数: {attempts}")

    raise TimeoutError(f"等待超过 {timeout} 秒，控件仍未找到")

def slide_simulation(min_slides=3, max_slides=5, duration_range=(280,320), direction='up'):
    screen_width = 1080  # 手机屏幕宽度
    screen_height = 1920  # 手机屏幕高度
    # 随机选择滑动次数
    num_slides = random.randint(min_slides, max_slides)
    print(f"我要滑动({num_slides})次")

    for _ in range(num_slides):
        start_x = random.randint(screen_width * 0.4, screen_width * 0.6)
        if direction == 'up':
            start_y = random.uniform(1540, 1560)  # 从屏幕底部的60%到70%区域滑动
            end_y = random.uniform(1390, 1410)  # 滑动到屏幕的50%到60%区域
        elif direction == 'down':
            start_y = random.uniform(1390, 1410)  # 从屏幕中间滑动
            end_y = random.uniform(1540, 1560)  # 到屏幕底部60%到70%区域停止
        else:
            print(f"未知的滑动方向: {direction}")
            return
        print(f"我从{start_x, start_y}开始滑到{start_x, end_y}")
        duration = random.uniform(*duration_range)
        slide(start_x, start_y, start_x, end_y)
        random_delay(3, 6)

# 模拟人为输入的函数
def simulate_human_typing(node_selector, text_input, max_retries=3, timeout=10):
    for retry in range(max_retries):
        try:
            # 使用 wait_for_node 等待控件出现
            node = wait_for_node(node_selector, timeout)
            if node:
                print(f"找到控件: {node}，准备输入文本: {text_input}")
                click_node_simulation(node_selector)  # 首先点击输入框
                node.input(text_input)  # 对控件执行输入操作
                return node  # 返回找到并输入文本的节点
        except TimeoutError:
            print(f"超时未找到控件，开始第 {retry + 1} 次重试...")
            random_delay(1, 1.5)  # 模拟人为的暂停后重试

            if retry == max_retries - 1:
                print(f"最大重试次数 {max_retries} 已达到，控件未找到")
                raise TimeoutError("没有找到可以输入的地方")


def process_images(flag, max_retries=10):
    """
    处理图片，通过滑动屏幕并截图
    :param max_retries: 判断第一张图片时的最大重试次数
    """
    # 获取屏幕中心坐标
    # screenSize = Selector().type("WebView").text("商品信息").find()
    # centerX = screenSize.rect.centerX()
    # centerY = screenSize.rect.centerY()

    # 判断是否为第一张图片
    isFirst = Ocr.mlkitocr_v2(rect=[506,75,574,130], pattern='1')

    retries = 0
    while not isFirst and retries < max_retries:
        print(f"当前不是第一张图片，向左滑动... (尝试次数: {retries + 1})")
        slide(540, 960, 1140, 960, 300)
        random_delay()
        isFirst = Ocr.mlkitocr_v2(rect=[506,75,574,130], pattern='1')
        retries += 1

    if not isFirst:
        print(f"未能找到第一张图片，达到最大重试次数 {max_retries} 次")
        raise TimeoutError(f"未能找到第一张图片，达到最大重试次数 {max_retries} 次")

    # 获取当前时间戳
    timestamp = int(time.time())

    # 截图第一张图片并使用时间戳命名
    print("当前是第一张图片，开始截图...")
    image1 = Screen.toFile(f"/sdcard/DCIM/Screenshots/first_image_{timestamp}.png", Screen.bitmap(0, 423, 1080, 1500))
    print(f"第一张图片截图保存到: {image1}")

    # 滑动到第二张图片
    random_delay()
    slide(540, 960, 140, 960, 500)
    random_delay()

    # 再次获取时间戳以命名第二张图片
    timestamp = int(time.time())

    # 截图第二张图片
    print("滑动到第二张图片，开始截图...")
    image2 = Screen.toFile(f"/sdcard/DCIM/Screenshots/second_image_{timestamp}.png", Screen.bitmap(0, 423, 1080, 1500))
    print(f"第二张图片截图保存到: {image2}")

    # 如果是要过剪映AI，则需要保存5张图片
    if flag:
        # 滑动到第三张图片
        random_delay()
        slide(540, 960, 140, 960, 500)
        random_delay()

        # 再次获取时间戳以命名第三张图片
        timestamp = int(time.time())

        # 截图第三张图片
        print("滑动到第三张图片，开始截图...")
        image3 = Screen.toFile(f"/sdcard/DCIM/Screenshots/second_image_{timestamp}.png", Screen.bitmap(0, 423, 1080, 1500))
        print(f"第三张图片截图保存到: {image3}")

        # 滑动到第四张图片
        random_delay()
        slide(540, 960, 140, 960, 500)
        random_delay()

        # 再次获取时间戳以命名第四张图片
        timestamp = int(time.time())

        # 截图第四张图片
        print("滑动到第四张图片，开始截图...")
        image4 = Screen.toFile(f"/sdcard/DCIM/Screenshots/second_image_{timestamp}.png", Screen.bitmap(0, 423, 1080, 1500))
        print(f"第四张图片截图保存到: {image4}")

        # 滑动到第五张图片
        random_delay()
        slide(540, 960, 140, 960, 500)
        random_delay()

        # 再次获取时间戳以命名第五张图片
        timestamp = int(time.time())

        # 截图第五张图片
        print("滑动到第五张图片，开始截图...")
        image5 = Screen.toFile(f"/sdcard/DCIM/Screenshots/second_image_{timestamp}.png", Screen.bitmap(0, 423, 1080, 1500))
        print(f"第五张图片截图保存到: {image5}")

    return True

def video_find():
    # 最大滑动次数限制
    max_attempts = 5
    attempt_count = 0

    # 通过 OCR 查找"视频"
    videoLocation = Ocr.mlkitocr_v2(rect=[18, 189, 965, 311], pattern='视频')

    # 如果找不到视频，执行滑动操作直到找到"视频"或达到最大滑动次数
    while not videoLocation and attempt_count < max_attempts:
        print(f"我找不到视频，当前滑动次数: {attempt_count + 1}")

        # 查找 HorizontalScrollView 以便进行滑动操作
        videoFind = Selector().type("HorizontalScrollView").find()

        if videoFind:
            # 随机化滑动操作，模拟人为滑动
            startX = videoFind.rect.centerX() + random.randint(-20, 20)
            startY = videoFind.rect.centerY() + random.randint(-20, 20)
            endX = startX + random.randint(280, 320)
            endY = startY

            # 滑动操作，随机化滑动时长
            slide(startX, startY, endX, endY, random.randint(250, 350))

            # 等待随机时间，模拟人工操作
            random_delay()

            # 滑动后再次通过 OCR 查找"视频"
            videoLocation = Ocr.mlkitocr_v2(rect=[18, 189, 965, 311], pattern='视频')

            # 增加滑动次数计数
            attempt_count += 1
        else:
            print("未找到 HorizontalScrollView 控件")
            break  # 如果找不到滑动控件，直接退出

    # 查找结束后，点击"视频"位置
    if videoLocation:
        for l in videoLocation:
            print(f"找到'视频'位置: x={l.x}, y={l.y}")
            click(l.x, l.y)
    else:
        print(f"达到最大滑动次数 {max_attempts} 次，仍未找到'视频'")


# 通过等待图片出现，继续下一步操作，不出现则轮询
def wait_for_pic(pic, timeout=45, interval=0.1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        path = R(__file__).res(pic)  # 这里替换为你的图片地址
        res = FindImages.find(path, confidence=0.95)
        if res:
            print(f"找到该图片: {res}")
            return res
        time.sleep(interval)
        print(interval)  # 输出轮询次数
    raise TimeoutError(f"等待的时间超过 {timeout} 秒，控件仍未找到")


def wait_for_nopic(nopic, timeout=45, interval=0.1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        path = R(__file__).res(nopic)  # 这里替换为你的图片地址
        res = FindImages.find(path, confidence=0.95)
        if not res:
            print(f"找不到该图片: {res}")
            return res
        time.sleep(interval)
        print(interval)  # 输出轮询次数
    raise TimeoutError(f"等待的时间超过 {timeout} 秒，控件仍未找到")


# 定义一个清除应用函数
def clearApp():
    key.home()
    random_delay()
    key.recents()
    try:
        # mi3清除app
        clearBtn = wait_for_node(Selector().id("com.android.systemui:id/clearAnimView"), timeout=45)
        click_node_simulation(Selector().id("com.android.systemui:id/clearAnimView"))  # 点击清除按钮
    except TimeoutError as e:
        print(e)
    random_delay()


# 定义一个锁住app函数
def lockApp(appName, appNode):
    key.home()
    random_delay()
    click_node_simulation(Selector().desc(appName).type("RelativeLayout")) # 点击进入AScript，为了确保锁定app时该app处在第一个位置
    wait_for_node(Selector().text(appNode), timeout=45)
    key.home()
    random_delay()
    key.recents()
    random_delay()
    isLock = Selector().desc(appName + ",已加锁").find()
    if not isLock:
        element = wait_for_node(Selector().text(appName), timeout=45)
        Selector().desc(appName + ",未加锁").long_click().find()
        random_delay
        click_node_simulation(Selector().desc("锁定任务"))
        random_delay()
    else:
        print("我已经被锁定了")

def videoInKuaishou(title):
    # 搜索素材
    findSearch = wait_for_node(Selector().desc("查找").id("com.smile.gifmaker:id/nasa_featured_default_search_view"), timeout=45)
    click_node_simulation(Selector().desc("查找").id("com.smile.gifmaker:id/nasa_featured_default_search_view")) # 点击放大镜
    simulate_human_typing(Selector().type("EditText"), title) # 输入标题
    random_delay()
    click_node_simulation(Selector().text("搜索")) # 点击搜索按钮
    random_delay()

    # 使用文字识别功能来点击该文字中点位置
    video_find()  # 找到视频按钮
    findVideoWrap = wait_for_node(Selector().id("com.smile.gifmaker:id/container"), timeout=45)
    random_delay()
    slide_simulation(1, 2)
    random_delay()
    click_node_simulation(Selector().type("RelativeLayout").visible(True).id(
        "com.smile.gifmaker:id/container"))  # 点击进入视频素材
    findShare = wait_for_node(Selector().id("com.smile.gifmaker:id/forward_count").visible(True),
                            timeout=45)
    click_node_simulation(
        Selector().id("com.smile.gifmaker:id/forward_count").visible(True).parent(1))  # 点击分享按钮
    findCopy = wait_for_node(Selector().text("复制链接"), timeout=45)
    click_node_simulation(Selector().text("复制链接").parent(1))  # 点击复制链接按钮
    findCopyed = wait_for_pic("img/copyed.png", timeout=45)
    random_delay()
    clearApp()

def videoInDouyin(title):
    findDouYin = wait_for_node(Selector().desc("抖音"), timeout=60)
    click_node_simulation(Selector().desc("抖音"))
    # findMagnifier = wait_for_node(Selector().desc("搜索").type("Button"), timeout=45)
    findShareButton = wait_for_node(Selector().desc("关注").visible(True), timeout=45)
    # slide_simulation()
    # random_delay()
    click_node_simulation(Selector().desc("搜索").type("Button"))
    findSearchBox = wait_for_node(Selector().type("EditText"), timeout=45)
    Selector().type("EditText").input(title).find()
    random_delay()
    searchButton = Selector().text("搜索").find()
    click(searchButton.rect.centerX(), searchButton.rect.centerY())
    findVideoButton = wait_for_node(Selector().text("视频").type("Button"), timeout=45)
    click_node_simulation(Selector().text("视频").type("Button").parent(1))
    random_delay()
    isVideoShow = wait_for_node(Selector().type("RecyclerView").visible(True).child(1).child(1), timeout=45)
    random_delay()
    click_node_simulation(Selector().type("RecyclerView").visible(True).child(1).child(1))
    findShareButton = wait_for_node(Selector().desc("关注").visible(True), timeout=45)
    random_delay()
    slide_simulation(2, 4)
    random_delay()
    findShareBtn = Selector().desc("关注").visible(True).brother(0.5).find()
    click(findShareBtn.rect.centerX(), findShareBtn.rect.centerY())
    findShareLink = wait_for_node(Selector().text("分享链接"), timeout=45)
    click_node_simulation(Selector().text("分享链接").parent(1))
    random_delay()
    findCopySuccess = wait_for_node(Selector().text("复制链接"), timeout=45)
    random_delay()
    clearApp()

def douyinCrack(title):
    print("我跑破解版抖音")
    # title = "薰衣草花香洗衣液深层去污去渍柔顺护衣持久留香洗衣液家庭大桶装"
    findDouyin = wait_for_node(Selector().text("抖音"), timeout=45)
    click_node_simulation(Selector().text("抖音").parent(1))
    random_delay(3, 5)
    findSearchBtn = wait_for_node(Selector().desc("搜索，按钮"), timeout=45)
    attempt_count = 0
    while True and attempt_count < 3:
        findAdult = Selector().text("青少年模式").find()
        findLogin = Selector().text("抖音登录").find()
        if findAdult:
            print("我找到了青少年模式")
            click_node_simulation(Selector().text("我知道了").type("Button"))
            break
        elif findLogin:
            print("我找到了抖音登录")
            click_node_simulation(Selector().desc("关闭，按钮"))
            break
        attempt_count += 1
        print(f"我尝试查找青少年模式提示和登录提示第({attempt_count})次")
        random_delay(1, 2)
    random_delay()
    click_node_simulation(Selector().desc("搜索，按钮").parent(1))
    findSearchBox = wait_for_node(Selector().type("EditText"), timeout=45)
    simulate_human_typing(Selector().type("EditText"), title)
    random_delay()
    searchButton = Selector().text("搜索").find()
    click(searchButton.rect.centerX(), searchButton.rect.centerY())
    findVideoButton = wait_for_node(Selector().text("视频").type("Button"), timeout=45)
    click_node_simulation(Selector().text("视频").type("Button").parent(1))
    random_delay()
    isVideoShow = wait_for_node(Selector().type("RecyclerView").visible(True).child(1).child(1), timeout=45)
    random_delay()
    click_node_simulation(Selector().type("RecyclerView").visible(True).child(1).child(1))
    findShareButton = wait_for_node(Selector().desc("关注").visible(True), timeout=45)
    random_delay()
    slide_simulation(2, 4)
    random_delay()
    touch.down(540, 960)
    time.sleep(1)
    touch.up(540, 960)
    findDownBtn = wait_for_node(Selector().text("无水印下载"), timeout=45)
    click_node_simulation(Selector().text("无水印下载"))
    random_delay()
    # 判断“无水印下载”控件是否仍然存在，如果存在则继续等待，直到消失
    start_time = time.time()
    attempts = 0
    while True and time.time() - start_time < 180:
            if not Selector().text("无水印下载").find():
                print("“无水印下载”控件已消失，下载完成！")
                break  # 控件消失，退出循环
            else:
                print("“无水印下载”控件仍然存在，继续等待...")
                time.sleep(1)  # 每隔1秒检查一次
            attempts += 1
            random_delay(0.4, 1.0)  # 随机间隔模拟人为的操作速度

            if attempts % 5 == 0:
                print(f"轮询次数: {attempts}")
    random_delay()
    clearApp()

def removeInTk():
    # 使用TK去水印
    findTk = wait_for_node(Selector().desc("TK去水印"), timeout=45)
    click_node_simulation(Selector().desc("TK去水印"))  # 进入去水印软件

    # 粘贴链接
    findPaste = wait_for_node(Selector().text("粘贴").parent(1).clickable(True), timeout=45)
    click_node_simulation(Selector().text("粘贴").parent(1).clickable(True))  # 点击粘贴按钮
    random_delay()

    # 更换接口
    findParse = wait_for_node(Selector().text("接口一 ⇋").parent(1), timeout=45)
    click_node_simulation(Selector().text("接口一 ⇋").parent(1))  # 更换接口
    
    findParse = wait_for_node(Selector().type("ScrollView").child(2), timeout=45)
    click_node_simulation(Selector().type("ScrollView").child(2))  # 选择端口
    
    # 解析视频
    findParse = wait_for_node(Selector().text("解析"), timeout=45)
    click_node_simulation(Selector().text("解析"))  # 点击解析按钮
    # 最大查找次数限制
    max_attempts = 3
    attempt_count = 0
    isParseError = Selector().text("解析失败：105").find()
    while isParseError and attempt_count < max_attempts:
        print(f"我找到解析失败，当前查找次数: {attempt_count + 1}")
        click_node_simulation(Selector().text("确定"))
        attempt_count += 1
        random_delay()
        findNoParsing = wait_for_nopic("img/parsing.png", timeout=45)
        isParseError = Selector().text("解析失败：105").find()

    findSavingVideo = wait_for_node(Selector().text("保存视频"), timeout=45)
    if not isParseError:
        if not findSavingVideo:
            findParse = wait_for_node(Selector().text("解析"), timeout=45)
            click_node_simulation(Selector().text("解析"))  # 点击解析按钮
            findNoParsing = wait_for_nopic("img/parsing.png", timeout=45)
    else:
        raise TimeoutError(f"达到最大查找次数 {max_attempts} 次，仍有105报错")

    # 保存视频
    findSavingVideo = wait_for_node(Selector().text("保存视频"), timeout=45)
    click_node_simulation(Selector().text("保存视频"))  # 点击保存视频
    random_delay(3.5, 5.5)

    # 清除应用
    findNoSaving = wait_for_nopic("img/saveing.png", timeout=120)
    print("我已经保存好了")
    clearApp()

def removeInQh():
    """
    使用青禾去水印App去除视频水印
    包含:等待加载、粘贴链接、提取下载等操作
    """
    try:
        # 进入青禾去水印
        findQh = wait_for_node(Selector().text("青禾去水印"), timeout=45)
        click_node_simulation(Selector().text("青禾去水印"))
        
        # 点击去水印入口
        findRemove = wait_for_node(Selector().desc("短视频去水印").parent(1), timeout=45)
        click_node_simulation(Selector().desc("短视频去水印").parent(1))
        
        # 确保【视频】选项被勾选
        findVideo = wait_for_node(Selector().text("视频").clickable(True), timeout=45)
        videoCheckbox = Selector().text("视频").clickable(True).brother(1).brother(1).find()
        if not videoCheckbox.checked:
            click_node_simulation(Selector().text("视频").clickable(True).brother(1).brother(1))
        
        # 使用touch模拟长按指定区域
        print("开始长按指定区域...")
        touch.down(524, 624)  # 长按区域的中心点 (89+960)/2=524, (446+803)/2=624
        time.sleep(2)  # 长按2秒
        touch.up(524, 624)    # 在同一位置松开
        
        # 等待并点击粘贴按钮
        Selector().desc("粘贴").clickable(True).click().find()
        random_delay()

        # 提取视频
        print("开始提取视频...")
        findTk = wait_for_node(Selector().text("提取").parent(1).clickable(True), timeout=45)
        click_node_simulation(Selector().text("提取").parent(1).clickable(True))
        
        # 增加等待时间
        print("等待提取完成...")
        random_delay(8, 10)  # 增加等待时间到8-10秒
        
        # 点击下载按钮
        print("点击下载按钮...")
        click(522, 1700)  # 使用准确的下载按钮坐标
        random_delay(2, 3)
        
        # 等待下载完成
        print("等待下载完成...")
        findNoSaving = wait_for_nopic("img/saveing.png", timeout=120)
        toast("视频保存成功～～", 5000)
        
    except TimeoutError as e:
        toast(f"去水印失败: {str(e)}", 5000)
        raise
    finally:
        print("清理应用...")
        clearApp()

def removeInWeb():
    # 使用网页去水印
    findWebRemove = wait_for_node(Selector().text("短视频去水印解析-全网短视频解析下载"), timeout=45)
    click_node_simulation(Selector().text("短视频去水印解析-全网短视频解析下载"))
    findInput = wait_for_node(Selector().hintText("请将APP里复制的视频链接粘贴到这里"), timeout=45)
    pasteLocation = Selector().hintText("请将APP里复制的视频链接粘贴到这里").find()
    touch.down(pasteLocation.rect.centerX(), pasteLocation.rect.centerY())
    time.sleep(1)
    touch.up(pasteLocation.rect.centerX(), pasteLocation.rect.centerY())
    findPaste = wait_for_node(Selector().desc("粘贴"), timeout=45)
    click_node_simulation(Selector().desc("粘贴"))
    random_delay()
    click_node_simulation(Selector().text("解析视频").type("Button"))
    findVideoHelper = wait_for_node(Selector().desc("视频助手"), timeout=45)
    click_node_simulation(Selector().desc("视频助手"))
    findDownloadBtn = wait_for_node(Selector().id("com.huawei.hisurf.webview:id/hw_media_video_assistant_download"), timeout=45)
    click_node_simulation(Selector().id("com.huawei.hisurf.webview:id/hw_media_video_assistant_download"))
    findAlert = wait_for_node(Selector().id("android:id/alertTitle"), timeout=45)
    click_node_simulation(Selector().id("android:id/button1"))
    findDownSuccess = wait_for_node(Selector().text("文件下载完成").id("com.android.browser:id/download_tips"), timeout=120)
    toast("我保存好视频啦～～", 5000)
    random_delay()
    clearApp() 

# 点击进入快手
def click_kuaishou_icon(counter_data):
    # 查找快手图标
    findApp = Selector().text("^快手$").find_all()
    
    # 确保至少找到两个图标
    if len(findApp) >= 2:
        if counter_data % 2 == 0:
            print(f"counter_data: {counter_data}, 点击了第一个快手图标")
            findApp[0].parent(1).click()  # 点击第一个图标
        else:
            print(f"counter_data: {counter_data}, 点击了第二个快手图标")
            findApp[1].parent(1).click()  # 点击第二个图标
    else:
        print("未找到足够的快手图标，尝试点击进入快手")
        # 如果找不到两个图标，执行以下操作
        findApp = wait_for_node(Selector().desc("^快手$").type("RelativeLayout"), timeout=45)
        click_node_simulation(Selector().desc("^快手$").type("RelativeLayout"))

# 固定的计数器文件路径
counter_file_path = '/storage/emulated/0/airscript/data/counter.json'
print(f"我是计数器文件路径：{counter_file_path}")
# 加载计数器数据
def load_counter():
    try:
        with open(counter_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 如果文件不存在，返回初始计数器值
        return {"counter": 0, "last_reset_date": str(datetime.now().date())}

# 保存计数器数据
def save_counter(counter_data):
    with open(counter_file_path, 'w', encoding='utf-8') as f:
        json.dump(counter_data, f)

def reset_counter_if_new_day():
    # 每天 0:00 重置计数器
    current_date = str(datetime.now().date())
    counter_data = load_counter()

    if counter_data["last_reset_date"] != current_date:
        counter_data["counter"] = 0
        counter_data["last_reset_date"] = current_date
        save_counter(counter_data)
        print(f"计数器已重置为 0，日期：{current_date}")

def increment_counter():
    # 加载计数器并增加计数
    counter_data = load_counter()
    counter_data["counter"] += 1
    save_counter(counter_data)
    print(f"计数器值增加1")

def simulate_publish_video():
    # 模拟发布视频后调用
    reset_counter_if_new_day()
    increment_counter()
    # 输出当前计数器状态（模拟查看当前计数器）
    counter_data = load_counter()
    print(f"当前计数器值：{counter_data['counter']}, 最后重置日期：{counter_data['last_reset_date']}")
    toast(f"发布成功！今日已发布{counter_data['counter']}条视频", 5000)

def clear_kuaishou_cache():
    # 需要清理的快手缓存路径（包括多开路径）
    kuaishou_paths = [
        '/storage/emulated/0/Android/data/com.smile.gifmaker',
        '/storage/emulated/999/Android/data/com.smile.gifmaker'
    ]
    
    # 可删除的文件扩展名
    clearable_extensions = ['.tmp', '.log', '.cache', '.dat', '.temp', '.apk', 
                            '.mp4', '.jpg', '.png', '.json', '.gif', '.webp']

    """ 遍历所有子目录，删除符合扩展名的文件 """
    for path in kuaishou_paths:
        if not os.path.exists(path):
            print(f"⚠ 目录不存在：{path}")
            continue

        print(f"📂 开始清理目录：{path}")

        # 遍历所有文件和子目录
        for root, dirs, files in os.walk(path):
            print(f"📂 正在扫描目录：{root}")

            for file in files:
                file_path = os.path.join(root, file)
                # 如果文件符合可删除扩展名，则删除
                if any(file.endswith(ext) for ext in clearable_extensions):
                    try:
                        os.remove(file_path)
                        print(f"✅ 已删除文件：{file_path}")
                    except Exception as e:
                        print(f"❌ 删除失败：{file_path} - 错误：{e}")

        print(f"🎉 {path} 目录清理完成！")

# 清理相册中的图片和视频
def clear_album():
    # 相册存储路径
    picture_path = '/storage/emulated/0/Pictures'
    dcim_path = '/storage/emulated/0/DCIM'

    # 定义要删除的文件类型
    clearable_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.mp4', '.avi', '.mov', '.mkv']

    for path in [picture_path, dcim_path]:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if any(file.endswith(ext) for ext in clearable_extensions):
                        try:
                            os.remove(file_path)
                            print(f"已删除文件：{file_path}")
                        except Exception as e:
                            print(f"删除失败：{file_path} - 错误：{e}")
        else:
            print(f"目录 {path} 不存在。")
    
    print("相册清理完成。")

def clear_capcut_cache():
    # 需要清理的剪映缓存路径
    capcut_paths = [
        '/storage/emulated/0/Android/data/com.lemon.lv'
    ]
    
    # 可删除的文件扩展名
    clearable_extensions = ['.tmp', '.log', '.cache', '.dat', '.temp', '.apk', 
                            '.mp4', '.jpg', '.png', '.json', '.gif', '.webp']

    """ 遍历所有子目录，删除符合扩展名的文件 """
    for path in capcut_paths:
        if not os.path.exists(path):
            print(f"⚠ 目录不存在：{path}")
            continue

        print(f"📂 开始清理目录：{path}")

        # 遍历所有文件和子目录
        for root, dirs, files in os.walk(path):
            print(f"📂 正在扫描目录：{root}")

            for file in files:
                file_path = os.path.join(root, file)
                # 如果文件符合可删除扩展名，则删除
                if any(file.endswith(ext) for ext in clearable_extensions):
                    try:
                        os.remove(file_path)
                        print(f"✅ 已删除文件：{file_path}")
                    except Exception as e:
                        print(f"❌ 删除失败：{file_path} - 错误：{e}")

        print(f"🎉 {path} 目录清理完成！")

# 完整的清理流程
def clear_all():
    print("开始清理快手缓存和相册内容...")

    # 清理快手缓存
    clear_kuaishou_cache()

    # 清理相册内容
    clear_album()

    # 清理剪映内容
    clear_capcut_cache()

    # toast("相册快手缓存清理完毕～～", 5000)
    random_delay()

def toastCount():
    counter_data = load_counter()
    # 在这里你可以根据加载的计数器数据执行一些操作，比如打印或展示
    toast(f"今日已发布：{counter_data['counter']}条视频", 5000)

# 发布视频判断成功否
def publishProcess():
    findSelected = wait_for_node(Selector().text("精选").type("CheckedTextView"), timeout=45)
    random_delay()
    start_time = time.time()
    attempts = 0
    path = R(__file__).res("img/publishSuccess.png")  # 这里替换为你的图片地址
    while time.time() - start_time < 180:
        picShow = FindImages.find(path, confidence=0.95)
        windowShow = Selector().id("com.smile.gifmaker:id/recyclerView").find()
        justShow = Selector().text("^刚刚$").find()
        if any([picShow, windowShow, justShow]):
            print(f"picShow={picShow}, windowShow={windowShow}, justShow={justShow}")
            # 如果希望在发布视频后立即执行，并且每天都检查是否需要重置计数器，可以这样调用
            simulate_publish_video()
            random_delay()
            # 清除所有缓存
            clear_all()
            random_delay()
            return True

        attempts += 1
        random_delay(0.4, 1.0)  # 随机间隔模拟人为的操作速度

        if attempts % 5 == 0:
            print(f"轮询次数: {attempts}")

    raise TimeoutError(f"等待超过 180 秒，控件仍未找到")

# 剪映Ai去重
def jianYingAi(title):
    # title = "薰衣草花香洗衣液深层去污去渍柔顺护衣持久留香洗衣液家庭大桶装"
    findJianYing = wait_for_node(Selector().text("剪映"), timeout=45)
    click_node_simulation(Selector().text("剪映").parent(1))
    random_delay(4, 6)
    # 判断是否有恢复操作，有则点击放弃
    attempt_count = 0
    while True and attempt_count < 5:
        findRecover = Selector().text("恢复创作").find()
        if findRecover:
            print("我找到了恢复创作")
            click_node_simulation(Selector().text("放弃").clickable(True))
            break
        attempt_count += 1
        print(f"我尝试查找恢复创作第({attempt_count})次")
        random_delay(1, 2)
    findAi = wait_for_node(Selector().text("AI 剪视频"), timeout=45)
    click_node_simulation(Selector().text("AI 剪视频").parent(1))
    random_delay(4, 6)
    # 判断是否需要是第一次Ai剪视频，是则点击上传素材
    attempt_count = 0
    while True and attempt_count < 5:
        findUpload = Selector().text("上传素材").find()
        if findUpload:
            print("我找到了上传素材")
            click_node_simulation(Selector().text("上传素材").parent(1))
            break
        attempt_count += 1
        print(f"我尝试查找上传素材第({attempt_count})次")
        random_delay(1, 2)
    findAi = wait_for_node(Selector().text("下一步"), timeout=45)
    click_node_simulation(Selector().type("HorizontalScrollView").visible(True).brother(0.1).child(1).child(2))
    random_delay()
    click_node_simulation(Selector().desc("照片"))
    random_delay(2, 3)
    for num in range(1, 6):
        click_node_simulation(Selector().type("HorizontalScrollView").visible(True).brother(0.1).child(num).child(2))
        random_delay(1, 2)
    findChooseSuccess = wait_for_node(Selector().text("^3$").clickable(False), timeout=45)
    random_delay()
    click_node_simulation(Selector().text("下一步").type("Button"))
    findEditText = wait_for_node(Selector().type("EditText"), timeout=45)
    simulate_human_typing(Selector().type("EditText"), title)
    random_delay()
    click_node_simulation(Selector().text("生成视频").parent(1))
    findOutPut = wait_for_node(Selector().text("进入编辑"), timeout=180)
    click_node_simulation(Selector().text("进入编辑").parent(1))
    findVideoShow = wait_for_node(Selector().text("编辑更多"), timeout=45)
    click_node_simulation(Selector().text("编辑更多").parent(1))
    findRate = wait_for_node(Selector().text("比例"), timeout=45)
    click_node_simulation(Selector().text("比例").parent(1))
    findRateNum = wait_for_node(Selector().text("9:16"), timeout=45)
    click_node_simulation(Selector().text("9:16").parent(1))
    random_delay()
    click_node_simulation(Selector().text("导出").type("Button").brother(-0.1))
    find1080p = wait_for_node(Selector().text("1080p"), timeout=45)
    local1080p = Selector().text("1080p").find()
    click(local1080p.rect.centerX(), local1080p.rect.centerY() - 75)
    random_delay()
    find30FPS = wait_for_pic("img/30FPS.png", timeout=45)
    click(find30FPS["result"])
    random_delay()
    click_node_simulation(Selector().text("导出").type("Button"))
    findOutSuccess = wait_for_node(Selector().text("^完成$"), timeout=180)
    random_delay()
    clearApp()

def tunner(k, v):
    print(k, v)
    if k == "submit":
        # # 声明使用全局变量
        # global counter_data
        res = json.loads(v)
        # lockApp("AScript", "开发者") # 测试版1
        # lockApp("MiTest", "运 行") # 测试版2
        lockApp("聚宝盆", "运 行") # 正式版
        filterName = res["filter"]
        if res["runWay"] == "app":
            # 创建 R 类的实例
            iconPath = R(__file__).res("img/count.png")
            print("我要跑app啦")
            while True:
                print(res["filter"])
                # 清除应用
                clearApp()

                try:
                    counter_data = load_counter()
                    FloatWindow.add_menu("888", iconPath, toastCount)
                    print(counter_data)
                    click_kuaishou_icon(counter_data['counter'])
                    
                    # 点击主页三条杠
                    findSelected = wait_for_node(Selector().text("精选").type("CheckedTextView"), timeout=45)
                    random_delay()
                    try:
                        findTab = wait_for_node(Selector().desc("侧边栏"), timeout=10)
                        click_node_simulation(Selector().desc("侧边栏"))
                        ifLogin = 0
                    except TimeoutError:
                        findLoginBtn = wait_for_node(Selector().text("^登录$"), timeout=10)
                        ifLogin = 1
                        toast("这个快手号掉了，我继续跑另一个", 5000)
                        random_delay()
                        clearApp()
                        click_kuaishou_icon(counter_data['counter'] + 1)
                        findSelected = wait_for_node(Selector().text("精选").type("CheckedTextView"), timeout=45)
                        findTab = wait_for_node(Selector().desc("侧边栏"), timeout=5)
                        click_node_simulation(Selector().desc("侧边栏"))


                    # 进入快手小店
                    findShop = wait_for_node(Selector().text("快手小店"), timeout=45)
                    click_node_simulation(Selector().text("快手小店").parent(1))  # 点击快手小店
                    random_delay()

                    # 判断是否需要切换卖家，需要则点击
                    attempt_count = 0
                    while True and attempt_count < 5:
                        findChangeSeller = Selector().text("切换卖家").find()
                        if findChangeSeller:
                            print("我找到了切换卖家")
                            click_node_simulation(Selector().text("切换卖家").parent(1))
                            break
                        attempt_count += 1
                        print(f"我尝试查找切换卖家第({attempt_count})次")
                        random_delay(1, 2)

                    # 进入选品广场
                    try:
                        findChoose = wait_for_node(Selector().text("^选品$"), timeout=25)
                        click_node_simulation(Selector().text("^选品$").parent(1))  # 点击选品按钮
                    except TimeoutError:
                        try:
                            findChoosePic = wait_for_pic('img/chooseGoods.png', timeout=45)
                            print(findChoosePic["result"])
                            click(findChoosePic["result"])
                        except TimeoutError:
                            toast("我找不到选品按钮，重新来", 5000)
                            raise

                    random_delay()
                    findIndex = wait_for_node(Selector().desc("首页").type("Button"), timeout=45)
                    click_node_simulation(Selector().desc("首页").type("Button").brother(0.2)) # 点击分类按钮
                    findMenu = wait_for_node(Selector().text(filterName).path("/FrameLayout/ViewGroup/ViewPager/FrameLayout/ViewGroup/TextView"), timeout=45)
                    click_node_simulation(Selector().text(filterName).path("/FrameLayout/ViewGroup/ViewPager/FrameLayout/ViewGroup/TextView").parent(1)) # 选择类目
                    random_delay()

                    isList = wait_for_node(Selector().text("综合排序"), timeout=45)
                    random_delay()
                    slide_simulation(2, 6)

                    # 随机滑动后点击进入商品详情
                    # 最大滑动次数限制
                    max_attempts = 5
                    attempt_count = 0
                    isJoined = Selector().text("加入货架").visible(True).find()
                    # 如果找不到，执行滑动操作，直到找到"加入货架"按钮，或达到最大滑动次数
                    while not isJoined and attempt_count < max_attempts:
                        print(f"我没找到加入货架，当前滑动次数: {attempt_count + 1}")
                        slide_simulation(1, 1)
                        isJoined = Selector().text("加入货架").visible(True).find()
                        attempt_count += 1
                    # 判断是否找到了"加入货架"
                    if isJoined:
                        print("我找到加入货架了")
                        # 点击"加入货架"的父控件
                        click_node_simulation(Selector().text("加入货架").visible(True).parent(2))
                    else:
                        raise TimeoutError(f"达到最大滑动次数 {max_attempts} 次，仍未找到'加入货架'按钮")
                    random_delay()

                    # 进入详情加入货架
                    findJoinPic = wait_for_pic("img/joinShelf.png", timeout=45)
                    isJoin = Ocr.mlkitocr_v2(rect=[811,1729,1047,1845], pattern='加入货架')
                    isJoined = Ocr.mlkitocr_v2(rect=[811,1729,1047,1845], pattern='已添加')
                    if isJoin:
                        for l in isJoin:
                            print(l.x, l.y)
                            click(l.x, l.y)  # 点击加入货架按钮
                    elif isJoined:
                        print("我已经加入选品车了")
                    random_delay(3.5, 5)

                    attempt_count = 0
                    while True and attempt_count < 3:
                        findLimit = Selector().text("订单限制提示").find()
                        findTip = Selector().text("加架提示").find()
                        if findLimit:
                            print("我找到了订单限制提示")
                            click_node_simulation(Selector().text("继续加入货架").parent(1))
                            break
                        elif findTip:
                            print("我找到了加架提示")
                            click_node_simulation(Selector().text("关闭").parent(1))
                            break
                        attempt_count += 1
                        print(f"我尝试查找订单限制提示和加架提示第({attempt_count})次")
                    random_delay(3, 5)

                    # 获取标题
                    findDetails = Ocr.mlkitocr_v2(rect=[930, 1120, 1055, 1470], pattern='详|详情||详信')
                    for l in findDetails:
                        click(l.center_x, l.center_y)
                    # 获取剪贴板内容
                    findParent = wait_for_node(Selector().desc("transparent_view_key_"), timeout=45)
                    if findParent.childCount <= 4:
                        click_node_simulation(Selector().desc("transparent_view_key_").child(3))
                    else:
                        click_node_simulation(Selector().desc("transparent_view_key_").child(4))

                    findCopyLink = wait_for_node(Selector().text("复制链接"), timeout=45)
                    click_node_simulation(Selector().text("复制链接").parent(1))
                    findCopied = wait_for_node(Selector().text("快口令复制成功，快去分享给朋友吧"), timeout=45)
                    random_delay()
                    copied_text = Clipboard.get()
                    print(copied_text)
                    # 使用正则表达式提取 `¥` 符号之前的内容
                    try:
                        match = re.match(r"^(.*?)\s*￥", copied_text)
                        if match:
                            title = match.group(1)  # 获取商品名称
                            # toast(f"商品名称：{title}", 5000)
                    except TimeoutError:
                        toast("没找到合适的商品名称", 5000)
                    random_delay()
                    key.back()

                    findJoinPic = wait_for_pic("img/joinedShelf.png", timeout=45)
                    click(500, 500)
                    print("我进入主图啦")
                    random_delay()
                    process_images(res["remove_repeat"]) # 主图截图
                    clearApp()

                    # 使用快手app找视频素材
                    if res["find_video"] == "快手App":
                        # 返回主页面
                        random_delay()
                        key.back()
                        random_delay()
                        key.back()

                        videoInKuaishou(title)

                        # 进入去水印软件
                        if res["remove_mark"] == "TK去水印":
                            removeInTk()
                        elif res["remove_mark"] == "网页去水印":
                            removeInWeb()
                        elif res["remove_mark"] == "青禾去水印":
                            removeInQh()
                        
                    # 使用破解版抖音app找视频素材
                    elif res["find_video"] == "抖音App":
                        # title = "薰衣草花香洗衣液深层去污去渍柔顺护衣持久留香洗衣液家庭大桶装"
                        clearApp()
                        random_delay()

                        douyinCrack(title)
                    
                    # 使用剪映的AI剪视频来去重
                    if res["remove_repeat"] == "剪映AI":
                        jianYingAi(title)

                    # 发布视频
                    if ifLogin == 0:
                        click_kuaishou_icon(counter_data['counter'])
                    elif ifLogin == 1:
                        click_kuaishou_icon(counter_data['counter'] + 1)
                    findSelected = wait_for_node(Selector().text("精选").type("CheckedTextView"), timeout=45)
                    shotShow = Selector().desc("^拍摄$").find()
                    path = R(__file__).res("img/publishSuccess.png")  # 这里替换为你的图片地址
                    picShow = FindImages.find(path, confidence=0.95) 
                    if shotShow:
                        click_node_simulation(Selector().desc("^拍摄$"))
                    elif picShow:
                        click(picShow['result'])
                    else:
                        toast("找不到发布按钮", 5000)
                    # findPublishAdd = wait_for_node(Selector().desc("^拍摄$"), timeout=45)
                    # click_node_simulation(Selector().desc("^拍摄$"))
                    # findAddBtn = wait_for_node(Selector().id("com.smile.gifmaker:id/shoot_container"), timeout=45)
                    # click_node_simulation(Selector().id("com.smile.gifmaker:id/shoot_container")) # 点击加号发布按钮
                    findGallery = wait_for_node(Selector().text("相册"), timeout=45)
                    click_node_simulation(Selector().text("相册").parent(1))  # 点击相册
                    findVideos = wait_for_node(Selector().id("com.smile.gifmaker:id/album_view_list").visible(True),
                                            timeout=45)
                    random_delay()
                    if res["remove_repeat"] == "剪映AI":
                        click_node_simulation(Selector().id("com.smile.gifmaker:id/album_view_list").visible(True).child(1).child(2)) # 选取视频
                        random_delay()
                        findNextStep1 = wait_for_node(Selector().id("com.smile.gifmaker:id/picked_recycler_view").childCount(1))
                        findNextStep1Pic = wait_for_pic("img/nextStep1.png", timeout=45)
                        random_delay()
                        click(findNextStep1Pic["result"])
                    else:
                        click_node_simulation(Selector().id("com.smile.gifmaker:id/album_view_list").visible(True).child(1).child(2)) # 选取视频
                        random_delay(0.8, 1.2)
                        click_node_simulation(Selector().id("com.smile.gifmaker:id/album_view_list").visible(True).child(3).child(2)) # 选取图片1
                        random_delay(0.8, 1.2)
                        click_node_simulation(Selector().id("com.smile.gifmaker:id/album_view_list").visible(True).child(2).child(2)) # 选取图片2
                        random_delay()
                        findNextStep3 = wait_for_node(Selector().id("com.smile.gifmaker:id/picked_recycler_view").childCount(3))
                        findNextStep3Pic = wait_for_pic("img/nextStep3.png", timeout=45)
                        random_delay()
                        click(findNextStep3Pic["result"])
                        
                    # findChosenVideo = wait_for_node(Selector().id("com.smile.gifmaker:id/picked_recycler_view").child(2), timeout=45)
                    # click_node_simulation(Selector().id("com.smile.gifmaker:id/next_step")) # 点击进入下一步
                    findMusic = wait_for_node(Selector().text("选择音乐"), timeout=45)
                    random_delay()
                    findNextStepPic = wait_for_pic("img/nextStep.png", timeout=45)
                    random_delay()
                    click(findNextStepPic["result"])  # 点击进入下一步

                    # 获取标题
                    findPublish = wait_for_node(Selector().id("com.smile.gifmaker:id/publish_button"), timeout=45)
                    simulate_human_typing(Selector().type("EditText"), title) # 输入标题
                    random_delay()

                    # 选择话题
                    click_node_simulation(Selector().id("com.smile.gifmaker:id/recycler_view").child(4).child(1)) # 第一个话题
                    random_delay(0.8, 1.2)
                    click_node_simulation(Selector().id("com.smile.gifmaker:id/recycler_view").child(4).child(1)) # 第二个话题
                    random_delay(0.8, 1.2)
                    click_node_simulation(Selector().id("com.smile.gifmaker:id/recycler_view").child(4).child(1)) # 第三个话题
                    random_delay(0.8, 1.2)

                    # 挂车
                    findService = wait_for_node(Selector().text("作者服务"), timeout=45)
                    click_node_simulation(Selector().text("作者服务").parent(1))  # 点击作者服务
                    findLinkGood = wait_for_node(Selector().text("关联商品"), timeout=45)
                    click_node_simulation(Selector().text("关联商品").parent(1))  # 点击关联商品
                    findLinkMain = wait_for_node(Selector().text("关联主推品"), timeout=45)
                    click_node_simulation(Selector().text("关联主推品").parent(1))  # 点击关联主推品
                    findSearch = wait_for_node(Selector().text("搜索"), timeout=45)
                    Selector().text("搜索").brother(1).input(title).find()  # 输入商品标题
                    random_delay()
                    findAddGood = wait_for_node(Selector().text(title).type("TextView"), timeout=45)
                    Selector().text(title).type("TextView").parent(1).brother(-0.1).click().find() # 选择商品
                    # findAddGood = wait_for_node(Selector().text("搜索").brother(3), timeout=45)
                    # Selector().text("搜索").brother(3).click().find()  # 选择商品
                    random_delay()
                    findAddBtn = wait_for_node(Selector().text("添加").path("/FrameLayout/ViewGroup/TextView").parent(1), timeout=45)
                    click_node_simulation(Selector().text("添加").path("/FrameLayout/ViewGroup/TextView").parent(1)) # 点击添加按钮
                    random_delay()
                    knowHint = Selector().text("我知道了").find()
                    if knowHint:
                        click_node_simulation(Selector().text("我知道了").parent(1))
                    findSaveBtn = wait_for_node(Selector().text("保存"), timeout=45)
                    click_node_simulation(Selector().text("保存").parent(1)) # 点击保存按钮
                    findPublishBtn = wait_for_node(Selector().id("com.smile.gifmaker:id/publish_button"), timeout=45)
                    click_node_simulation(Selector().id("com.smile.gifmaker:id/publish_button")) # 点击发布按钮
                    publishProcess()
                except TimeoutError:
                    toast("被你玩坏了，5秒后重新玩吧～～", 5000)
                    random_delay(4.5, 5.5)
                    continue

w = Window(R(__file__).ui("myUi.html"), tunner)
w.width(-1)
w.height("80vh")
w.show()
