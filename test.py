import jieba

# 默认是精确模式
seg_list = jieba.cut("宣城市人民政府关于调整宣城市中心城区和宣州区城镇土地使用税适用税额标准的通知", cut_all=True)
seg_list = ", ".join(seg_list)
print(seg_list)
