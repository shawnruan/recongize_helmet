# 安全帽检测提示词配置

## 基础检测提示词

```prompt
判断图片中的人是否佩戴安全帽。
只返回符合以下格式的 JSON：
{
    "helmet": <是否佩戴安全帽，1表示佩戴，0表示未佩戴>
}
```

## 输出格式配置

```json
{
    "type": "object",
    "properties": {
        "helmet": {
            "type": "integer",
            "enum": [0, 1]
        }
    },
    "required": ["helmet"]
}
```

