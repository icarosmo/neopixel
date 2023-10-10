from pyneopixel import NeoPixel
import time

# 设置 NeoPixel 参数
pin = 0  # 选择一个数字引脚，可以根据硬件连接进行更改
num_leds = 8  # 你的NeoPixel上LED的数量
np = NeoPixel(pin, num_leds)

# 流水灯效果
while True:
    for i in range(num_leds):
        np[i] = (255, 0, 0)  # 设置LED颜色为红色 (R, G, B)
        np.write()
        time.sleep(0.2)  # 延时
        np[i] = (0, 0, 0)  # 关闭LED
    time.sleep(0.5)  # 等待一段时间后再重复
