import re
import requests
import random
import os


# 定义函数方法
def spider_pic(html, keyword, path_word, max_num):
    print(f"正在查找{keyword}对应的图片，下载中，请稍后。。。。。。")
    addr_list = re.findall('"objURL":"(.*?)"', html, re.S)  # 返回的地址列表
    count = 0  # 用于计数已经下载的图片数量
    while count < max_num:
        for addr in addr_list:
            print('正在爬取URL地址：' + str(addr)[0:30] + '...')  # 显示正在爬取的地址（前30个字符）

            try:
                # 添加User-Agent请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                }
                pics = requests.get(addr, headers=headers, timeout=20)  # 请求URL时间
                pics.raise_for_status()  # 如果响应状态码不是200，则抛出异常

            except requests.exceptions.RequestException as e:
                print(f"请求失败: {e}")
                continue

            # 创建文件夹路径
            folder_path = os.path.join('./百度图片', path_word)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # 保存图片
            file_path = os.path.join(folder_path, keyword + '_' + str(random.randrange(0, 1000)) + '.jpg')
            with open(file_path, 'wb') as f:
                f.write(pics.content)

            # 验证图片是否有效
            if not is_valid_image(file_path):
                print(f"图片 {file_path} 破损，删除并重新下载。")
                os.remove(file_path)  # 删除破损图片
                continue  # 继续下载下一张图片

            count += 1  # 每下载一张有效的图片，计数器加1

            if count >= max_num:
                print(f"已爬取到{max_num}张有效图片，停止爬取。")
                break

            # 增加请求间隔，避免被封禁
            # time.sleep(random.uniform(1, 3))  # 随机延迟1到3秒

def is_valid_image(file_path):
    try:
        with open(file_path, 'rb') as f:
            # 读取文件的前几个字节
            data = f.read(10)
            if data.startswith(b'\xff\xd8'):  # JPEG文件通常以0xFFD8开始
                return True
    except Exception as e:
        print(f"验证图片时出错: {e}")
    return False


if __name__ == '__main__':
    cur_dir = './百度图片'
    file = input('输入一个您要保存图片的文件夹名称：')
    path = os.path.join(cur_dir, file)

    if not os.path.exists(path):
        os.makedirs(path)  # 创建路径下输入文件夹名称

    word = input('请输入你要搜索的图片关键字: ')
    max_images = int(input('请输入要爬取的图片数量: '))  # 获取用户想要爬取的图片数量

    # 修改百度图片搜索URL，正确拼接参数
    result = requests.get(f'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={word}&pn=0')

    # 调用函数，爬取图片
    spider_pic(result.text, word, file, max_images)
