# 安全帽佩戴概率提示词配置

## 基础概率检测提示词

```prompt
判断图片中的人是否佩戴安全帽。
请返回一个1到100之间的整数，表示此人佩戴安全帽的概率。
数值越接近100，表示此人佩戴安全帽的可能性越大；
数值越接近1，表示此人佩戴安全帽的可能性越小。
只返回符合以下格式的 JSON：
{
    "helmet_score": <佩戴安全帽的概率分数，1到100之间的整数>
}
```

## 输出格式配置

```json
{
    "type": "object",
    "properties": {
        "helmet_score": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
        }
    },
    "required": ["helmet_score"]
}
``` 