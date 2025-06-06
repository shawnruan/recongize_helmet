# 安全帽数量统计提示词配置

## 数量统计提示词

```prompt
分析图片中的人物情况，请严格按照以下规则计数：
- head: 未戴安全帽的人数
- helmet: 戴安全帽的人数
- person: 图片中的总人数（应等于 head + helmet）
- alert: 是否存在未戴安全帽的情况

只返回符合以下格式的 JSON：
{
    "head": <未戴安全帽的人数>,
    "helmet": <戴安全帽的人数>,
    "person": <总人数>,
    "alert": <是否存在未戴安全帽的情况>
}

注意：确保 head + helmet = person
```

## 输出格式配置

```json
{
    "type": "object",
    "properties": {
        "helmet": {
            "type": "integer"
        },
        "head": {
            "type": "integer"
        },
        "person": {
            "type": "integer"
        },
        "alert": {
            "type": "boolean"
        }
    },
    "required": [
        "helmet",
        "head",
        "person",
        "alert"
    ]
}
``` 